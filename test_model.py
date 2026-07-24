# test_model.py
import joblib
import re
from urllib.parse import urlparse

def extract_features(url):
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
    print("=" * 50)
    print("🧪 TESTING PHISHING DETECTION MODEL")
    print("=" * 50)
    
    try:
        model = joblib.load("MODEL/phishing_model.pkl")
        print("✅ Model loaded!")
    except:
        print("❌ Model not found! Run train_model.py first.")
        return
    
    test_urls = [
        ("https://www.google.com", "Safe"),
        ("https://www.github.com", "Safe"),
        ("http://login-secure-verify.com", "Phishing"),
        ("http://192.168.1.1/account", "Phishing"),
    ]
    
    correct = 0
    for url, expected in test_urls:
        features = extract_features(url)
        prediction = model.predict([features])[0]
        predicted = "Phishing" if prediction == -1 else "Safe"
        result = "✅ PASS" if predicted == expected else "❌ FAIL"
        if predicted == expected:
            correct += 1
        print(f"{url[:30]:<30} {expected:<10} {predicted:<10} {result}")
    
    print(f"\n📊 Accuracy: {correct/len(test_urls)*100:.2f}%")

if __name__ == "__main__":
    test_model()
