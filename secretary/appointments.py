import streamlit as st
import pandas as pd
from datetime import datetime
import requests


### Section 3: Monitoring Today's Appointments
st.header("Todas as Consultas de Hoje")

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
    st.write(f"Consultas de hoje ({today}):")
    for index, appointment in todays_appointments.iterrows():
        # Retrieve the patient's name by their ID, with a fallback
        patient_match = st.session_state.patients[
            st.session_state.patients["Patient ID"] == appointment["Patient ID"]
        ]
        st.write(
            f"Appointment ID: {appointment['Appointment ID']}, Patient ID: {appointment['Patient ID']}"
        )
        if not patient_match.empty:
            patient_name = patient_match["Name"].values[0]
        else:
            patient_name = "Unknown Patient"

        st.subheader(f"Hora: {appointment['Time']}")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(f"Nome: {patient_name}")
            if st.button(
                "Consulta Realizada", key=f"attended_{appointment['Appointment ID']}"
            ):
                st.session_state.appointments.at[index, "Attended"] = True
                st.session_state.appointments.at[index, "Canceled"] = False
                data = {
                    "Appointment ID": appointment["Appointment ID"],
                    "Attended": True,
                    "Canceled": False,
                }
                url = st.secrets["n8n"]["post_attended_url"]
                response = requests.post(url, json=data)
                response_data = response.json()
                # Ensure correct data types
                response_data["Attended"] = (
                    False if response_data["Attended"] == "false" else True
                )
                response_data["Canceled"] = (
                    False if response_data["Canceled"] == "false" else True
                )
                # Update the appointment status in session state
                st.session_state.appointments.at[index, "Attended"] = response_data[
                    "Attended"
                ]
                st.session_state.appointments.at[index, "Canceled"] = response_data[
                    "Canceled"
                ]
                st.success(
                    f"Appointment ID {appointment['Appointment ID']} marked as attended successfully!"
                )

        with col2:
            if st.button(
                "Cancelar Consulta", key=f"cancel_{appointment['Appointment ID']}"
            ):
                data = {
                    "Appointment ID": appointment["Appointment ID"],
                    "Canceled": True,
                    "Attended": False,
                }
                url = st.secrets["n8n"]["post_canceled_url"]
                response = requests.post(url, json=data)
                response_data = response.json()
                # Ensure correct data types
                response_data["Canceled"] = (
                    False if response_data["Canceled"] == "false" else True
                )
                response_data["Attended"] = (
                    False if response_data["Attended"] == "false" else True
                )
                # Update the appointment status in session state
                st.session_state.appointments.at[index, "Canceled"] = response_data[
                    "Canceled"
                ]
                st.session_state.appointments.at[index, "Attended"] = response_data[
                    "Attended"
                ]
                st.session_state.appointments.at[index, "Canceled"] = True
                st.success(
                    f"Appointment ID {appointment['Appointment ID']} canceled successfully!"
                )

        with col3:
            st.write(f"Convênio: {appointment['Insurance']}")

        with col4:
            payment = st.number_input(
                "Pagamento (R$)",
                min_value=0.0,
                value=float(appointment["Payment Status"]),
                key=f"payment_{appointment['Appointment ID']}",
            )
            if st.button(
                "Salvar Pagamento", key=f"save_payment_{appointment['Appointment ID']}"
            ):
                # st.session_state.appointments.at[index, "Payment Status"] = payment
                data = {
                    "Appointment ID": appointment["Appointment ID"],
                    "Payment Status": payment,
                }
                url = st.secrets["n8n"]["post_payment_url"]
                response = requests.post(url, json=data)
                response_data = response.json()
                # Assuming the API returns the updated payment status
                st.session_state.appointments.at[index, "Payment Status"] = float(
                    response_data.get("Payment Status", payment)
                )
                st.success(
                    f"Payment for Appointment ID {appointment['Appointment ID']} updated to R${payment:.2f}!"
                )
        st.write("---")
else:
    st.write("No appointments scheduled for today.")
