def patient_email_template(appointment,patient_name):
    
    # Patient email
    patient_subject = f"Appointment Confirmation - {appointment['appointment_id']}"
    patient_body = f"""
        Dear {patient_name},

        Your appointment has been confirmed!

        APPOINTMENT DETAILS:
        --------------------
        Appointment ID: {appointment['appointment_id']}
        Date: {appointment['date']}
        Time: {appointment['time']}
        Doctor: Dr. {appointment['doctor_name']}
        Hospital: {appointment['hospital']}
        Concern: {appointment['patient_concern']}

        Contact: {appointment['doctor_phone']}

        Please arrive 15 minutes early.

        Thank you,
        Medical Assistant System
            """
    
    return patient_subject, patient_body

def doctor_email_template(appointment, patient_name):
    doctor_subject = f"New Appointment - {appointment['appointment_id']}"
    doctor_body = f"""
        Dear Dr. {appointment['doctor_name']},

        New appointment scheduled:

        DETAILS:
        --------
        Appointment ID: {appointment['appointment_id']}
        Date: {appointment['date']}
        Time: {appointment['time']}
        Patient: {patient_name}
        Concern: {appointment['patient_concern']}
        Severity: {appointment['severity'].upper()}

        Medical Assistant System
            """
    
    return doctor_subject, doctor_body
