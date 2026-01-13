from workflow.state import MedicalAssistantState
from .email_templates import patient_email_template, doctor_email_template
from .send_email import send_email

def notifier_agent(state: MedicalAssistantState) -> MedicalAssistantState:
    appointment = state.get("appointment_details")
    
    if not appointment:
        state["email_status"] = "failed"
        return state
    
    patient_name = state.get("patient_name", "Patient")
    patient_email = state.get("patient_email", "patient@example.com")

    patient_subject, patient_body = patient_email_template(appointment, patient_name)

    doctor_subject, doctor_body = doctor_email_template(appointment, patient_name)

    patient_success = send_email(patient_email, patient_subject, patient_body)
    doctor_success = send_email(
        appointment['doctor_email'], 
        doctor_subject, 
        doctor_body
    )
    
    if patient_success and doctor_success:
        state["email_status"] = "success"
    elif patient_success or doctor_success:
        state["email_status"] = "partial"
    else:
        state["email_status"] = "failed"
    
    state["workflow_complete"] = True
    
    return state

