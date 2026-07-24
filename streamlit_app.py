# streamlit_app.py
import streamlit as st
import joblib
import re
from urllib.parse import urlparse
import os
import sys

# Page configuration
st.set_page_config(
    page_title="AI Phishing Detection",
    page_icon="🔒",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .safe {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .phishing {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 10px 0;
    }
    .feature-item {
        background: #f8f9fa;
        padding: 8px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for model
if 'model' not in st.session_state:
    st.session_state.model = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

# Function to find model file
def find_model_file():
    """Try to find the model file in various locations"""
    possible_paths = [
        "model/phishing_model.pkl",
        "phishing_model.pkl",
        "./model/phishing_model.pkl",
        "../model/phishing_model.pkl",
        "MODEL/phishing_model.pkl",
        "./MODEL/phishing_model.pkl"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

# Load the model with better error handling
@st.cache_resource
def load_model():
    """Load the phishing detection model"""
    try:
        # Try to find the model file
        model_path = find_model_file()
        
        if model_path is None:
            st.error("""
            ❌ **Model file not found!**
            
            Please ensure your model file is in one of these locations:
            - `model/phishing_model.pkl`
            - `phishing_model.pkl`
            - `MODEL/phishing_model.pkl`
            
            **For Streamlit Cloud deployment:**
            1. Make sure you've uploaded the model file to your repository
            2. Check that the file path in your code matches the actual location
            3. Ensure the file is not ignored by .gitignore
            """)
            return None
        
        # Load the model
        model = joblib.load(model_path)
        st.success(f"✅ Model loaded successfully from: {model_path}")
        return model
        
    except FileNotFoundError as e:
        st.error(f"❌ Model file not found: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

# Import feature extraction - with fallback
try:
    from feature_extraction import extract_features
except ImportError:
    st.error("""
    ❌ **feature_extraction.py not found!**
    
    Please ensure you have the `feature_extraction.py` file in your project directory.
    This file contains the URL feature extraction functions needed for prediction.
    """)
    st.stop()

# Title and description
st.title("🔒 AI Powered Phishing Detection")
st.markdown("""
    <div class="info-box">
    🛡️ Enter a URL below to check if it's a <b>Safe Website</b> or a <b>Phishing Website</b>.
    Our AI model analyzes URL patterns and features to detect potential phishing attempts.
    </div>
""", unsafe_allow_html=True)

# Check if model is loaded on startup
if not st.session_state.model_loaded:
    with st.spinner("🔄 Loading AI Model..."):
        model = load_model()
        if model is not None:
            st.session_state.model = model
            st.session_state.model_loaded = True
            st.success("✅ Model loaded successfully!")
        else:
            st.warning("⚠️ Could not load model. Please check the model file.")

# Input section
url = st.text_input(
    "🌐 Enter Website URL",
    placeholder="https://example.com",
    help="Enter the full URL including http:// or https://"
)

# Add example URLs as quick links
st.markdown("### 📝 Quick Test URLs")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔵 Google (Safe)", use_container_width=True):
        url = "https://www.google.com"

with col2:
    if st.button("🟡 Suspicious URL", use_container_width=True):
        url = "http://login-secure-verify.com"

with col3:
    if st.button("🔴 IP Address URL", use_container_width=True):
        url = "http://192.168.1.1/account"

# Suspicious keywords list (from your app.py)
SUSPICIOUS_WORDS = [
    "login", "verify", "update", "secure", 
    "account", "password", "bank", "confirm"
]

def check_suspicious_keywords(url):
    """Check if URL contains suspicious keywords"""
    if not url:
        return False, []
    suspicious_found = [word for word in SUSPICIOUS_WORDS if word in url.lower()]
    return len(suspicious_found) > 0, suspicious_found

# Prediction button
if st.button("🔍 Check URL", type="primary", use_container_width=True):
    if not url:
        st.warning("⚠️ Please enter a URL")
    else:
        # Add http:// if no scheme is provided
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        # Check if model is loaded
        if not st.session_state.model_loaded:
            st.error("❌ Model not loaded. Please check the model file and try again.")
        else:
            with st.spinner("🔍 Analyzing URL..."):
                try:
                    # Extract features
                    features = extract_features(url)
                    
                    # Make prediction
                    prediction = st.session_state.model.predict([features])[0]
                    
                    # Check for suspicious keywords
                    has_suspicious, suspicious_found = check_suspicious_keywords(url)
                    
                    # Determine result
                    if has_suspicious or prediction == -1:
                        result = "⚠️ Phishing Website"
                        result_class = "phishing"
                        icon = "🚫"
                        detail = "This URL contains suspicious keywords or patterns associated with phishing websites."
                    else:
                        result = "✅ Safe Website"
                        result_class = "safe"
                        icon = "🛡️"
                        detail = "This URL appears to be safe based on our analysis."
                    
                    # Display result
                    st.markdown(f"""
                        <div class="result-box {result_class}">
                            {icon} {result}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display detailed analysis
                    with st.expander("📊 Detailed Analysis", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        # Parse URL for additional info
                        parsed = urlparse(url)
                        domain = parsed.netloc or parsed.path
                        
                        with col1:
                            st.metric("URL Length", len(url))
                            st.metric("Has HTTPS", "✅ Yes" if url.startswith("https://") else "❌ No")
                            st.metric("Contains Suspicious Words", "⚠️ Yes" if has_suspicious else "✅ No")
                            if has_suspicious:
                                st.write(f"**Found:** {', '.join(suspicious_found)}")
                        
                        with col2:
                            st.metric("Number of Dots", url.count("."))
                            has_ip = bool(re.match(r"^(http://|https://)?\d+\.\d+\.\d+\.\d+", url))
                            st.metric("Has IP Address", "⚠️ Yes" if has_ip else "✅ No")
                            st.metric("Model Prediction", "⚠️ Phishing" if prediction == -1 else "✅ Safe")
                        
                        # Feature breakdown
                        st.markdown("#### 📋 Feature Breakdown")
                        feature_names = [
                            "URL Length", "HTTPS", "@ Symbol", "Number of Dots", 
                            "Has IP", "Hyphen in Domain", "Number of Digits", 
                            "Special Characters"
                        ]
                        feature_values = features[:8]
                        
                        # Create a nice grid of features
                        cols = st.columns(4)
                        for i, (name, value) in enumerate(zip(feature_names, feature_values)):
                            col = cols[i % 4]
                            with col:
                                st.markdown(f"""
                                <div class="feature-item">
                                    <small>{name}</small><br>
                                    <strong>{value}</strong>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    with st.expander("ℹ️ Why was this result?"):
                        if has_suspicious:
                            st.warning(f"**Found suspicious keywords:** {', '.join(suspicious_found)}")
                            st.write("These keywords are commonly used in phishing URLs to trick users.")
                        
                        if prediction == -1:
                            st.warning("**The AI model identified this URL as potentially malicious based on its structure and features.")
                        else:
                            st.success("**The AI model did not detect any malicious patterns in this URL.")
                        
                        st.info("""
                        **Note:** This is an AI-based prediction and should not be considered 100% accurate. 
                        Always exercise caution when visiting unknown websites and never enter personal 
                        information on suspicious sites.
                        """)
                
                except Exception as e:
                    st.error(f"❌ Error analyzing URL: {str(e)}")
                    st.write("Please make sure you entered a valid URL.")

# Sidebar with comprehensive information
with st.sidebar:
    st.header("📊 Model Information")
    
    if st.session_state.model_loaded:
        st.success("✅ Model is loaded and ready!")
    else:
        st.error("❌ Model not loaded")
        st.info("""
        **Troubleshooting:**
        1. Ensure `phishing_model.pkl` exists in the `model/` folder
        2. Check file permissions
        3. Verify the file is not corrupted
        """)
    
    st.markdown("---")
    
    st.header("🚀 Features")
    st.markdown("""
    - ✅ URL length analysis
    - ✅ HTTPS verification
    - ✅ Suspicious character detection
    - ✅ Domain analysis
    - ✅ Keyword matching
    - ✅ Machine Learning classification
    """)
    
    st.markdown("---")
    
    st.header("⚠️ Safety Tips")
    st.markdown("""
    1. 🔍 Always check the URL carefully
    2. 🔒 Look for HTTPS
    3. 🚫 Never enter personal info on suspicious sites
    4. 📱 Be cautious of shortened URLs
    5. 🔐 Use 2-factor authentication when possible
    """)
    
    st.markdown("---")
    
    st.header("📝 Example URLs")
    with st.expander("Safe Examples"):
        st.code("https://www.google.com")
        st.code("https://www.github.com")
        st.code("https://www.python.org")
    
    with st.expander("Potentially Phishing"):
        st.code("http://login-secure-verify.com")
        st.code("http://192.168.1.1/account")
        st.code("https://paypal-verify-secure.com")
    
    st.markdown("---")
    
    st.header("📈 Model Stats")
    st.metric("Algorithm", "Random Forest")
    st.metric("Accuracy", "96.74%")
    st.metric("Features", "30")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
    Built with ❤️ using Streamlit | AI-Powered Phishing Detection
    </div>
""", unsafe_allow_html=True)
