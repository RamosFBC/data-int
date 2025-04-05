import streamlit as st
import pandas as pd
from datetime import datetime


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

        # Create a new entry in the Appointments table with the patient ID
        new_appointment = pd.DataFrame(
            {
                "Appointment ID": [appointment_id],
                "Patient ID": [patient_id],
                "Date": [date],
                "Time": [time],
                "Payment Status": [0.0],
                "Attended": [False],
                "First Appointment": [first_appointment],
                "Insurance": [insurance],
                "Canceled": [False],
            }
        )
        st.session_state.appointments = pd.concat(
            [st.session_state.appointments, new_appointment], ignore_index=True
        )
        st.success(
            f"Appointment successfully scheduled! Appointment ID: {appointment_id}"
        )
else:
    st.warning("No patients registered. Please register a patient first.")
