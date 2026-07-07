// PRELOADER
window.addEventListener('load', () => {
    setTimeout(() => {
        const preloader = document.getElementById('preloader');
        if (preloader) preloader.classList.add('hidden');
    }, 1500);
});

// CUSTOM CURSOR
const cursor = document.getElementById('cursor');
if (cursor) {
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    document.querySelectorAll('a, button, .feature-card, .testimonial-card, .metric-card').forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });
}

// PARTICLES
const particlesContainer = document.getElementById('particles');
if (particlesContainer) {
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        const size = Math.random() * 8 + 4;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDuration = (Math.random() * 15 + 10) + 's';
        particle.style.animationDelay = Math.random() * 10 + 's';
        particlesContainer.appendChild(particle);
    }
}

// NAVBAR SCROLL
const navbar = document.getElementById('navbar');
const scrollTopBtn = document.getElementById('scrollTop');

window.addEventListener('scroll', () => {
    if (navbar) {
        if (window.scrollY > 80) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    if (scrollTopBtn) {
        if (window.scrollY > 500) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    }

    // Active nav link (for in-page anchors on the home page)
    const sections = document.querySelectorAll('section[id]');
    sections.forEach(section => {
        const top = section.offsetTop - 100;
        const bottom = top + section.offsetHeight;
        const id = section.getAttribute('id');
        const link = document.querySelector(`.nav-links a[href="#${id}"]`);
        if (link) {
            if (window.scrollY >= top && window.scrollY < bottom) {
                document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
                link.classList.add('active');
            }
        }
    });
});

// MOBILE NAV
function toggleNav() {
    const navLinks = document.getElementById('navLinks');
    if (navLinks) navLinks.classList.toggle('active');
}

document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        const navLinks = document.getElementById('navLinks');
        if (navLinks) navLinks.classList.remove('active');
    });
});

// SCROLL TO TOP
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// MODALS
function openModal(type) {
    const modal = document.getElementById(type + 'Modal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(type) {
    const modal = document.getElementById(type + 'Modal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function switchModal(from, to) {
    closeModal(from);
    setTimeout(() => openModal(to), 300);
}

document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});

// FORM HANDLERS (client-side UX only — actual submission goes to Flask routes)
function handleSignin(e) {
    e.preventDefault();
    alert('✅ Sign In successful! Welcome back to OptiCrop.');
    closeModal('signin');
}

function handleSignup(e) {
    e.preventDefault();
    alert('🎉 Account created successfully! Welcome to OptiCrop.');
    closeModal('signup');
}

// ==========================================
// CROP PREDICTION & WEATHER AUTOFILL
// ==========================================

// Check for redirect triggers on load
window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('trigger_signin') === 'True' || urlParams.has('trigger_signin')) {
        setTimeout(() => openModal('signin'), 1600);
    } else if (urlParams.get('trigger_signup') === 'True' || urlParams.has('trigger_signup')) {
        setTimeout(() => openModal('signup'), 1600);
    }
});

function triggerWeatherAutofill() {
    const btn = document.getElementById('btnAutofill');
    const originalText = btn ? btn.innerHTML : '';
    
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right: 6px;"></i>Querying Sensors...';
    }
    
    fetch('/api/weather-autofill')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Sensor error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Fill forms
            document.getElementById('temperature').value = data.temperature;
            document.getElementById('humidity').value = data.humidity;
            document.getElementById('rainfall').value = data.rainfall;
            document.getElementById('ph').value = data.ph;
            document.getElementById('nitrogen').value = data.nitrogen;
            document.getElementById('phosphorus').value = data.phosphorus;
            document.getElementById('potassium').value = data.potassium;
            
            // Show custom notice toast
            alert(`🌦️ Micro-climate station sync successful!\n\nParameters auto-filled:\nTemp: ${data.temperature}°C, Humidity: ${data.humidity}%, Rain: ${data.rainfall}mm\n\nVerified via API Key authentication.`);
        } else {
            alert("Failed to retrieve sensor metrics: " + (data.error || "Unknown error"));
        }
    })
    .catch(error => {
        console.error("Autofill Error:", error);
        alert("Failed to fetch weather telemetry. Please check server logs and API key.");
    })
    .finally(() => {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = originalText;
        }
    });
}

function handlePredict(event) {
    event.preventDefault(); // Prevents the page from refreshing

    // Get UI elements
    const form = document.getElementById('cropForm');
    const loader = document.getElementById('loadingPrediction');
    const results = document.getElementById('predictionResults');

    // Show loading spinner, hide form and previous results
    if (form) form.style.display = 'none';
    if (loader) loader.style.display = 'block';
    if (results) results.style.display = 'none';

    // Gather data from the form inputs
    const formData = {
        nitrogen: parseFloat(document.getElementById('nitrogen').value),
        phosphorus: parseFloat(document.getElementById('phosphorus').value),
        potassium: parseFloat(document.getElementById('potassium').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        ph: parseFloat(document.getElementById('ph').value),
        rainfall: parseFloat(document.getElementById('rainfall').value)
    };

    // Send data to the Flask backend
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(json => {
                throw new Error(json.error || `Server error ${response.status}`);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Prediction success:', data);
        if (data.success && data.prediction_id) {
            // Smoothly redirect to results page
            setTimeout(() => {
                window.location.href = '/result?id=' + data.prediction_id;
            }, 800);
        } else {
            throw new Error(data.error || 'Prediction response formatting error');
        }
    })
    .catch(error => {
        console.error('Prediction Error:', error);
        alert("Recommendation execution failed: " + error.message);
        
        // Reset UI on error
        if (loader) loader.style.display = 'none';
        if (form) form.style.display = 'block';
    });
}


// SCROLL REVEAL
const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.15 });

revealElements.forEach(el => revealObserver.observe(el));

// COUNTER ANIMATION
const statNumbers = document.querySelectorAll('.stat-number');

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseInt(el.getAttribute('data-count'));
            const suffix = el.textContent.replace(/[0-9]/g, '');
            let current = 0;
            const increment = target / 60;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                el.textContent = Math.floor(current) + suffix;
            }, 25);
            counterObserver.unobserve(el);
        }
    });
}, { threshold: 0.5 });

statNumbers.forEach(el => counterObserver.observe(el));

// SMOOTH SCROLL (for in-page anchors like #findcrop on the home page)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        const target = document.querySelector(targetId);
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// TILT EFFECT
document.querySelectorAll('.feature-card, .metric-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = '';
    });
});