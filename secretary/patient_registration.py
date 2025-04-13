import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Translation mappings
referral_map = {
    "Social Media": "Mídias Sociais",
    "Website": "Site",
    "Google": "Google",
    "Referral": "Indicação",
    "Other": "Outro",
}

# Reverse mapping for processing
reverse_referral_map = {v: k for k, v in referral_map.items()}
### Section 1: Patient Registration
st.header("Registrar Paciente")

with st.form("patient_registration"):
    patient_name = st.text_input("Nome do paciente")
    patient_phone = st.text_input("Número de telefone")
    patient_email = st.text_input("Email")
    referral_source_pt = st.selectbox(
        "Como o paciente conheceu o médico?",
        list(referral_map.values()),
    )
    submit_patient = st.form_submit_button("Registrar Paciente")

if submit_patient:
    # Generate a unique ID for the patient
    patient_id = len(st.session_state.patients) + 1
    # Convert Portuguese referral source to English for internal use
    referral_source_en = reverse_referral_map[referral_source_pt]
    new_patient = pd.DataFrame(
        {
            "Patient ID": [patient_id],
            "Name": [patient_name],
            "Phone": [patient_phone],
            "Email": [patient_email],
            "Referral Source": [referral_source_en],
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
        "referral_source": referral_source_en,
    }
    response = requests.post(
        st.secrets["n8n"]["post_patient_url"],
        data=data,
    )
    if response.status_code == 200:
        response_data = response.json()
        st.write(response_data)
        # Ensure correct data types
        response_data["Patient ID"] = str(response_data["Patient ID"])
        response_data["Name"] = str(response_data["Name"])
        response_data["Phone"] = str(response_data["Phone"])
        response_data["Email"] = str(response_data["Email"])
        response_data["Referral Source"] = str(response_data["Referral Source"])
        new_patient = pd.DataFrame([response_data])
        st.session_state.patients = pd.concat(
            [st.session_state.patients, new_patient], ignore_index=True
        )
        st.success(
            f"Patient successfully registered! Patient ID: {response_data['Patient ID']}"
        )
    else:
        st.error("Error registering patient.")

    st.success(f"Patient {patient_name} successfully registered! ID: {patient_id}")
