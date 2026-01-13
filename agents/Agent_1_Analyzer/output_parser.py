from workflow.state import MedicalAssistantState
import json
from typing import Dict, Any

def parse_llm_response(response_text: str) -> Dict[str, Any]:
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            return {
                "summary": response_text[:500],
                "severity": "mild",
                "department": "general medicine",
                "disease_type": "unknown"
            }
    except Exception as e:
        print(f"⚠️ Error parsing response: {e}")
        return {
            "summary": "Unable to parse medical report",
            "severity": "mild",
            "department": "general medicine",
            "disease_type": "unknown"
        }
