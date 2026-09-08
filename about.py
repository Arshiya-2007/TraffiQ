import streamlit as st


def about_page():
    st.title("About TraffiQ")
    st.write(
        "TraffiQ is an Intelligent Transportation System (ITS) platform aimed at easing urban congestion."
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🎯 Project Goals")
        st.write("""
        - **Accurate Traffic Forecasting:** Help drivers avoid peak congestion.
        - **Data-Driven Infrastructure:** Assist traffic authorities with adaptive signal timing.
        - **Environmental Impact:** Reduce vehicle idling and lower carbon emissions in urban areas.
        """)

    with c2:
        st.subheader("⚙️ Technology Stack")
        st.write("""
        - **Frontend Framework:** Streamlit
        - **Data Processing:** Pandas, NumPy
        - **Machine Learning:** Scikit-Learn (Random Forest)
        - **Visualization:** Matplotlib, Seaborn
        """)

    st.markdown("---")
    st.subheader("👥 System Architecture")
    st.write("""
    The system processes real-time inputs including temporal features (hour, day, month) and environmental 
    data (temperature, rainfall, weather conditions). The Random Forest Classifier evaluates these inputs against 
    trained historical patterns to output immediate congestion predictions along with signal adjustment advice.
    """)