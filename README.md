🌱 OptiCrop - Smart Agricultural Production Optimization Engine
OptiCrop is a Machine Learning-based web application developed using Python, Flask, HTML, CSS, and JavaScript. It helps farmers identify the most suitable crop based on soil nutrients and environmental conditions. The system predicts the best crop using a trained Machine Learning model and provides an easy-to-use web interface.

📌 Features
🌾 Smart Crop Recommendation
🤖 Machine Learning Prediction Model
🌡️ Soil and Environmental Parameter Analysis
📊 Interactive Web Interface
🔐 User Sign Up and Sign In Pages
📄 About Page
🌿 Crop Prediction Form
📈 Result Page with Prediction Output
📱 Responsive User Interface
🛠 Technologies Used
Frontend
HTML5
CSS3
JavaScript
Backend
Python
Flask
Machine Learning
Scikit-learn
Pandas
NumPy
Pickle
📂 Project Structure
OptiCrop/
│
├── app.py
├── model.py
├── model.pkl
├── Crop_recommendation.csv
├── requirements.txt
│
├── templates/
│   ├── home.html
│   ├── about.html
│   ├── base.html
│   ├── findyourcrop.html
│   ├── result.html
│   ├── signin.html
│   └── signup.html
│
├── static/
│   ├── css/
│   │     └── style.css
│   │
│   ├── js/
│   │     └── script.js
│   │
│   └── images/
│         ├── home.jpg
│         ├── about.jpg
│         ├── findyourcrop.jpeg
│         └── result.jpg
│
└── README.md
⚙ Installation
Clone the repository:

git clone https://github.com/YOUR_USERNAME/OptiCrop.git
Move into the project folder:

cd OptiCrop
Install the required packages:

pip install -r requirements.txt
Run the Flask application:

python app.py
Open your browser and visit:

http://127.0.0.1:5000
🌱 Input Parameters
The prediction model uses the following parameters:

Nitrogen (N)
Phosphorus (P)
Potassium (K)
Temperature
Humidity
pH Value
Rainfall
🎯 Output
The application predicts the most suitable crop for the given environmental and soil conditions.

Example:

Recommended Crop:
Rice
📷 Screens
Home Page
About Page
Find Your Crop
Result Page
Sign In
Sign Up
🚀 Future Enhancements
Weather API Integration
Fertilizer Recommendation
Disease Prediction
Multi-language Support
Farmer Dashboard
Database Authentication
Cloud Deployment
👩‍💻 Developed By
Lakshmi Priya, Durga Krishna Sai, Vasanthi, Deva Sahayam 

B.Tech – Computer Science and Engineering (Artificial Intelligence & Machine Learning)

Jawaharlal Nehru Technological University Kakinada

📜 License
This project is developed for educational and academic purposes.image
