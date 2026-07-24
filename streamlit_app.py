# streamlit_app.py - Path update
import streamlit as st
import joblib
import re
from urllib.parse import urlparse
import os

# ... (rest of your code)

@st.cache_resource
def load_model():
    """Load the phishing detection model"""
    try:
        # Check for MODEL folder (capital letters) first
        model_paths = [
            "MODEL/phishing_model.pkl",    # Capital letters
            "model/phishing_model.pkl",    # Small letters
            "phishing_model.pkl",          # Root
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                model = joblib.load(path)
                return model, path
        
        # If model not found
        st.error("❌ Model file not found!")
        st.info("""
        **Please ensure your model file is in one of these locations:**
        - `MODEL/phishing_model.pkl` (recommended)
        - `model/phishing_model.pkl`
        - `phishing_model.pkl`
        """)
        
        # Show debug info
        st.write("📁 Files in current directory:")
        for file in os.listdir('.'):
            st.write(f"- {file}")
        
        if os.path.exists('MODEL'):
            st.write("📁 Files in MODEL folder:")
            for file in os.listdir('MODEL'):
                st.write(f"- {file}")
        
        return None, None
        
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None, None

# ... (rest of your code)
