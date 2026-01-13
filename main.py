import streamlit as st
import sys
from pathlib import Path
import tempfile
import os

sys.path.append(str(Path(__file__).parent.parent))

from workflow.state import MedicalAssistantState
from agents.Agent_1_Analyzer.report_analyzer import report_analyzer_agent
from agents.Agent_1_Analyzer.pdf_parser import extract_text_from_pdf
from agents.Agent_1_Analyzer.image_parser import extract_text_from_image
from agents.Agent_2_doctor_recommendation.doctor_recommender import doctor_recommender_agent
from agents.Agent_3_appointment_booking.appointment_booking import appointment_booking_agent
from agents.Agent_4_notification.notifier import notifier_agent

st.set_page_config(
    page_title="Medical Assistant System",
)

if "state" not in st.session_state:
    st.session_state.state = None
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "doctors_displayed" not in st.session_state:
    st.session_state.doctors_displayed = False
if "appointment_booked" not in st.session_state:
    st.session_state.appointment_booked = False
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Patient Information")
    
    patient_name = st.text_input("Patient Name", value="John Doe")
    patient_age = st.number_input("Age", min_value=1, max_value=120, value=45)
    patient_email = st.text_input("Email", value="patient@example.com")
    patient_location = st.selectbox(
        "City",
        ["Bangalore", "Mumbai", "Hyderabad", "Delhi", "Vijayawada", "Chennai", "Chandigarh"]
    )
    
    st.divider()
    
    st.header("Report Input")
    input_type = st.radio(
        "Select Input Type:",
        ["Text Input", "PDF Upload", "Image Upload"]
    )
    
    st.divider()
    
    if st.button("Clear All", type="secondary"):
        st.session_state.state = None
        st.session_state.analysis_done = False
        st.session_state.doctors_displayed = False
        st.session_state.appointment_booked = False
        st.session_state.messages = []
        st.rerun()

st.title("Medical Assistant System")
st.write("Multi-Agent AI System powered by LangGraph")

st.divider()

st.header("Step 1: Upload Medical Report")

input_content = None
file_input_type = "text"

if input_type == "Text Input":
    input_content = st.text_area(
        "Enter medical report data:",
        height=200,
        placeholder="Example:\nPatient: John Doe\nAge: 45 years\n\nLab Results:\n- Blood Pressure: 150/95 mmHg\n- Fasting Blood Sugar: 180 mg/dL\n- Total Cholesterol: 240 mg/dL"
    )
    file_input_type = "text"

elif input_type == "PDF Upload":
    uploaded_file = st.file_uploader("Upload PDF medical report", type=["pdf"])
    if uploaded_file:
        temp_path = Path(tempfile.mktemp(suffix=".pdf"))
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        input_content = extract_text_from_pdf(str(temp_path))
        if input_content:
            st.success("PDF uploaded and text extracted successfully")
            with st.expander("View Extracted Text"):
                st.text(input_content[:500] + "..." if len(input_content) > 500 else input_content)
        else:
            st.error("Failed to extract text from PDF")
        
        temp_path.unlink(missing_ok=True)
    file_input_type = "pdf"

else: 
    uploaded_file = st.file_uploader("Upload medical report image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Medical Report", use_column_width=True)
        
        temp_path = Path(tempfile.mktemp(suffix=".png"))
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        input_content = extract_text_from_image(str(temp_path))
        if input_content:
            st.success("Image uploaded and text extracted using OCR")
            with st.expander("View Extracted Text"):
                st.text(input_content[:500] + "..." if len(input_content) > 500 else input_content)
        else:
            st.error("Failed to extract text from image")
        
        temp_path.unlink(missing_ok=True)
    file_input_type = "image"

