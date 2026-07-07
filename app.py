"""
OptiCrop - Smart Agricultural Production Optimization Engine
Flask application entry point with authentication, database logging,
admin controls, and weather API integration.
"""

import pickle
import os
import traceback
import subprocess
import sys
from pathlib import Path
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session

import database as db

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "opticrop-dev-secret-key-32810"

# Integrated User API Key
API_KEY = "AQ.Ab8RN6K4BL0XF5EEreS4LG2MozqtVMMwHoCFJteGoA4dDmzlUg"

# Load the model at startup
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

crop_model = None

try:
    if not MODEL_PATH.exists():
        print("[WARNING] model.pkl not found. Training model automatically...")
        # Run main.py to train model and create model.pkl
        subprocess.run([sys.executable, str(BASE_DIR / "main.py")], cwd=str(BASE_DIR), check=True)
        
    with open(MODEL_PATH, "rb") as f:
        crop_model = pickle.load(f)
    print("[SUCCESS] Machine Learning model loaded successfully!")
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")
    crop_model = None

# Initialize Database
db.init_db()

@app.before_request
def log_session():
    if not request.path.startswith('/static'):
        log_msg = f"[Session Logs] Path: {request.path} | Method: {request.method} | Session: {dict(session)}"
        try:
            # Safely encode with replace to avoid CP1252 print crashes on Windows terminals
            print(log_msg.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8'))
        except Exception:
            # Fallback in case of encoding failures
            print(f"[Session Logs] Path: {request.path} | Method: {request.method}")

# Crop metadata for all 22 crops in the dataset
CROP_METADATA = {
    "rice": {
        "name": "Rice (Paddy)",
        "icon": "fa-seedling",
        "yield": "5.5 - 8.0 tons/hectare",
        "season": "Kharif (Monsoon) - 4-5 months",
        "water": "Very High (Requires flooded fields or high precipitation)",
        "sunlight": "6 - 8 hours daily",
        "tips": [
            "Maintain 5-10 cm standing water during the vegetative stage.",
            "Apply nitrogen in 3 split doses (basal, tillering, and panicle initiation).",
            "Monitor regularly for blast disease and stem borer insects."
        ]
    },
    "maize": {
        "name": "Maize (Corn)",
        "icon": "fa-leaf",
        "yield": "7.0 - 10.0 tons/hectare",
        "season": "Kharif & Rabi - 3-4 months",
        "water": "Moderate (500-800 mm water requirements)",
        "sunlight": "7 - 9 hours daily",
        "tips": [
            "Ensure warm and well-aerated soil before planting.",
            "Provide high nitrogen nutrition, particularly during jointing stage.",
            "Avoid waterlogging at flowering and grain-filling stages."
        ]
    },
    "chickpea": {
        "name": "Chickpea (Gram)",
        "icon": "fa-seedling",
        "yield": "1.5 - 2.5 tons/hectare",
        "season": "Rabi (Winter) - 3-4 months",
        "water": "Low (Requires light, timely irrigations)",
        "sunlight": "6 - 8 hours daily",
        "tips": [
            "Use Rhizobium culture seed treatment to enhance nitrogen fixation.",
            "Avoid excess irrigation to prevent root rot and vegetative overgrowth.",
            "Keep monitoring for pod borer infestations at fruiting stage."
        ]
    },
    "kidneybeans": {
        "name": "Kidney Beans (Rajma)",
        "icon": "fa-seedling",
        "yield": "1.2 - 2.0 tons/hectare",
        "season": "Rabi / Spring - 3-4 months",
        "water": "Moderate (Consistent soil moisture is essential)",
        "sunlight": "6 - 8 hours daily",
        "tips": [
            "Requires well-drained, sandy loam soils for optimal root growth.",
            "Highly sensitive to frost; plant only when cold risks pass.",
            "Incorporate organic matter and phosphorus into the seedbed."
        ]
    },
    "pigeonpeas": {
        "name": "Pigeon Peas (Arhar/Tur)",
        "icon": "fa-seedling",
        "yield": "1.5 - 2.2 tons/hectare",
        "season": "Kharif - 6-9 months",
        "water": "Low-Moderate (Highly drought-resistant due to taproots)",
        "sunlight": "7 - 9 hours daily",
        "tips": [
            "An excellent choice for crop rotation and soil structure repair.",
            "Inoculate seeds to maximize natural nitrogen fixing capabilities.",
            "Provide proper drainage to prevent waterlogging during early growth."
        ]
    },
    "mothbeans": {
        "name": "Moth Beans",
        "icon": "fa-seedling",
        "yield": "0.5 - 1.0 tons/hectare",
        "season": "Kharif (Monsoon) - 2-3 months",
        "water": "Very Low (Extremely drought-tolerant)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Ideal for sandy and marginal soils with low fertility.",
            "Prevents soil erosion due to its low-spreading mat growth pattern.",
            "Harvest promptly when pods dry to prevent pod shattering."
        ]
    },
    "mungbean": {
        "name": "Mung Bean (Green Gram)",
        "icon": "fa-seedling",
        "yield": "0.8 - 1.5 tons/hectare",
        "season": "Summer / Kharif - 2-3 months",
        "water": "Low (Prefers dry harvest conditions)",
        "sunlight": "7 - 8 hours daily",
        "tips": [
            "A fast-maturing crop that fits perfectly as a catch crop.",
            "Harvest in multiple pickings as pods mature unevenly.",
            "Highly beneficial for replenishing soil organic nitrogen."
        ]
    },
    "blackgram": {
        "name": "Black Gram (Urad)",
        "icon": "fa-seedling",
        "yield": "0.8 - 1.6 tons/hectare",
        "season": "Kharif & Rabi - 2-3 months",
        "water": "Low-Moderate (Prefers warm conditions)",
        "sunlight": "7 - 8 hours daily",
        "tips": [
            "Thrives in heavy soils with good moisture-retaining capacity.",
            "Treat seeds with fungicide to prevent seed-borne illnesses.",
            "Apply phosphorus at sowing to stimulate root development."
        ]
    },
    "lentil": {
        "name": "Lentil (Masoor)",
        "icon": "fa-seedling",
        "yield": "1.0 - 1.8 tons/hectare",
        "season": "Rabi (Winter) - 3-4 months",
        "water": "Low (Sensitive to waterlogging)",
        "sunlight": "6 - 8 hours daily",
        "tips": [
            "Thrives in cool climates and well-drained loam soils.",
            "Keep fields weed-free, especially in the first 40 days.",
            "Harvest when pods turn brown and dry to prevent yield loss."
        ]
    },
    "pomegranate": {
        "name": "Pomegranate",
        "icon": "fa-apple-alt",
        "yield": "12.0 - 15.0 tons/hectare",
        "season": "Perennial (Harvest in Bahar cycles)",
        "water": "Medium (Highly drought tolerant once established)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Utilize drip irrigation for consistent growth and fruit sizing.",
            "Prune branches regularly to maintain light penetration and shape.",
            "Protect developing fruit from fruit-borers using bagging."
        ]
    },
    "banana": {
        "name": "Banana",
        "icon": "fa-pepper-hot",
        "yield": "30.0 - 50.0 tons/hectare",
        "season": "Year-round (11-14 months crop cycle)",
        "water": "Very High (Needs frequent, deep irrigation)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Heavy potassium feeder; supply potassium rich fertilizers.",
            "Provide shelter belts to prevent leaf shredding by high winds.",
            "Perform de-suckering to leave only one main pseudo-stem per pit."
        ]
    },
    "mango": {
        "name": "Mango",
        "icon": "fa-apple-alt",
        "yield": "8.0 - 12.0 tons/hectare",
        "season": "Perennial (Fruiting in Summer)",
        "water": "Medium (Reduce irrigation before flowering to induce blooms)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Grows best in deep, well-drained alluvial or loamy soils.",
            "Control powdery mildew and hopper pests during flowering.",
            "Harvest when fruits develop a slight color break near the beak."
        ]
    },
    "grapes": {
        "name": "Grapes",
        "icon": "fa-wine-glass",
        "yield": "15.0 - 20.0 tons/hectare",
        "season": "Perennial (Harvest in late Winter/Spring)",
        "water": "Medium (Needs precise water budget to avoid berry splitting)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Requires strong trellising supports and severe yearly pruning.",
            "Minimize overhead irrigation to prevent fungal leaf infections.",
            "Harvest when sugar content reaches optimal Brix level."
        ]
    },
    "watermelon": {
        "name": "Watermelon",
        "icon": "fa-circle",
        "yield": "20.0 - 30.0 tons/hectare",
        "season": "Summer (Zaid) - 3-4 months",
        "water": "Medium-High (Critical at vine development and fruit set)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Requires light-textured, sandy loam soils with warm temperatures.",
            "Use straw mulching to control weeds and maintain soil temperature.",
            "Harvest when the bottom spot turns creamy white or yellow."
        ]
    },
    "muskmelon": {
        "name": "Muskmelon",
        "icon": "fa-circle",
        "yield": "15.0 - 22.0 tons/hectare",
        "season": "Summer (Zaid) - 3-4 months",
        "water": "Medium (Reduce irrigation during ripening for higher sweetness)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Enjoys dry atmospheric conditions during fruit maturity.",
            "Ensure plenty of organic manure is incorporated during soil prep.",
            "Look for 'slip' stage (stem separating easily) to harvest."
        ]
    },
    "apple": {
        "name": "Apple",
        "icon": "fa-apple-alt",
        "yield": "20.0 - 30.0 tons/hectare",
        "season": "Perennial (Fruiting in late Summer/Autumn)",
        "water": "Medium (Sensitive to severe soil moisture fluctuations)",
        "sunlight": "7 - 9 hours daily",
        "tips": [
            "Requires a specific minimum chilling hours (below 7°C) in winter.",
            "Prune dormant trees to encourage fruiting spurs and air circulation.",
            "Thin excess small fruits to prevent alternate bearing cycle."
        ]
    },
    "orange": {
        "name": "Orange (Citrus)",
        "icon": "fa-lemon",
        "yield": "15.0 - 25.0 tons/hectare",
        "season": "Perennial (Harvest in Winter)",
        "water": "Medium-High (Regular watering during fruit development)",
        "sunlight": "7 - 9 hours daily",
        "tips": [
            "Choose frost-free locations or use windbreaks for cold protection.",
            "Apply balanced fertilizer including zinc and iron micro-nutrients.",
            "Monitor and treat early for citrus canker and leaf miner."
        ]
    },
    "papaya": {
        "name": "Papaya",
        "icon": "fa-apple-alt",
        "yield": "40.0 - 60.0 tons/hectare",
        "season": "Year-round (9-12 months crop cycle)",
        "water": "High (Requires regular moisture but zero waterlogging)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Sow seeds on raised beds to protect the delicate root system.",
            "Feed nitrogen and phosphorus fertilizers regularly every 2 months.",
            "Harvest when color changes from green to yellow at the base."
        ]
    },
    "coconut": {
        "name": "Coconut",
        "icon": "fa-egg",
        "yield": "80 - 120 nuts/palm/year",
        "season": "Perennial (Lifespan of 60+ years)",
        "water": "High (Prefers coastal aquifers and high rainfall)",
        "sunlight": "9 - 10 hours daily",
        "tips": [
            "Extremely salt-tolerant, thrives in sandy coastal soils.",
            "Apply organic manure and common salt (sodium chloride) to soil.",
            "Clear weeds in a 2-meter radius basin around palm trunks."
        ]
    },
    "cotton": {
        "name": "Cotton",
        "icon": "fa-cloud",
        "yield": "1.5 - 3.0 tons/hectare",
        "season": "Kharif - 5-6 months",
        "water": "Medium (Requires dry weather during boll opening)",
        "sunlight": "8 - 10 hours daily",
        "tips": [
            "Requires deep black cotton soils or alluvial sandy-clays.",
            "Maintain soil potassium levels to improve boll size and lint weight.",
            "Control bollworms using BT cultivars and integrated pest management."
        ]
    },
    "jute": {
        "name": "Jute",
        "icon": "fa-bars",
        "yield": "2.0 - 3.5 tons/hectare",
        "season": "Kharif (Monsoon) - 4-5 months",
        "water": "High (Requires high humidity and rainfall)",
        "sunlight": "7 - 8 hours daily",
        "tips": [
            "Harvest jute at the early pod-formation stage for optimal fiber quality.",
            "Conduct retting (soaking stems) in clean, slow-flowing water.",
            "Thrives best in fertile alluvial soils and warm river basins."
        ]
    },
    "coffee": {
        "name": "Coffee",
        "icon": "fa-coffee",
        "yield": "1.0 - 2.0 tons/hectare",
        "season": "Perennial (Fruits harvested in Winter)",
        "water": "High (Prefers misty hills and well-distributed rain)",
        "sunlight": "Filtered light (Requires shade trees like silver oak)",
        "tips": [
            "Requires acidic, deep volcanic or organic-rich hillside soils.",
            "Prune vertical suckers to channel energy into lateral branches.",
            "Hand-pick only the fully ripe coffee berries."
        ]
    }
}

