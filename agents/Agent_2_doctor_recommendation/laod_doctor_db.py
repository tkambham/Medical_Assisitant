import json
from pathlib import Path
from typing import List, Dict

DOCTORS_FILE = Path("agents/Agent_2_doctor_recommendation/data/doctors.json")

def load_doctors_database() -> List[Dict]:
    
    if not DOCTORS_FILE.exists():
        return []
    
    try:
        with open(DOCTORS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return []