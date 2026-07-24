# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 50)
print("🤖 TRAINING PHISHING DETECTION MODEL")
print("=" * 50)

try:
    # Try to load dataset
    df = pd.read_csv('DATASET/dataset.csv')
    print(f"✅ Dataset loaded: {len(df)} rows")
    
    # Assuming last column is label
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
except:
    print("⚠️ Dataset not found! Creating sample data...")
    np.random.seed(42)
    n_samples = 2000
    
    # Create 30 features
    X = np.random.randn(n_samples, 30)
    
    # Create labels with some pattern
    y = np.zeros(n_samples)
    for i in range(n_samples):
        if X[i, 0] > 0.5 or X[i, 7] > 1.0:
            y[i] = 1
        elif X[i, 1] < -0.5 and X[i, 2] > 0.5:
            y[i] = 1
    
    print(f"✅ Sample data created: {n_samples} rows")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("🔄 Training Random Forest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy * 100:.2f}%")

# Save model
os.makedirs('MODEL', exist_ok=True)
joblib.dump(model, 'MODEL/phishing_model.pkl')
print("✅ Model saved to MODEL/phishing_model.pkl!")

print("=" * 50)
print("🎉 Training complete! Run: streamlit run streamlit_app.py")