# ---------------------------------------------------------------------------
# Middlewares / Decorators
# ---------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in or create an account to access this page.", "warning")
            return redirect(url_for("home", trigger_signin=True))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "admin":
            flash("Unauthorized access. Admin privileges required.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

# Context processor to inject global parameters
@app.context_processor
def inject_user_status():
    return {
        "logged_in": "user_id" in session,
        "username": session.get("username"),
        "full_name": session.get("full_name"),
        "is_admin": session.get("role") == "admin"
    }

# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    trigger_signin = request.args.get("trigger_signin")
    return render_template("home.html", trigger_signin=trigger_signin)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/findyourcrop")
@login_required
def find_your_crop():
    return render_template("findyourcrop.html")


@app.route("/result")
@login_required
def result():
    prediction_id = request.args.get("id")
    if not prediction_id:
        flash("No prediction report identifier provided.", "warning")
        return redirect(url_for("dashboard"))
        
    prediction = db.get_prediction_by_id(prediction_id)
    if not prediction:
        flash("Prediction report not found.", "error")
        return redirect(url_for("dashboard"))
        
    # Security check: standard users can only view their own reports
    if session.get("role") != "admin" and prediction["user_id"] != session.get("user_id"):
        flash("Access denied to this prediction report.", "error")
        return redirect(url_for("dashboard"))
        
    # Get crop metadata
    crop_key = prediction["predicted_crop"].lower().strip()
    # Handle cases like "rice (paddy)"
    for key in CROP_METADATA:
        if key in crop_key or crop_key in key:
            crop_key = key
            break
            
    crop_info = CROP_METADATA.get(crop_key, {
        "name": prediction["predicted_crop"],
        "icon": "fa-seedling",
        "yield": "N/A",
        "season": "N/A",
        "water": "N/A",
        "sunlight": "N/A",
        "tips": ["Refer to general agricultural guides for this crop."]
    })
    
    return render_template("result.html", prediction=prediction, crop_info=crop_info)


@app.route("/dashboard")
@login_required
def dashboard():
    user_predictions = db.get_user_predictions(session["user_id"])
    return render_template("dashboard.html", predictions=user_predictions)

# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------

@app.route("/signin", methods=["POST"])
def signin():
    identifier = request.form.get("email") # Serves as username or email
    password = request.form.get("password")
    
    user = db.verify_user(identifier, password)
    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["full_name"] = user["fullname"]
        session["role"] = user["role"]
        
        flash(f"Welcome back, {user['fullname']}!", "success")
        if user["role"] == "admin":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid email/username or password. Please try again.", "error")
        return redirect(url_for("home", trigger_signin=True))


@app.route("/signup", methods=["POST"])
def signup():
    full_name = request.form.get("full_name")
    username = request.form.get("username", "").lower().strip()
    email = request.form.get("email", "").lower().strip()
    password = request.form.get("password")
    
    # Simple username generator if not provided
    if not username:
        username = email.split("@")[0]
        
    success, message = db.register_user(full_name, username, email, password)
    if success:
        # Automatically log the user in
        user = db.verify_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["full_name"] = user["fullname"]
            session["role"] = user["role"]
            flash(f"Account created successfully! Welcome to your dashboard, {user['fullname']}!", "success")
            return redirect(url_for("dashboard"))
            
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("home", trigger_signin=True))
    else:
        flash(f"Sign up failed: {message}", "error")
        return redirect(url_for("home", trigger_signup=True))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("home"))

