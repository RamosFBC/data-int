import streamlit as st
import pandas as pd
from datetime import datetime
import requests


### Section 2: Appointment Registration
st.header("Appointment Registration")

# Check if there are registered patients
if not st.session_state.patients.empty:
    # Create a list of patients for selection
    patients_list = st.session_state.patients["Name"].tolist()
    selected_patient = st.selectbox("Select Patient", patients_list)

    with st.form("appointment_registration"):
        date = st.date_input("Appointment Date")
        date = pd.to_datetime(date).date()
        time = st.time_input("Appointment Time")

        insurance = st.selectbox(
            "Insurance", ["Unimed", "Bradesco Saúde", "Amil", "Private", "Other"]
        )
        submit_appointment = st.form_submit_button("Schedule Appointment")

    if submit_appointment:
        # Find the ID of the selected patient
        patient_id = st.session_state.patients[
            st.session_state.patients["Name"] == selected_patient
        ]["Patient ID"].values[0]

        # Generate a unique ID for the appointment
        appointment_id = len(st.session_state.appointments) + 1

        # Check if it is the first appointment
        if st.session_state.appointments.empty:
            first_appointment = True
        else:
            first_appointment = (
                st.session_state.appointments[
                    st.session_state.appointments["Patient ID"] == patient_id
                ].shape[0]
                == 0
            )

        data = {
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "date": date,
            "time": time,
            "first_appointment": first_appointment,
            "insurance": insurance,
            "payment_status": 0.0,
            "attended": False,
            "canceled": False,
        }

        response = requests.post(
            "https://feliperamos.app.n8n.cloud/webhook-test/03bebc41-3821-4a55-9926-c5c7949c839a",
            data=data,
        )
        # Load response return data and update session state
        if response.status_code == 200:
            response_data = response.json()
            st.write(response_data)
            # Ensure correct data types
            response_data["Date"] = pd.to_datetime(
                response_data["Date"], format="%Y-%m-%d"
            ).date()
            response_data["Time"] = pd.to_datetime(
                response_data["Time"], format="%H:%M:%S"
            ).time()
            response_data["Payment Status"] = float(response_data["Payment Status"])
            response_data["Attended"] = (
                False if response_data["Attended"] == "false" else True
            )
            response_data["First Appointment"] = (
                False if response_data["First Appointment"] == "false" else True
            )

            response_data["Canceled"] = (
                False if response_data["Canceled"] == "false" else True
            )
            response_data["Insurance"] = str(response_data["Insurance"])
            response_data["row_number"] = int(response_data["row_number"])
            new_appointment = pd.DataFrame([response_data])
            st.session_state.appointments = pd.concat(
                [st.session_state.appointments, new_appointment], ignore_index=True
            )
            st.success(
                f"Appointment successfully scheduled! Appointment ID: {response_data['Appointment ID']}"
            )
        else:
            st.error("Error scheduling appointment.")

else:
    st.warning("No patients registered. Please register a patient first.")
