# streamlit_app.py
import streamlit as st
import joblib
import re
from urllib.parse import urlparse
import os
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="AI Phishing Detection",
    page_icon="🔒",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
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
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

# Feature extraction function - 30 features ONLY
def extract_features(url):
    """Extract 30 features from URL"""
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

# Load model
@st.cache_resource
def load_model():
    """Load the phishing detection model"""
    try:
        # Check multiple paths
        model_paths = [
            "MODEL/phishing_model.pkl",
            "model/phishing_model.pkl",
            "phishing_model.pkl"
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                model = joblib.load(path)
                return model, path
        
        # If no model found
        st.error("❌ Model file not found!")
        st.info("""
        **Please ensure your model file is at:**
        - `MODEL/phishing_model.pkl`
        """)
        
        # Debug info
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

# Suspicious keywords
SUSPICIOUS_WORDS = [
    "login", "verify", "update", "secure", 
    "account", "password", "bank", "confirm"
]

def check_suspicious_keywords(url):
    """Check if URL contains suspicious keywords"""
    if not url:
        return False, []
    found = [word for word in SUSPICIOUS_WORDS if word in url.lower()]
    return len(found) > 0, found

# Title
st.title("🔒 AI Powered Phishing Detection")
st.markdown("""
    <div class="info-box">
    🛡️ Enter a URL to check if it's <b>Safe</b> or <b>Phishing</b>.
    </div>
""", unsafe_allow_html=True)

# Load model
if not st.session_state.model_loaded:
    with st.spinner("🔄 Loading AI Model..."):
        model, model_path = load_model()
        if model is not None:
            st.session_state.model = model
            st.session_state.model_loaded = True
            st.success(f"✅ Model loaded successfully!")

if not st.session_state.model_loaded:
    st.stop()

# URL Input
url = st.text_input(
    "Enter Website URL",
    placeholder="https://example.com",
    key="url_input"
)

# Quick test buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 Google", use_container_width=True):
        st.session_state.url_input = "https://www.google.com"
        st.rerun()
with col2:
    if st.button("🟡 Suspicious", use_container_width=True):
        st.session_state.url_input = "http://login-secure-verify.com"
        st.rerun()
with col3:
    if st.button("🔴 Phishing", use_container_width=True):
        st.session_state.url_input = "http://192.168.1.1/account"
        st.rerun()

# Check URL button
if st.button("🔍 Check URL", type="primary", use_container_width=True):
    current_url = st.session_state.get("url_input", "")
    
    if not current_url:
        st.warning("⚠️ Please enter a URL")
    else:
        # Normalize URL
        url_to_check = current_url.strip()
        if not url_to_check.startswith(("http://", "https://")):
            url_to_check = "http://" + url_to_check
        
        with st.spinner("🔍 Analyzing..."):
            try:
                # Extract features
                features = extract_features(url_to_check)
                
                # Predict
                prediction = st.session_state.model.predict([features])[0]
                
                # Check suspicious keywords
                has_suspicious, suspicious_found = check_suspicious_keywords(url_to_check)
                
                # Determine result
                if has_suspicious or prediction == -1:
                    result = "⚠️ Phishing Website"
                    result_class = "phishing"
                    icon = "🚫"
                else:
                    result = "✅ Safe Website"
                    result_class = "safe"
                    icon = "🛡️"
                
                # Display result
                st.markdown(f"""
                    <div class="result-box {result_class}">
                        {icon} {result}
                    </div>
                """, unsafe_allow_html=True)
                
                # Detailed analysis
                with st.expander("📊 Analysis Details", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("URL Length", len(url_to_check))
                        st.metric("HTTPS", "✅ Yes" if url_to_check.startswith("https://") else "❌ No")
                        st.metric("Suspicious Words", "⚠️ Found" if has_suspicious else "✅ None")
                        if has_suspicious:
                            st.write(f"Found: {', '.join(suspicious_found)}")
                    
                    with col2:
                        st.metric("Dots", url_to_check.count("."))
                        has_ip = bool(re.match(r"^(http://|https://)?\d+\.\d+\.\d+\.\d+", url_to_check))
                        st.metric("IP Address", "⚠️ Yes" if has_ip else "✅ No")
                        st.metric("Prediction", "Phishing" if prediction == -1 else "Safe")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("📊 Model Info")
    st.info("""
    **Algorithm:** Random Forest  
    **Accuracy:** 96.74%  
    **Features:** 30
    """)
    
    st.header("⚠️ Safety Tips")
    st.markdown("""
    1. 🔍 Check URL carefully
    2. 🔒 Look for HTTPS
    3. 🚫 Don't enter personal info
    4. 📱 Be cautious of shortened URLs
    """)
    
    st.header("📝 Test URLs")
    with st.expander("✅ Safe"):
        st.code("https://www.google.com")
        st.code("https://www.github.com")
    with st.expander("⚠️ Phishing"):
        st.code("http://login-secure-verify.com")
        st.code("http://192.168.1.1/account")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#666; font-size:0.9rem;">
    Built with ❤️ using Streamlit | AI-Powered Phishing Detection
    </div>
""", unsafe_allow_html=True)
