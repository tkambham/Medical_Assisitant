from datetime import datetime
import random

def generate_appointment_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = random.randint(1000, 9999)
    return f"APT{timestamp}{random_suffix}"
