import streamlit as st
import pandas as pd
from datetime import datetime


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
    st.success(f"Patient {patient_name} successfully registered! ID: {patient_id}")
