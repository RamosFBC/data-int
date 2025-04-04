import streamlit as st


def settings_page():
    st.title("Settings")

    st.header("User Preferences")
    username = st.text_input("Username", value="Enter your username")
    theme = st.selectbox("Theme", options=["Light", "Dark"], index=0)

    st.header("Application Settings")
    notifications = st.checkbox("Enable Notifications", value=True)
    data_refresh_rate = st.slider(
        "Data Refresh Rate (seconds)", min_value=1, max_value=60, value=10
    )

    st.header("Save Settings")
    if st.button("Save"):
        st.success("Settings saved successfully!")
        # Here you can add logic to save these settings to a file or database


if __name__ == "__main__":
    settings_page()
