import streamlit as st


def load_css():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Solid Dark Navy Background (#00072D) - No Linear Gradients */
    .stApp {
        background-color: #00072D !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    header, footer {
        visibility: hidden;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-left: 4rem;
        padding-right: 4rem;
        padding-bottom: 2rem;
    }

    /* TRAFFIQ BRAND TEXT */
    .traffiq-brand {
        font-weight: 800 !important;
        font-size: 38px !important;
        color: #FFFFFF !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        display: inline-block;
    }

    .traffiq-brand span {
        color: #00E676; /* Vibrant Accent Green */
    }

    /* HERO CONTAINER */
    .hero {
        background-color: #001242; /* Slightly lighter Navy contrast container */
        border-radius: 20px;
        padding: 40px 60px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    }

    .hero h1 {
        font-size: 48px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
        color: #E2E8F0; /* Clean Off-White */
        max-width: 850px;
        margin: auto;
        line-height: 1.6;
    }

    /* CARDS & METRICS (Navy Background + Crisp White Text) */
    div[data-testid="stMetric"] {
        background-color: #001242;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.3s ease-in-out;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #00E676;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6);
    }

    /* Metric Values and Labels in Pure White */
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #E2E8F0 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    p, span, label {
        color: #FFFFFF !important;
    }

    /* PREDICTION BUTTON (Solid Dark Green with Bold White Text) */
    .stButton>button {
        width: 100%;
        height: 60px;
        border-radius: 14px;
        border: 1px solid #00E676;
        background-color: #008938;
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px;
        transition: 0.3s ease-in-out;
        box-shadow: 0px 6px 20px rgba(0, 137, 56, 0.4);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        background-color: #00A843;
        box-shadow: 0px 10px 28px rgba(0, 230, 118, 0.5);
    }

    hr {
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )