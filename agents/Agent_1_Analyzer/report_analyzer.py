from workflow.state import MedicalAssistantState
from .prompts import MEDICAL_ANALYSIS_PROMPT
from .llm_config import get_medical_llm
from .output_parser import parse_llm_response

def report_analyzer_agent(state:MedicalAssistantState) -> MedicalAssistantState:
    input_content = state.get("input_content")
    llm = get_medical_llm()

    input_content = state.get("input_content")

    if not input_content:
        error_msg = "No report text available for analysis."
        state.setdefault("chat_history", []).append(error_msg)
        return state
    
    prompt = MEDICAL_ANALYSIS_PROMPT.format(
        input_content=state["input_content"],
        patient_location=state.get("patient_location", "Not specified")
    )

    try:
        response = llm.invoke(prompt)
        response_text = response.content

        analysis = parse_llm_response(response_text)

        state["report_summary"] = analysis.get("summary", "Analysis completed")
        state["severity"] = analysis.get("severity", "mild").lower()
        state["department"] = analysis.get("department", "general medicine").lower()
        state["disease_type"] = analysis.get("disease_type", "unknown")

        state.setdefault("chat_history", []).append(
            f"Analysis complete - Severity: {state['severity']}, Department: {state['department']}"
        )

    except Exception as e:
        error_msg = f"Error analyzing report: {str(e)}"

        state["report_summary"] = "Error analyzing report. Please consult a doctor."
        state["severity"] = "mild"
        state["department"] = "general medicine"
        state["disease_type"] = "unknown"

        state.setdefault("chat_history", []).append(error_msg)


    return state