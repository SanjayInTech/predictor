import streamlit as st
import pickle
import os

# Set page config
st.set_page_config(page_title="Dynamic Price Predictor", layout="centered", page_icon="📈")

# Custom CSS for Streamlit to match previous Flask UI
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Background and global font */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Centered translucent card */
    .block-container {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 48px 40px !important;
        max-width: 480px !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
        margin-top: 5vh;
        margin-bottom: 5vh;
        color: white;
    }

    /* Titles and text */
    h1, h2, h3, p, label, .stMarkdown p {
        color: white !important;
    }
    
    h1 {
        font-size: 26px !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        text-align: center;
        padding-bottom: 0;
    }

    .subtitle {
        text-align: center;
        font-size: 14px;
        color: rgba(255,255,255,0.5) !important;
        margin-bottom: 20px;
        margin-top: -10px;
    }

    /* Input styling overrides */
    div[data-baseweb="select"] > div, 
    input[type="number"] {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
    }

    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:focus-within,
    input[type="number"]:focus {
        border-color: rgba(130, 100, 255, 0.7) !important;
        background: rgba(130, 100, 255, 0.12) !important;
    }

    /* Predict Button */
    .stButton > button {
        width: 100% !important;
        padding: 15px !important;
        background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
        letter-spacing: 0.3px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.5) !important;
    }
    
    /* Result Box CSS */
    .result-box {
        margin-top: 28px;
        padding: 20px 24px;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.25), rgba(168, 85, 247, 0.15));
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 14px;
        text-align: center;
        animation: fadeIn 0.5s ease;
    }
    .result-label { font-size: 12px; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .result-value { font-size: 36px; font-weight: 700; color: #c084fc; letter-spacing: -1px; margin: 0; padding: 0;}
    .result-unit { font-size: 14px; color: rgba(255,255,255,0.5); margin-top: 4px; }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    
    /* Hide top bar & footer for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hint text */
    .st-emotion-cache-1jig1md p { 
        font-size: 11px;
        color: rgba(255,255,255,0.35) !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Header Section
st.markdown("<div style='text-align: center; font-size: 48px;'>📈</div>", unsafe_allow_html=True)
st.markdown("<h1>Dynamic Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-powered pricing based on market conditions</p>", unsafe_allow_html=True)

# Load Model
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    with open(model_path, 'rb') as file:
        return pickle.load(file)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Input fields
demand_options = {1: "1 = Low | 2 = Medium | 3 = High"} # Small hack to show hint
st.markdown("<label>Demand Level</label>", unsafe_allow_html=True)
demand = st.selectbox("Demand Level", options=[1, 2, 3], format_func=lambda x: {1: "1 (Low)", 2: "2 (Medium)", 3: "3 (High)"}[x], label_visibility="collapsed")
st.markdown("<p style='font-size: 11px; color: rgba(255,255,255,0.35) !important; margin-top: -10px;'>1 = Low &nbsp;|&nbsp; 2 = Medium &nbsp;|&nbsp; 3 = High</p>", unsafe_allow_html=True)

st.markdown("<label>Competitor Price (₹)</label>", unsafe_allow_html=True)
competitor = st.number_input("Competitor Price", min_value=0.0, value=0.0, step=1.0, format="%.2f", label_visibility="collapsed")
st.markdown("<p style='font-size: 11px; color: rgba(255,255,255,0.35) !important; margin-top: -10px;'>Enter the current competitor's price in rupees</p>", unsafe_allow_html=True)

st.markdown("<label>Season</label>", unsafe_allow_html=True)
season = st.selectbox("Season", options=[0, 1], format_func=lambda x: {0: "🌤️ Off-Season", 1: "🔥 Peak Season"}[x], label_visibility="collapsed")

if st.button("⚡ Predict Price"):
    try:
        # Perform prediction
        prediction = model.predict([[float(demand), float(competitor), float(season)]])
        result = round(float(prediction[0]), 2)
        
        st.markdown(f"""
        <div style="height: 1px; background: rgba(255,255,255,0.08); margin: 28px 0;"></div>
        <div class="result-box">
            <p class="result-label">Predicted Price</p>
            <p class="result-value">₹{result}</p>
            <p class="result-unit">Recommended market price</p>
        </div>
        """, unsafe_allow_html=True)
        
    except ValueError:
        st.markdown("""
        <div style="margin-top: 20px; padding: 14px 18px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; color: #fca5a5; font-size: 14px; text-align: center;">
            ⚠️ Please enter valid numeric values in all fields.
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
         st.markdown(f"""
        <div style="margin-top: 20px; padding: 14px 18px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; color: #fca5a5; font-size: 14px; text-align: center;">
            ⚠️ An unexpected error occurred: {str(e)}
        </div>
        """, unsafe_allow_html=True)
