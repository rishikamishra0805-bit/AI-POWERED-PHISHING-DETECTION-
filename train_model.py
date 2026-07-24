# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import time
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("🤖 AI POWERED PHISHING DETECTION - MODEL TRAINING")
print("=" * 80)

def load_dataset():
    """Load and prepare dataset"""
    try:
        # Try to load from dataset folder
        dataset_paths = [
            "DATASET/dataset.csv",
            "dataset.csv",
            "data/dataset.csv"
        ]
        
        for path in dataset_paths:
            if os.path.exists(path):
                print(f"📂 Loading dataset from: {path}")
                df = pd.read_csv(path)
                print(f"✅ Dataset loaded successfully!")
                print(f"📊 Dataset shape: {df.shape}")
                return df
        
        # If no dataset found, create sample data
        print("⚠️ Dataset not found! Creating sample data for demonstration...")
        return create_sample_dataset()
        
    except Exception as e:
        print(f"❌ Error loading dataset: {str(e)}")
        return None

def create_sample_dataset():
    """Create sample dataset for demonstration"""
    np.random.seed(42)
    n_samples = 2000
    
    # Create features
    X = np.random.randn(n_samples, 30)
    
    # Create labels (0 = safe, 1 = phishing)
    y = np.zeros(n_samples)
    
    # Add patterns for phishing URLs
    for i in range(n_samples):
        # Phishing pattern: long URLs, no HTTPS, many special characters
        if (X[i, 0] > 1.5 or X[i, 7] > 2.0 or X[i, 6] > 1.5):
            y[i] = 1
        elif (X[i, 1] < -1.0 and X[i, 0] > 0.5):
            y[i] = 1
        elif (X[i, 2] < -1.5 and X[i, 3] > 1.0):
            y[i] = 1
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(30)])
    df['label'] = y
    
    print(f"✅ Sample dataset created with {n_samples} samples")
    print(f"📊 Safe URLs: {sum(y == 0)}")
    print(f"📊 Phishing URLs: {sum(y == 1)}")
    
    return df

def train_model(df):
    """Train the Random Forest model"""
    print("\n" + "=" * 80)
    print("🔄 TRAINING MODEL")
    print("=" * 80)
    
    # Separate features and labels
    X = df.drop('label', axis=1)
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"📊 Training set: {X_train.shape[0]} samples")
    print(f"📊 Testing set: {X_test.shape[0]} samples")
    
    # Initialize Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    print("\n🔄 Training Random Forest...")
    start_time = time.time()
    
    # Train model
    model.fit(X_train, y_train)
    
    training_time = time.time() - start_time
    print(f"✅ Training completed in {training_time:.2f} seconds")
    
    # Evaluate model
    print("\n📊 EVALUATING MODEL")
    print("-" * 40)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {accuracy * 100:.2f}%")
    
    # Classification report
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\n📊 Confusion Matrix:")
    print(f"   Safe      Phishing")
    print(f"Safe: {cm[0,0]}      {cm[0,1]}")
    print(f"Phishing: {cm[1,0]}      {cm[1,1]}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"\n📊 Cross-validation scores: {cv_scores}")
    print(f"📊 Average CV score: {cv_scores.mean() * 100:.2f}%")
    
    # Feature Importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n📊 Top 10 Most Important Features:")
    print(feature_importance.head(10).to_string(index=False))
    
    return model, accuracy

def save_model(model, accuracy):
    """Save the trained model"""
    print("\n" + "=" * 80)
    print("💾 SAVING MODEL")
    print("=" * 80)
    
    # Create model directory
    os.makedirs('MODEL', exist_ok=True)
    os.makedirs('model', exist_ok=True)
    
    # Save model
    model_paths = [
        "MODEL/phishing_model.pkl",
        "model/phishing_model.pkl",
        "phishing_model.pkl"
    ]
    
    for path in model_paths:
        try:
            joblib.dump(model, path)
            print(f"✅ Model saved to: {path}")
        except Exception as e:
            print(f"❌ Error saving to {path}: {str(e)}")
    
    # Save model metadata
    metadata = {
        'accuracy': accuracy,
        'model_type': 'RandomForestClassifier',
        'features': 30,
        'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0.0'
    }
    
    try:
        import json
        with open('MODEL/model_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        print("✅ Model metadata saved")
    except:
        pass
    
    print("\n✅ Model saving complete!")

def main():
    """Main training pipeline"""
    print("\n🚀 Starting Model Training Pipeline...")
    print("=" * 80)
    
    # Step 1: Load dataset
    df = load_dataset()
    if df is None:
        print("❌ Failed to load dataset. Exiting...")
        return
    
    # Step 2: Train model
    model, accuracy = train_model(df)
    
    # Step 3: Save model
    save_model(model, accuracy)
    
    print("\n" + "=" * 80)
    print("🎉 MODEL TRAINING COMPLETE!")
    print("=" * 80)
    print(f"📊 Final Accuracy: {accuracy * 100:.2f}%")
    print("\n🚀 You can now run:")
    print("   streamlit run streamlit_app.py")
    print("   or")
    print("   python app.py")
    print("=" * 80)

if __name__ == "__main__":
    main()
