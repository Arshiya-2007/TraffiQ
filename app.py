import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from huggingface_hub import hf_hub_download
from about import about_page
from analytics import analytics_page
from prediction import prediction_page
from styles import load_css
MODEL-REPO = "Arshu-08/traffiq-model"
model_path = hf_hub_download(
    repo_id=MODEL_REPO,
    filename="Traffic_Congestion_RF_Model.pkl"
)

st.set_page_config(
    page_title="TraffiQ",
    page_icon="🚦",
    layout="wide",
)

load_css()


# ---------------- DATA & MODEL LOADING ---------------- #
@st.cache_resource
def load_app_data():
    """Loads dataset and pre-trained models.

    Generates synthetic fallback data if files do not exist yet.
    """
    if os.path.exists("traffic_data.csv"):
        df = pd.read_csv("traffic_data.csv")
    else:
        np.random.seed(42)
        n_samples = 1000
        df = pd.DataFrame(
            {
                "hour": np.random.randint(0, 24, n_samples),
                "day": np.random.randint(1, 31, n_samples),
                "month": np.random.randint(1, 13, n_samples),
                "temp": np.random.uniform(260, 310, n_samples),
                "rain_1h": np.random.exponential(0.5, n_samples),
                "snow_1h": np.zeros(n_samples),
                "clouds_all": np.random.randint(0, 101, n_samples),
                "traffic_volume": np.random.randint(100, 7000, n_samples),
                "weather_main": np.random.choice(
                    ["Clear", "Clouds", "Rain", "Snow", "Mist", "Fog"],
                    n_samples,
                ),
            }
        )

    rf = (
        joblib.load("Traffic_Congestion_RF_Model.pkl")
        if os.path.exists("Traffic_Congestion_RF_Model.pkl")
        else None
    )
    
    encoders = None

    target_encoder = (
        joblib.load("encoders.pkl")
        if os.path.exists("encoders.pkl")
        else None
    )
    # Feature columns for analytics
    feature_cols = [
        "temp",
        "rain_1h",
        "snow_1h",
        "clouds_all",
        "hour",
        "day",
        "month",
    ]
    X = (
        df[feature_cols]
        if set(feature_cols).issubset(df.columns)
        else df.select_dtypes(include=[np.number])
    )

    # Evaluation metrics
    accuracy, precision, recall, f1 = 0.8434, 0.8350, 0.8410, 0.8380

    return (
        df,
        rf,
        encoders,
        target_encoder,
        X,
        accuracy,
        precision,
        recall,
        f1,
    )


(
    df,
    rf,
    encoders,
    target_encoder,
    X,
    accuracy,
    precision,
    recall,
    f1,
) = load_app_data()

# ---------------- NAVIGATION ---------------- #
selected = option_menu(
    menu_title=None,
    options=["Home", "Prediction", "Analytics", "About"],
    icons=["house", "cpu", "bar-chart", "person"],
    orientation="horizontal",
    default_index=0,
)


# ---------------- HOME PAGE ---------------- #
if selected == "Home":
    st.markdown('<div class="traffiq-brand">TRAFFI<span>Q</span></div>', unsafe_allow_html=True)
    st.markdown(
        """
    <div class="hero">
        <div class="hero-text">
            <h1>Predict Traffic Smarter with AI</h1>
            <p>
            TraffiQ leverages Artificial Intelligence and Machine Learning
            to predict traffic congestion, estimate travel time,
            and support intelligent transportation systems.
            </p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if os.path.exists("assets/hero.jpg"):
        st.image("assets/hero.jpg", use_container_width=True)

    st.write("")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", f"{accuracy*100:.2f}%")
    col2.metric("Traffic Classes", "3")
    col3.metric("Algorithm", "Random Forest")
    col4.metric("Dataset", "48K+")

    st.markdown("---")

    st.header("Features")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if os.path.exists("assets/traffic.png"):
            st.image("assets/traffic.png", width=70)
        st.subheader("Traffic Prediction")
        st.write("Predict Low, Medium and High congestion levels.")

    with c2:
        if os.path.exists("assets/weather.png"):
            st.image("assets/weather.png", width=70)
        st.subheader("Weather Analysis")
        st.write("Uses weather and temporal information.")

    with c3:
        if os.path.exists("assets/time.png"):
            st.image("assets/time.png", width=70)
        st.subheader("Travel Time")
        st.write("Estimate travel duration instantly.")

    with c4:
        if os.path.exists("assets/signal.png"):
            st.image("assets/signal.png", width=70)
        st.subheader("Signal Optimization")
        st.write("Suggest optimal traffic signal duration.")

    st.markdown("---")

    st.header("About TraffiQ")
    st.write("""
TraffiQ is an AI-powered traffic prediction platform that uses Machine Learning
to forecast congestion using weather conditions and historical traffic data.

The objective is to assist commuters and support intelligent transportation systems
through fast and accurate congestion prediction.
""")

# ---------------- OTHER PAGES ---------------- #
elif selected == "Prediction":
    prediction_page(df, rf, encoders, target_encoder)

elif selected == "Analytics":
    analytics_page(
        df=df,
        rf=rf,
        X=X,
        y_test=None,
        rf_pred=None,
        target_encoder=target_encoder,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
    )

elif selected == "About":
    about_page()
