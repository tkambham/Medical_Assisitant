from workflow.state import MedicalAssistantState
from datetime import datetime, timedelta
from .generate_appointment_id import generate_appointment_id

def appointment_booking_agent(state: MedicalAssistantState) -> MedicalAssistantState:
    
    selected_doctor = state.get("selected_doctor")
    
    if not selected_doctor:
        state["appointment_details"] = None
        return state
    
    doctor_name = selected_doctor.get("Name", "Unknown")
    hospital = selected_doctor.get("Hospital", "Unknown Hospital")
    
    availability = selected_doctor.get("Availability", {})
    schedule = availability.get("Schedule", {})
    available_days = availability.get("AvailabilityDays", [])
    
    if not available_days:
        appointment_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        appointment_time = "10:00 AM"
    else:
        first_day = available_days[0]
        day_schedule = schedule.get(first_day, {})
        time_slots = day_schedule.get("time_slots", ["10:00 AM - 12:00 PM"])
        
        selected_slot = time_slots[0]
        appointment_time = selected_slot.split(" - ")[0]  # Get start time
        
        day_full = day_schedule.get("day", "Monday")
        days_ahead = 1 
        appointment_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    
    appointment_id = generate_appointment_id()
    
    appointment_details = {
        "appointment_id": appointment_id,
        "doctor_name": doctor_name,
        "doctor_id": selected_doctor.get("DoctorID"),
        "hospital": hospital,
        "date": appointment_date,
        "time": appointment_time,
        "patient_concern": state.get("disease_type", "General consultation"),
        "severity": state.get("severity", "mild"),
        "doctor_email": selected_doctor.get("Email"),
        "doctor_phone": selected_doctor.get("Phone"),
        "booking_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "confirmed"
    }
    
    state["appointment_details"] = appointment_details

    state.setdefault("chat_history", []).append(
        f"Appointment booked: {appointment_id} with Dr. {doctor_name} on {appointment_date} at {appointment_time}"
    )
    
    return state