# ---------------------------------------------------------------------------
# API Key Simulated Weather Endpoint
# ---------------------------------------------------------------------------

@app.route("/api/weather-autofill", methods=["GET"])
@login_required
def weather_autofill():
    """Uses the configured API key to fetch simulated local agricultural weather metrics."""
    # Ensure API Key exists
    if not API_KEY:
        return jsonify({"success": False, "error": "API Key is missing."}), 500
        
    # Log usage of API key
    print(f"[API Logs] Weather autofill triggered using API Key: {API_KEY[:6]}...{API_KEY[-4:]}")
    
    # In a real environment, this makes an HTTP request passing the API key.
    # We simulate this behavior with realistic crop-predictive values.
    import random
    data = {
        "success": True,
        "temperature": round(random.uniform(18.0, 32.0), 1),
        "humidity": round(random.uniform(50.0, 85.0), 1),
        "rainfall": round(random.uniform(60.0, 220.0), 1),
        "ph": round(random.uniform(5.5, 7.5), 1),
        "nitrogen": random.randint(50, 110),
        "phosphorus": random.randint(30, 80),
        "potassium": random.randint(30, 80),
        "message": f"Successfully loaded mock weather station coordinates via API Key ({API_KEY[:6]}...)"
    }
    return jsonify(data)

