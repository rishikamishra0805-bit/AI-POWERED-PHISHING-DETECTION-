# AI Powered Phishing Detection Using Machine Learning

## Project Overview
AI Powered Phishing Detection is a cybersecurity project that uses Machine Learning techniques to identify whether a website URL is safe or potentially a phishing website.

The system analyzes URL features and uses a Random Forest Classifier to classify websites. A Flask-based web application provides an easy interface where users can enter a URL and get a prediction result.

## Features
- AI-based phishing URL detection
- Machine Learning classification using Random Forest
- URL feature extraction
- Web interface using Flask
- Safe and Phishing website prediction

## Technologies Used
- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Joblib
- HTML/CSS

## Project Structure

AI-PHISHING-DETECTION/
dataset/              - Dataset files
model/                - Trained ML model
templates/            - Web pages
screenshots/          - Project screenshots
report/               - Project report
app.py                - Flask application
feature_extraction.py - URL feature extraction

## Machine Learning Model
Algorithm Used:
- Random Forest Classifier

Model Accuracy:
- 96.74%

## How to Run

1. Install required libraries:
pip install flask pandas numpy scikit-learn joblib

2. Run the application:
python app.py

3. Open browser:
http://127.0.0.1:5000⁠�

4. Enter a website URL and check the prediction.

## Result
The system classifies URLs into:
- Safe Website
- Phishing Website

## Future Scope
- Real-time browser extension
- Advanced phishing intelligence integration
- Deep Learning based detection
- Real-time threat monitoring

## Author
Cyber Security Project