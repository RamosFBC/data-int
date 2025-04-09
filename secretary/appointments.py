import streamlit as st
import pandas as pd
from datetime import datetime
import requests


### Section 3: Monitoring Today's Appointments
st.header("Today's Appointments")

# Convert 'Date' to datetime.date for consistent comparison
if not st.session_state.appointments.empty:
    st.session_state.appointments["Date"] = pd.to_datetime(
        st.session_state.appointments["Date"]
    ).dt.date

today = datetime.now().date()
todays_appointments = st.session_state.appointments[
    st.session_state.appointments["Date"] == today
]

if not todays_appointments.empty:
    # convert 'Time' to datetime.time for consistent comparison
    todays_appointments["Time"] = pd.to_datetime(
        todays_appointments["Time"], format="%H:%M:%S"
    ).dt.time
    todays_appointments = todays_appointments.sort_values(by="Time")
    st.write(f"Appointments scheduled for today ({today}):")
    for index, appointment in todays_appointments.iterrows():
        # Retrieve the patient's name by their ID
        patient_name = st.session_state.patients[
            st.session_state.patients["Patient ID"] == appointment["Patient ID"]
        ]["Name"].values[0]

        st.subheader(f"Hora: {appointment['Time']}")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(f"Name: {patient_name}")
            if st.button(
                "Mark as Attended", key=f"attended_{appointment['Appointment ID']}"
            ):
                st.session_state.appointments.at[index, "Attended"] = True
                st.session_state.appointments.at[index, "Canceled"] = False
                data = {
                    "Appointment ID": appointment["Appointment ID"],
                    "Attended": True,
                    "Canceled": False,
                }
                # Update the tables at google sheetes with n8n api
                url = "https://feliperamos.app.n8n.cloud/webhook-test/4b863963-7c56-43f6-84e0-7768137f2645"
                response = requests.post(url, json=data)
                st.success(
                    f"Appointment ID {appointment['Appointment ID']} marked as attended successfully!"
                )

        with col2:
            if st.button(
                "Cancel Appointment", key=f"cancel_{appointment['Appointment ID']}"
            ):
                st.session_state.appointments.at[index, "Canceled"] = True
                st.success(
                    f"Appointment ID {appointment['Appointment ID']} canceled successfully!"
                )

        with col3:
            st.write(f"Insurance: {appointment['Insurance']}")

        with col4:
            payment = st.number_input(
                "Payment (R$)",
                min_value=0.0,
                value=float(appointment["Payment Status"]),
                key=f"payment_{appointment['Appointment ID']}",
            )
            st.session_state.appointments.at[index, "Payment Status"] = payment
        st.write("---")
else:
    st.write("No appointments scheduled for today.")