# ---------------------------------------------------------------------------
# Prediction API
# ---------------------------------------------------------------------------

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    if crop_model is None:
        return jsonify({"success": False, "error": "ML Prediction Model is not loaded on the server"}), 500

    try:
        # Support both JSON payload (AJAX) and form submissions
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                "nitrogen": request.form.get("nitrogen"),
                "phosphorus": request.form.get("phosphorus"),
                "potassium": request.form.get("potassium"),
                "temperature": request.form.get("temperature"),
                "humidity": request.form.get("humidity"),
                "ph": request.form.get("ph"),
                "rainfall": request.form.get("rainfall"),
            }

        # Check required fields
        required_fields = ["temperature", "humidity", "rainfall", "ph", "nitrogen", "phosphorus", "potassium"]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({"success": False, "error": f"Missing agricultural parameters: {', '.join(missing)}"}), 400

        # Parse and validate ranges
        try:
            temperature = float(data["temperature"])
            humidity = float(data["humidity"])
            rainfall = float(data["rainfall"])
            ph = float(data["ph"])
            nitrogen = float(data["nitrogen"])
            phosphorus = float(data["phosphorus"])
            potassium = float(data["potassium"])
        except ValueError:
            return jsonify({"success": False, "error": "Invalid parameter input. Please enter numeric values."}), 400

        # Make prediction
        if hasattr(crop_model, 'predict') and callable(getattr(crop_model, 'predict')):
            try:
                # Rule-based custom model prediction
                recommendation = crop_model.predict(
                    temperature, humidity, rainfall, ph, nitrogen, phosphorus, potassium
                )
                if isinstance(recommendation, dict):
                    crop_name = recommendation.get("name", "Mixed Vegetables")
                    confidence = recommendation.get("confidence", 85)
                else:
                    crop_name = str(recommendation)
                    confidence = 88
            except TypeError:
                # Sklearn ML model prediction
                features = [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]
                prediction = crop_model.predict([features])
                crop_name = str(prediction[0]).capitalize()
                confidence = 94
        else:
            return jsonify({"success": False, "error": "Invalid recommendation model structure"}), 500

        # Log prediction to SQL database
        prediction_id = db.add_prediction(
            user_id=session["user_id"],
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            temp=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall,
            predicted_crop=crop_name,
            confidence=confidence
        )

        return jsonify({
            "success": True,
            "prediction_id": prediction_id,
            "crop": crop_name,
            "confidence": confidence
        })

    except Exception as e:
        print(f"[ERROR] Prediction error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ---------------------------------------------------------------------------
# Admin Panel routes
# ---------------------------------------------------------------------------

@app.route("/admin", methods=["GET"])
def admin_login():
    if "user_id" in session and session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_login.html")


@app.route("/admin/dashboard", methods=["GET"])
@admin_required
def admin_dashboard():
    stats = db.get_system_stats()
    users = db.get_all_users()
    predictions = db.get_all_predictions()
    
    # Append model information
    stats['model_loaded'] = crop_model is not None
    stats['model_type'] = type(crop_model).__name__ if crop_model else "Not Loaded"
    stats['api_key'] = API_KEY
    
    return render_template("admin_dashboard.html", stats=stats, users=users, predictions=predictions)


@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    db.delete_user(user_id)
    flash(f"User account (ID: {user_id}) deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/clear_predictions", methods=["POST"])
@admin_required
def admin_clear_predictions():
    db.clear_all_predictions()
    flash("All crop prediction logs successfully cleared.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/retrain", methods=["POST"])
@admin_required
def admin_retrain():
    try:
        # Run main.py training
        subprocess.run([sys.executable, str(BASE_DIR / "main.py")], cwd=str(BASE_DIR), check=True)
        
        # Reload global model
        global crop_model
        with open(MODEL_PATH, "rb") as f:
            crop_model = pickle.load(f)
            
        flash("Machine Learning model retrained and reloaded successfully!", "success")
    except Exception as e:
        flash(f"Error retraining model: {str(e)}", "error")
        
    return redirect(url_for("admin_dashboard"))

# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        use_reloader=False
    )