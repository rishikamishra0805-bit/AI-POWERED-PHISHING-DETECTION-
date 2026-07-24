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
    
    # 1. URL length
    features[0] = len(url)
    
    # 2. HTTPS
    features[1] = 1 if parsed.scheme == "https" else -1
    
    # 3. @ symbol
    features[2] = -1 if "@" in url else 1
    
    # 4. Number of dots
    features[3] = url.count(".")
    
    # 5. URL has IP address
    if re.match(r"^(http://|https://)?\d+\.\d+\.\d+\.\d+", url):
        features[4] = -1
    else:
        features[4] = 1
    
    # 6. Hyphen in domain
    features[5] = -1 if "-" in parsed.netloc else 1
    
    # 7. Number of digits
    features[6] = sum(c.isdigit() for c in url)
    
    # 8. Special characters
    features[7] = sum(not c.isalnum() for c in url)
    
    # 9-30. Default features
    for i in range(8, 30):
        features[i] = 1
    
    return features

def test_model():
    """Test the trained model"""
    print("=" * 80)
    print("🧪 AI POWERED PHISHING DETECTION - MODEL TESTING")
    print("=" * 80)
    
    # Load model
    try:
        model = joblib.load("MODEL/phishing_model.pkl")
        print("✅ Model loaded successfully from MODEL/phishing_model.pkl!")
    except:
        try:
            model = joblib.load("phishing_model.pkl")
            print("✅ Model loaded successfully from root!")
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            print("\n💡 Please run train_model.py first.")
            return
    
    # Test URLs
    test_urls = [
        ("https://www.google.com", "Safe"),
        ("https://www.github.com", "Safe"),
        ("https://www.python.org", "Safe"),
        ("https://www.stackoverflow.com", "Safe"),
        ("http://login-secure-verify.com", "Phishing"),
        ("http://192.168.1.1/account", "Phishing"),
        ("https://paypal-verify-secure.com", "Phishing"),
        ("http://secure-login-verify.net", "Phishing"),
    ]
    
    print("\n📊 TESTING URLS")
    print("-" * 80)
    print(f"{'URL':<40} {'Expected':<15} {'Predicted':<15} {'Result':<15}")
    print("-" * 80)
    
    correct = 0
    total = len(test_urls)
    
    for url, expected in test_urls:
        features = extract_features(url)
        start_time = time.time()
        prediction = model.predict([features])[0]
        prediction_time = (time.time() - start_time) * 1000
        
        predicted = "Phishing" if prediction == -1 else "Safe"
        
        result = "✅ PASS" if predicted == expected else "❌ FAIL"
        if predicted == expected:
            correct += 1
        
        print(f"{url[:38]:<40} {expected:<15} {predicted:<15} {result:<15}")
        print(f"  ⏱️ Time: {prediction_time:.2f}ms")
    
    print("-" * 80)
    accuracy = (correct / total) * 100
    print(f"\n📊 Test Accuracy: {accuracy:.2f}% ({correct}/{total})")
    print("=" * 80)

if __name__ == "__main__":
    test_model()
