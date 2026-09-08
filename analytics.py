import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def create_transparent_fig(figsize=(8, 4)):
    """Helper to maintain dark background consistency."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    return fig, ax


def analytics_page(
    df,
    rf,
    X,
    y_test,
    rf_pred,
    target_encoder,
    accuracy,
    precision,
    recall,
    f1,
):

    st.title("Analytics Dashboard")
    st.write("Model performance, feature importance, and traffic insights.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accuracy", f"{accuracy*100:.2f}%")
    c2.metric("Precision", f"{precision*100:.2f}%")
    c3.metric("Recall", f"{recall*100:.2f}%")
    c4.metric("F1 Score", f"{f1*100:.2f}%")

    st.divider()

    # ---------------- Feature Importance ---------------- #
    st.subheader("Feature Importance")

    features = [
        "holiday",
        "temp",
        "rain_1h",
        "snow_1h",
        "clouds_all",
        "weather_main",
        "weather_description",
        "hour",
        "day",
        "month",
    ]

    if rf is not None and hasattr(rf, "feature_importances_"):
        importances = rf.feature_importances_

        # Safety check in case feature counts differ
        if len(importances) != len(features):
            min_len = min(len(importances), len(features))
            features = features[:min_len]
            importances = importances[:min_len]
    else:
        # Placeholder fallback feature importance
        features = ["hour", "temp", "clouds_all", "month", "day", "rain_1h"]
        importances = [0.40, 0.22, 0.15, 0.11, 0.08, 0.04]

    importance_df = pd.DataFrame(
        {"Feature": features, "Importance": importances}
    ).sort_values("Importance", ascending=False)

    fig, ax = create_transparent_fig(figsize=(8, 4))
    sns.barplot(
        data=importance_df,
        x="Importance",
        y="Feature",
        palette="Blues_r",
        ax=ax,
    )
    st.pyplot(fig)

    st.divider()

    # ---------------- Traffic Distribution ---------------- #
    if "traffic_volume" in df.columns:
        st.subheader("Traffic Volume Distribution")
        fig, ax = create_transparent_fig(figsize=(8, 4))
        sns.histplot(
            df["traffic_volume"],
            bins=30,
            kde=True,
            color="royalblue",
            ax=ax,
        )
        st.pyplot(fig)
        st.divider()

    # ---------------- Hourly Trends ---------------- #
    if "hour" in df.columns and "traffic_volume" in df.columns:
        st.subheader("Average Traffic by Hour")
        hourly = df.groupby("hour")["traffic_volume"].mean()

        fig, ax = create_transparent_fig(figsize=(9, 4))
        ax.plot(
            hourly.index,
            hourly.values,
            linewidth=3,
            marker="o",
            color="#00E676",
        )
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Average Traffic")
        st.pyplot(fig)
        st.divider()

    # ---------------- Monthly Trends ---------------- #
    if "month" in df.columns and "traffic_volume" in df.columns:
        st.subheader("Average Traffic by Month")
        monthly = df.groupby("month")["traffic_volume"].mean()

        fig, ax = create_transparent_fig(figsize=(8, 4))
        ax.plot(
            monthly.index,
            monthly.values,
            marker="o",
            linewidth=3,
            color="orange",
        )
        ax.set_xlabel("Month")
        ax.set_ylabel("Average Traffic")
        st.pyplot(fig)
        st.divider()

    # ---------------- Weather Breakdown ---------------- #
    if "weather_main" in df.columns:
        st.subheader("Weather Conditions Breakdown")
        fig, ax = create_transparent_fig(figsize=(8, 4))
        df["weather_main"].value_counts().plot(
            kind="bar", color="steelblue", ax=ax
        )
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.divider()

    # ---------------- Correlation Heatmap ---------------- #
    st.subheader("Correlation Heatmap")
    fig, ax = create_transparent_fig(figsize=(9, 5))
    numeric_df = df.select_dtypes(include=["number"])
    sns.heatmap(
        numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax
    )
    st.pyplot(fig)