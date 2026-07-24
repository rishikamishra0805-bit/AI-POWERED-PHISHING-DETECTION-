# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("🤖 AI POWERED PHISHING DETECTION - MODEL TRAINING")
print("=" * 80)

def create_sample_dataset():
    """Create sample dataset for demonstration"""
    np.random.seed(42)
    n_samples = 2000
    
    X = np.random.randn(n_samples, 30)
    y = np.zeros(n_samples)
    
    # Add phishing patterns
    for i in range(n_samples):
        if (X[i, 0] > 1.5 or X[i, 7] > 2.0 or X[i, 6] > 1.5):
            y[i] = 1
        elif (X[i, 1] < -1.0 and X[i, 0] > 0.5):
            y[i] = 1
    
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(30)])
    df['label'] = y
    
    print(f"✅ Sample dataset created with {n_samples} samples")
    print(f"📊 Safe: {sum(y == 0)}, Phishing: {sum(y == 1)}")
    return df

def main():
    # Create dataset
    df = create_sample_dataset()
    
    # Split data
    X = df.drop('label', axis=1)
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    print("\n🔄 Training Random Forest...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {accuracy * 100:.2f}%")
    
    # Save model
    os.makedirs('MODEL', exist_ok=True)
    joblib.dump(model, 'MODEL/phishing_model.pkl')
    print("✅ Model saved to MODEL/phishing_model.pkl")
    
    print("\n🎉 Training complete!")

if __name__ == "__main__":
    main()
