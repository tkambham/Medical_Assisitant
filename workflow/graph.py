from langgraph.graph import StateGraph, START, END
from workflow.state import MedicalAssistantState

from agents.Agent_1_Analyzer.report_analyzer import report_analyzer_agent
from agents.Agent_2_doctor_recommendation.doctor_recommender import doctor_recommender_agent
from agents.Agent_3_appointment_booking.appointment_booking import appointment_booking_agent
from agents.Agent_4_notification.notifier import notifier_agent

def route_after_analysis(state: MedicalAssistantState) -> str:
    severity = state.get("severity", "mild")
    if severity == "normal":
        return END
    else:
        return "doctor_recommender"

def route_after_recommendation(state: MedicalAssistantState) -> str:
    wants_appointment = state.get("user_wants_appointment", False)
    
    if wants_appointment:
        return "appointment_booking"
    else:
        return END

def build_medical_assistant_graph():
    builder = StateGraph(MedicalAssistantState)
    
    builder.add_node("analyzer", report_analyzer_agent)
    builder.add_node("doctor_recommender", doctor_recommender_agent)
    builder.add_node("appointment_booking", appointment_booking_agent)
    builder.add_node("notifier", notifier_agent)
    
    builder.set_entry_point("analyzer")
    
    builder.add_conditional_edges(
        "analyzer",
        route_after_analysis,
        {
            END: END,
            "doctor_recommender": "doctor_recommender"
        }
    )
    
    builder.add_conditional_edges(
        "doctor_recommender",
        route_after_recommendation,
        {
            END: END,
            "appointment_booking": "appointment_booking"
        }
    )
    
    builder.add_edge("appointment_booking", "notifier")
    
    builder.add_edge("notifier", END)
    
    return builder.compile()

medical_assistant_app = build_medical_assistant_graph()