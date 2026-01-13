import json
from pathlib import Path
from typing import List, Dict

DOCTOR_AVAILABILITY_FILE = Path("agents/Agent_2_doctor_recommendation/data/doctor_availability.json")

def load_doctor_availability() -> Dict:
    
    if not DOCTOR_AVAILABILITY_FILE.exists():
        return {}
    
    try:
        with open(DOCTOR_AVAILABILITY_FILE, 'r', encoding='utf-8') as f:
            availability_list = json.load(f)
            return {item["DoctorID"]: item for item in availability_list}
    except Exception as e:
        return {}