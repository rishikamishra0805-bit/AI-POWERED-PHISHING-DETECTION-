# test_model.py
import joblib
import re
from urllib.parse import urlparse
import time
import os

def extract_features(url):
    """Extract 30 features from URL for testing"""
    features = [0] * 30
    parsed = urlparse(url)
    
    features[0] = len(url)
    features[1] = 1 if parsed.scheme == "https" else -1
    features[2] = -1 if "@" in url else 1
    features[3] = url.count(".")
    
    if re.match(r"^(http://|https://)?\d+\.\d+\.\d+\.\d+", url):
        features[4] = -1
    else:
        features[4] = 1
    
    features[5] = -1 if "-" in parsed.netloc else 1
    features[6] = sum(c.isdigit() for c in url)
    features[7] = sum(not c.isalnum() for c in url)
    
    for i in range(8, 30):
        features[i] = 1
    
    return features

def test_model():
    """Test the trained model"""
    print("=" * 80)
    print("🧪 AI POWERED PHISHING DETECTION - MODEL TESTING")
    print("=" * 80)
    
    # Load model from MODEL folder
    try:
        model = joblib.load("MODEL/phishing_model.pkl")
        print("✅ Model loaded successfully from MODEL/phishing_model.pkl!")
    except FileNotFoundError:
        try:
            model = joblib.load("phishing_model.pkl")
            print("✅ Model loaded successfully from root!")
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            print("\n💡 Please run train_model.py first to create the model.")
            return
    
    # Test URLs
    test_urls = [
        # Safe URLs
        ("https://www.google.com", "Safe"),
        ("https://www.github.com", "Safe"),
        ("https://www.python.org", "Safe"),
        ("https://www.stackoverflow.com", "Safe"),
        ("https://www.wikipedia.org", "Safe"),
        ("https://www.microsoft.com", "Safe"),
        
        # Phishing URLs
        ("http://login-secure-verify.com", "Phishing"),
        ("http://192.168.1.1/account", "Phishing"),
        ("https://paypal-verify-secure.com", "Phishing"),
        ("http://secure-login-verify.net", "Phishing"),
        ("http://bank-account-update.com", "Phishing"),
        ("https://login-verify-paypal.com", "Phishing"),
    ]
    
    print("\n📊 TESTING URLS")
    print("-" * 80)
    print(f"{'URL':<40} {'Expected':<15} {'Predicted':<15} {'Result':<15}")
    print("-" * 80)
    
    correct = 0
    total = len(test_urls)
    
    for url, expected in test_urls:
        # Extract features
        features = extract_features(url)
        
        # Predict
        start_time = time.time()
        prediction = model.predict([features])[0]
        prediction_time = (time.time() - start_time) * 1000
        
        # Map prediction
        predicted = "Phishing" if prediction == -1 else "Safe"
        
        # Check result
        result = "✅ PASS" if predicted == expected else "❌ FAIL"
        if predicted == expected:
            correct += 1
        
        # Print result
        print(f"{url[:38]:<40} {expected:<15} {predicted:<15} {result:<15}")
        print(f"  ⏱️ Prediction time: {prediction_time:.2f}ms")
    
    print("-" * 80)
    accuracy = (correct / total) * 100
    print(f"\n📊 Test Accuracy: {accuracy:.2f}% ({correct}/{total})")
    
    # Additional test with suspicious keywords
    print("\n🔍 SUSPICIOUS KEYWORD TEST")
    print("-" * 80)
    suspicious_words = ["login", "verify", "update", "secure", "account", "password", "bank", "confirm"]
    
    for word in suspicious_words:
        test_url = f"http://{word}-test.com"
        features = extract_features(test_url)
        prediction = model.predict([features])[0]
        result = "Phishing" if prediction == -1 else "Safe"
        print(f"  {word:<15} → {result}")
    
    print("\n" + "=" * 80)
    print("🎉 TESTING COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    test_model()
