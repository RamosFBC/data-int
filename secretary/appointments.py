import streamlit as st
import pandas as pd
from datetime import datetime
import requests


### Section 3: Monitoring Today's Appointments
st.header("Today's Appointments")

# Ensure 'Date' is in datetime64[ns] format (don't convert to .dt.date permanently)
if not st.session_state.appointments.empty:
    # Convert 'Date' to datetime64[ns] if it isn't already
    st.session_state.appointments["Date"] = pd.to_datetime(
        st.session_state.appointments["Date"]
    )

today = datetime.now().date()
# Use .dt.date only for comparison, not for modifying the column
todays_appointments = st.session_state.appointments[
    st.session_state.appointments["Date"].dt.date == today
]

if not todays_appointments.empty:
    # Convert 'Time' to datetime.time for sorting/display
    todays_appointments["Time"] = pd.to_datetime(
        todays_appointments["Time"], format="%H:%M:%S"
    ).dt.time
    todays_appointments = todays_appointments.sort_values(by="Time")
    st.write(f"Appointments scheduled for today ({today}):")
    for index, appointment in todays_appointments.iterrows():
        # Retrieve the patient's name by their ID, with a fallback
        patient_match = st.session_state.patients[
            st.session_state.patients["Patient ID"] == appointment["Patient ID"]
        ]
        if not patient_match.empty:
            patient_name = patient_match["Name"].values[0]
        else:
            patient_name = "Unknown Patient"

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

# Debug section
if st.checkbox("Exibir tabelas de dados (debug)"):
    st.subheader("Tabela de Pacientes")
    st.write(st.session_state.patients)
    st.subheader("Tabela de Consultas")
    # Optionally convert 'Date' and 'Time' to strings for display
    display_df = st.session_state.appointments.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    display_df["Time"] = pd.to_datetime(
        display_df["Time"], format="%H:%M:%S"
    ).dt.strftime("%H:%M:%S")
    st.write(display_df)
