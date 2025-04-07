import streamlit as st
import pandas as pd
from datetime import datetime
import requests


### Section 1: Patient Registration
st.header("Patient Registration")

with st.form("patient_registration"):
    patient_name = st.text_input("Patient Name")
    patient_phone = st.text_input("Phone")
    patient_email = st.text_input("Email")
    referral_source = st.selectbox(
        "How did you hear about the doctor?",
        ["Social Media", "Website", "Google", "Referral", "Other"],
    )
    submit_patient = st.form_submit_button("Register Patient")

if submit_patient:
    # Generate a unique ID for the patient
    patient_id = len(st.session_state.patients) + 1
    new_patient = pd.DataFrame(
        {
            "Patient ID": [patient_id],
            "Name": [patient_name],
            "Phone": [patient_phone],
            "Email": [patient_email],
            "Referral Source": [referral_source],
        }
    )
    st.session_state.patients = pd.concat(
        [st.session_state.patients, new_patient], ignore_index=True
    )
    # make a POST request
    data = {
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "patient_email": patient_email,
        "referral_source": referral_source,
    }
    response = requests.post(
        "https://feliperamos.app.n8n.cloud/webhook-test/c6bd068c-6aed-4e49-8b82-d0beb4b0e08d",
        data=data,
    )

    st.success(f"Patient {patient_name} successfully registered! ID: {patient_id}")
