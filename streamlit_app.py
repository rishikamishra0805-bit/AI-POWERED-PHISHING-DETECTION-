# streamlit_app.py
import streamlit as st
import joblib
import re
from urllib.parse import urlparse
import tldextract

# Import your feature extraction function
from feature_extraction import extract_features

# Page configuration
st.set_page_config(
    page_title="AI Phishing Detection",
    page_icon="🔒",
    layout="centered"
)

# Load the model
@st.cache_resource
def load_model():
    try:
        model = joblib.load("model/phishing_model.pkl")
        return model
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Please ensure 'model/phishing_model.pkl' exists.")
        return None

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
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🔒 AI Powered Phishing Detection")
st.markdown("""
    <div class="info-box">
    Enter a URL below to check if it's a <b>Safe Website</b> or a <b>Phishing Website</b>.
    Our AI model analyzes URL patterns and features to detect potential phishing attempts.
    </div>
""", unsafe_allow_html=True)

# Input section
url = st.text_input(
    "Enter Website URL",
    placeholder="https://example.com",
    help="Enter the full URL including http:// or https://"
)

# Suspicious keywords list (from your app.py)
SUSPICIOUS_WORDS = [
    "login", "verify", "update", "secure", 
    "account", "password", "bank", "confirm"
]

def check_suspicious_keywords(url):
    """Check if URL contains suspicious keywords"""
    return any(word in url.lower() for word in SUSPICIOUS_WORDS)

# Prediction button
if st.button("🔍 Check URL", type="primary"):
    if not url:
        st.warning("⚠️ Please enter a URL")
    else:
        # Add http:// if no scheme is provided
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        with st.spinner("Analyzing URL..."):
            try:
                # Load model
                model = load_model()
                
                if model is None:
                    st.error("❌ Model loading failed. Please check the model file.")
                else:
                    # Extract features
                    features = extract_features(url)
                    
                    # Make prediction
                    prediction = model.predict([features])[0]
                    
                    # Check for suspicious keywords
                    suspicious = check_suspicious_keywords(url)
                    
                    # Determine result
                    if suspicious or prediction == -1:
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
                    
                    # Display additional information
                    with st.expander("📊 Analysis Details"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("URL Length", len(url))
                            st.metric("Has HTTPS", "✅ Yes" if url.startswith("https://") else "❌ No")
                            st.metric("Contains Suspicious Words", "⚠️ Yes" if suspicious else "✅ No")
                        
                        with col2:
                            st.metric("Number of Dots", url.count("."))
                            st.metric("Has IP Address", "⚠️ Yes" if re.match(r"^(http://|https://)?\d+\.\d+\.\d+\.\d+", url) else "✅ No")
                            st.metric("Model Prediction", "Phishing" if prediction == -1 else "Safe")
                    
                    with st.expander("ℹ️ Why was this result?"):
                        if suspicious:
                            suspicious_found = [word for word in SUSPICIOUS_WORDS if word in url.lower()]
                            st.write(f"**Found suspicious keywords:** {', '.join(suspicious_found)}")
                            st.write("These keywords are commonly used in phishing URLs.")
                        
                        if prediction == -1:
                            st.write("**The AI model identified this URL as potentially malicious based on its structure and features.")
                        else:
                            st.write("**The AI model did not detect any malicious patterns in this URL.")
                        
                        st.write("\n**Note:** This is an AI-based prediction and should not be considered 100% accurate. Always exercise caution when visiting unknown websites.")
            
            except Exception as e:
                st.error(f"❌ Error analyzing URL: {str(e)}")
                st.write("Please make sure you entered a valid URL.")

# Sidebar information
with st.sidebar:
    st.header("📊 Model Information")
    st.info("""
    **Algorithm:** Random Forest Classifier  
    **Accuracy:** 96.74%  
    **Features Extracted:** 30 URL features  
    """)
    
    st.header("🚀 Features")
    st.markdown("""
    - URL length analysis
    - HTTPS verification
    - Suspicious character detection
    - Domain analysis
    - Keyword matching
    - Machine Learning classification
    """)
    
    st.header("⚠️ Safety Tips")
    st.markdown("""
    1. Always check the URL carefully
    2. Look for HTTPS
    3. Never enter personal info on suspicious sites
    4. Use this tool as an additional safety check
    """)
    
    st.header("📝 Example URLs")
    st.markdown("""
    **Safe:**
    - https://www.google.com
    - https://www.github.com
    
    **Potentially Phishing:**
    - http://login-secure-verify.com
    - http://192.168.1.1/account
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    Built with ❤️ using Streamlit | AI-Powered Phishing Detection
    </div>
""", unsafe_allow_html=True)