if st.button("Analyze Medical Report", type="primary", disabled=not input_content):
    if input_content:
        with st.spinner("Analyzing medical report..."):
            initial_state = MedicalAssistantState(
                input_type=file_input_type,
                input_content=input_content,
                patient_location=patient_location,
                patient_name=patient_name,
                patient_email=patient_email,
                workflow_complete=False,
                chat_history=[]
            )
            
            result_state = report_analyzer_agent(initial_state)
            
            st.session_state.state = result_state
            st.session_state.analysis_done = True
            st.session_state.messages.append(
                f"Analysis complete - Severity: {result_state.get('severity')}, "
                f"Department: {result_state.get('department')}"
            )
            st.rerun()

if st.session_state.analysis_done and st.session_state.state:
    st.divider()
    st.header("Step 2: Analysis Results")
    
    state = st.session_state.state
    severity = state.get("severity", "mild")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Severity", severity.upper())
    with col2:
        st.metric("Department", state.get("department", "N/A").title())
    with col3:
        st.metric("Condition", state.get("disease_type", "N/A").title())
    
    st.subheader("Summary")
    st.write(state.get("report_summary", "No summary available"))
    
    if severity == "normal":
        st.success(
            "Good news! Your medical report shows normal results. "
            "No immediate medical attention required. Continue with regular health checkups."
        )
    else:
        if not st.session_state.doctors_displayed:
            if st.button("Find Doctors", type="primary"):
                with st.spinner("Searching for doctors..."):
                    state = doctor_recommender_agent(state)
                    st.session_state.state = state
                    st.session_state.doctors_displayed = True
                    st.session_state.messages.append(
                        f"Found {len(state.get('recommended_doctors', []))} doctors"
                    )
                    st.rerun()
        
        if st.session_state.doctors_displayed:
            st.divider()
            st.header("Step 3: Recommended Doctors")
            
            doctors = state.get("recommended_doctors", [])
            
            if doctors:
                for i, doctor in enumerate(doctors):
                    with st.expander(
                        f"Dr. {doctor['Name']} - {doctor['Hospital']}", 
                        expanded=(i==0)
                    ):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Speciality:** {doctor['Speciality']}")
                            st.write(f"**Experience:** {doctor['Experience']}")
                            st.write(f"**Hospital:** {doctor['Hospital']}")
                            st.write(f"**City:** {doctor['City']}")
                        
                        with col2:
                            st.write(f"**Email:** {doctor['Email']}")
                            st.write(f"**Phone:** {doctor['Phone']}")
                            avail = doctor.get("Availability", {})
                            avail_days = avail.get("AvailabilityDays", [])
                            if avail_days:
                                st.write(f"**Available Days:** {', '.join(avail_days)}")
                        
                        if st.button(
                            f"Book Appointment with Dr. {doctor['Name']}", 
                            key=f"book_{i}"
                        ):
                            state["selected_doctor"] = doctor
                            state["user_wants_appointment"] = True
                            
                            with st.spinner("Booking appointment..."):
                                state = appointment_booking_agent(state)
                                state = notifier_agent(state)
                                
                                st.session_state.state = state
                                st.session_state.appointment_booked = True
                                st.session_state.messages.append(
                                    f"Appointment booked with Dr. {doctor['Name']}"
                                )
                                st.rerun()
            else:
                st.warning("No doctors found matching your requirements. Please try a different location.")
        
        if st.session_state.appointment_booked:
            st.divider()
            st.header("Step 4: Appointment Confirmation")
            
            appointment = state.get("appointment_details")
            if appointment:
                st.success("APPOINTMENT BOOKED SUCCESSFULLY")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Appointment ID:** {appointment['appointment_id']}")
                    st.write(f"**Doctor:** Dr. {appointment['doctor_name']}")
                    st.write(f"**Hospital:** {appointment['hospital']}")
                
                with col2:
                    st.write(f"**Date:** {appointment['date']}")
                    st.write(f"**Time:** {appointment['time']}")
                    st.write(f"**Concern:** {appointment['patient_concern']}")
                
                st.info(f"Email Status: {state.get('email_status', 'unknown')}")
                st.info("Confirmation emails sent to both you and the doctor.")

st.divider()
st.subheader("Workflow Messages")

if st.session_state.messages:
    for msg in st.session_state.messages:
        st.write(f"- {msg}")
else:
    st.write("No messages yet.")