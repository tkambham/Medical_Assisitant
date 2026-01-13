from workflow.state import MedicalAssistantState
from .load_doctor_availability import load_doctor_availability
from .laod_doctor_db import load_doctors_database

def doctor_recommender_agent(state: MedicalAssistantState) -> MedicalAssistantState:
    department = state.get("department", "general medicine").lower()
    location = state.get("patient_location", "Bangalore")
    severity = state.get("severity", "mild")
    
    all_doctors = load_doctors_database()
    availability_data = load_doctor_availability()
    
    if not all_doctors:
        state["recommended_doctors"] = []
        return state
    
    department_keywords = {
        "cardiology": ["cardiology", "cardiac", "heart"],
        "neurology": ["neurology", "neurologist", "neuro"],
        "orthopedics": ["orthopedics", "orthopedic", "bone"],
        "pediatrics": ["pediatrics", "pediatric", "child"],
        "dermatology": ["dermatology", "skin"],
        "gastroenterology": ["gastroenterology", "gastro", "stomach"],
        "endocrinology": ["endocrinology", "endocrine", "diabetes"],
        "ent": ["ent", "ear", "nose", "throat"],
        "internal medicine": ["internal medicine", "general medicine"],
        "obstetrics": ["obstetrics", "gynecology", "obg", "women"]
    }
    
    search_terms = []
    for dept, keywords in department_keywords.items():
        if any(keyword in department for keyword in keywords):
            search_terms.extend(keywords)
            break
    
    if not search_terms:
        search_terms = [department]
    
    recommended = []
    for doctor in all_doctors:
        doc_speciality = doctor.get("Speciality", "").lower()
        doc_location = doctor.get("City", "").lower()
        
        speciality_match = any(term in doc_speciality for term in search_terms)
        location_match = location.lower() in doc_location
        
        if speciality_match and location_match:
            doctor_id = doctor.get("DoctorID")
            if doctor_id in availability_data:
                doctor["Availability"] = availability_data[doctor_id]
            else:
                doctor["Availability"] = {
                    "AvailabilityDays": [],
                    "Schedule": {}
                }
            
            recommended.append(doctor)
    
    if severity == "critical":
        recommended.sort(
            key=lambda x: int(x.get("Experience", "0 years").split()[0]), 
            reverse=True
        )
    
    recommended = recommended[:5]
    
    state["recommended_doctors"] = recommended
    
    state.setdefault("chat_history", []).append(
        f"Found {len(recommended)} {department} doctors in {location}"
    )
    
    return state
