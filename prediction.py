import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder


# ----------------------------------------------------------
# Load feature encoders from dataset
# ----------------------------------------------------------
@st.cache_resource
def load_feature_encoders():
    try:
        df = pd.read_csv("Cleaned_Traffic_Dataset.csv")
    except Exception:
        # Fallback if CSV is not found
        df = pd.DataFrame({
            "holiday": ["None", "Christmas"],
            "weather_main": ["Clear", "Rain"],
            "weather_description": ["Sky is Clear", "Light Rain"]
        })

    holiday_encoder = LabelEncoder()
    weather_encoder = LabelEncoder()
    weather_desc_encoder = LabelEncoder()

    df["holiday"] = df["holiday"].fillna("Unknown")
    df["weather_main"] = df["weather_main"].fillna("Unknown")
    df["weather_description"] = df["weather_description"].fillna("Unknown")

    holiday_encoder.fit(df["holiday"])
    weather_encoder.fit(df["weather_main"])
    weather_desc_encoder.fit(df["weather_description"])

    return (
        holiday_encoder,
        weather_encoder,
        weather_desc_encoder,
    )


holiday_encoder, weather_encoder, weather_desc_encoder = (
    load_feature_encoders()
)


# ----------------------------------------------------------
# Prediction Page
# ----------------------------------------------------------
def prediction_page(df, rf, encoders, target_encoder):

    st.markdown('<div class="traffiq-brand">TRAFFI<span>Q</span></div>', unsafe_allow_html=True)
    st.title("Traffic Congestion Prediction")

    st.write(
        """
Enter weather conditions and travel information below to predict
traffic congestion using the trained Random Forest model.
"""
    )

    st.markdown("---")

    left, right = st.columns(2)

    # ---------------- LEFT ---------------- #
    with left:

        st.subheader("🌦 Weather Information")

        holiday = st.selectbox(
            "Holiday",
            holiday_encoder.classes_
        )

        weather = st.selectbox(
            "Weather",
            weather_encoder.classes_
        )

        weather_desc = st.selectbox(
            "Weather Description",
            weather_desc_encoder.classes_
        )

        temp = st.number_input(
            "Temperature (Kelvin)",
            value=288.0,
            step=0.5
        )

        rain = st.number_input(
            "Rainfall (mm)",
            value=0.0,
            step=0.1
        )

        snow = st.number_input(
            "Snowfall (mm)",
            value=0.0,
            step=0.1
        )

        clouds = st.slider(
            "Cloud Cover (%)",
            0,
            100,
            50
        )

    # ---------------- RIGHT ---------------- #
    with right:

        st.subheader("🚗 Travel Information")

        hour = st.slider(
            "Hour",
            0,
            23,
            12
        )

        day = st.slider(
            "Day",
            1,
            31,
            15
        )

        month = st.slider(
            "Month",
            1,
            12,
            6
        )

        distance = st.number_input(
            "Travel Distance (km)",
            min_value=1.0,
            value=10.0,
            step=1.0
        )

    st.markdown("---")

    predict = st.button(
        "🚦 Predict Congestion",
        use_container_width=True
    )

    if predict:
        try:
            if rf is None:
                st.error("Random Forest model not found.")
                st.stop()

            if target_encoder is None:
                st.error("Target encoder not found.")
                st.stop()

            # Encode categorical inputs
            holiday_encoded = holiday_encoder.transform([holiday])[0]
            weather_encoded = weather_encoder.transform([weather])[0]
            weather_desc_encoded = weather_desc_encoder.transform([weather_desc])[0]

            # Create model input dataframe
            input_df = pd.DataFrame(
                [{
                    "holiday": holiday_encoded,
                    "temp": temp,
                    "rain_1h": rain,
                    "snow_1h": snow,
                    "clouds_all": clouds,
                    "weather_main": weather_encoded,
                    "weather_description": weather_desc_encoded,
                    "hour": hour,
                    "day": day,
                    "month": month
                }]
            )

            # Perform prediction
            prediction_index = rf.predict(input_df)[0]
            prediction = target_encoder.inverse_transform([prediction_index])[0]
            probabilities = rf.predict_proba(input_df)[0]
            confidence = probabilities[prediction_index] * 100

            # Calculate Travel Time & Signal Duration
            if prediction == "Low":
                avg_speed = 60
                signal_time = "30 Seconds"
            elif prediction == "Medium":
                avg_speed = 40
                signal_time = "60 Seconds"
            else:
                avg_speed = 25
                signal_time = "90 Seconds"

            travel_time = round((distance / avg_speed) * 60, 1)

            # Prominent Result Display Banner
            st.markdown("---")

            if prediction == "Low":
                bg_color = "#008938"
                border_color = "#00E676"
                icon = "🟢"
                status_text = "LOW CONGESTION"
            elif prediction == "Medium":
                bg_color = "#B78103"
                border_color = "#FFD600"
                icon = "🟡"
                status_text = "MEDIUM CONGESTION"
            else:
                bg_color = "#C62828"
                border_color = "#FF5252"
                icon = "🔴"
                status_text = "HIGH CONGESTION"

            st.markdown(
                f"""
                <div style="
                    background-color: {bg_color};
                    border: 2px solid {border_color};
                    border-radius: 18px;
                    padding: 25px;
                    text-align: center;
                    margin-bottom: 25px;
                    box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
                ">
                    <span style="font-size: 16px; text-transform: uppercase; letter-spacing: 2px; color: #FFFFFF; font-weight: 600;">Predicted Traffic Level</span>
                    <h1 style="font-size: 42px; margin: 8px 0; font-weight: 800; color: #FFFFFF; text-shadow: 0px 3px 6px rgba(0,0,0,0.4);">
                        {icon} {status_text}
                    </h1>
                </div>
            """,
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Confidence", f"{confidence:.2f}%")
            with c2:
                st.metric("Estimated Travel Time", f"{travel_time} min")
            with c3:
                st.metric("Signal Duration", signal_time)

            st.markdown("---")

            # Prediction Probabilities Bar Chart
            st.subheader("📊 Prediction Probabilities")

            congestion_labels = ["Low", "Medium", "High"]
            if len(probabilities) == len(congestion_labels):
                labels = congestion_labels
            elif hasattr(target_encoder, "classes_") and len(target_encoder.classes_) == len(probabilities):
                labels = target_encoder.classes_
            else:
                labels = [f"Level {i+1}" for i in range(len(probabilities))]

            prob_df = pd.DataFrame(
                {
                    "Congestion": labels,
                    "Probability (%)": probabilities * 100,
                }
            )

            import matplotlib.pyplot as plt
            import seaborn as sns

            plt.style.use("dark_background")
            fig, ax = plt.subplots(figsize=(7, 3))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)

            color_map = {
                "Low": "#00E676",      # Green
                "Medium": "#FFD600",   # Yellow
                "High": "#FF5252",     # Red
            }
            colors = [color_map.get(label, "#2C7BE5") for label in prob_df["Congestion"]]

            sns.barplot(
                data=prob_df,
                x="Congestion",
                y="Probability (%)",
                palette=colors,
                ax=ax,
            )

            ax.set_ylim(0, 100)
            ax.set_ylabel("Probability (%)")
            ax.set_xlabel("")

            for p in ax.patches:
                height = p.get_height()
                if height > 0:
                    ax.annotate(
                        f"{height:.1f}%",
                        (p.get_x() + p.get_width() / 2.0, height),
                        ha="center",
                        va="bottom",
                        xytext=(0, 3),
                        textcoords="offset points",
                        color="white",
                        fontweight="bold",
                    )

            st.pyplot(fig)

            st.markdown("---")

            # Recommendations
            st.subheader("Travel Recommendation")
            if prediction == "Low":
                st.success("✅ Roads are mostly clear. Recommended Speed: **60 km/h**. Ideal time to travel.")
            elif prediction == "Medium":
                st.warning("⚠ Moderate traffic detected. Recommended Speed: **40 km/h**. Expect minor delays.")
            else:
                st.error("🚨 Heavy congestion detected. Recommended Speed: **25 km/h**. Consider alternate routes.")

        except Exception as e:
            st.error("Prediction Failed")
            st.exception(e)