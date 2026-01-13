from typing import TypedDict, Literal, Optional, List, Dict
from langgraph.graph import MessagesState

class MedicalAssistantState(TypedDict, total=False):
    input_type: Literal["pdf", "image", "text"]
    input_content: str
    
    report_summary: Optional[str]
    severity: Optional[Literal["normal", "mild", "critical"]]
    department: Optional[str]
    disease_type: Optional[str]
    patient_location: str  
    
    recommended_doctors: List[Dict] 
    selected_doctor: Optional[Dict]
    
    appointment_details: Optional[Dict]
    email_status: Optional[str]
    
    user_wants_appointment: bool  
    workflow_complete: bool 
    chat_history: List[str] 

    patient_name: str
    patient_email: str
    email_status: Optional[str]