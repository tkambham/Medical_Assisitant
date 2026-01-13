import json
import random
from faker import Faker

fake = Faker('en_IN')

DOCTOR_COUNT = 100
DOCTOR_AVAILABILITY = 100

INDIAN_CITIES = [
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Delhi",
    "Vijayawada",
    "Chennai",
    "Chandigarh"
]

DOCTOR_QUALIFICATIONS = [
    "MBBS, MD Cardiology",
    "MBBS, MS ENT",
    "MBBS, DM Neurology",
    "MBBS, MD Internal Medicine",
    "MBBS, MS Orthopedics",
    "MBBS, MS OBG",
    "MBBS, MD Dermatology",
    "MBBS, MD Pediatrics",
    "MBBS, DM Gastroenterology",
    "MBBS, DM Endocrinology"
]

HOSPITALS = [
    "Apollo Hospitals",
    "AIIMS",
    "NRI Hospital",
    "Manipal Hospitals",
    "Max Healthcare"
]

# Map speciality from qualifications
SPECIALITY_MAP = {
    "MBBS, MD Cardiology": "Cardiology",
    "MBBS, MS ENT": "ENT",
    "MBBS, DM Neurology": "Neurology",
    "MBBS, MD Internal Medicine": "Internal Medicine",
    "MBBS, MS Orthopedics": "Orthopedics",
    "MBBS, MS OBG": "Obstetrics & Gynecology",
    "MBBS, MD Dermatology": "Dermatology",
    "MBBS, MD Pediatrics": "Pediatrics",
    "MBBS, DM Gastroenterology": "Gastroenterology",
    "MBBS, DM Endocrinology": "Endocrinology"
}

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAY_ABBREVIATIONS = ["M", "T", "W", "Th", "F", "S", "Su"]

# Time slots for appointments (in 24-hour format)
TIME_SLOTS = [
    "09:00 AM - 11:00 AM",
    "11:00 AM - 01:00 PM",
    "02:00 PM - 04:00 PM",
    "04:00 PM - 06:00 PM",
    "06:00 PM - 08:00 PM"
]


def generate_doctors_data():
    """Generate doctors.json data"""
    doctors = []
    
    for i in range(1, DOCTOR_COUNT + 1):
        qualification = random.choice(DOCTOR_QUALIFICATIONS)
        speciality = SPECIALITY_MAP[qualification]
        
        doctor = {
            "DoctorID": f"DOC{str(i).zfill(4)}",  # DOC0001, DOC0002, etc.
            "Name": fake.name(),
            "City": random.choice(INDIAN_CITIES),
            "Speciality": speciality,
            "Hospital": random.choice(HOSPITALS),
            "Experience": f"{random.randint(5, 30)} years",
            "Qualifications": qualification,
            "Email": fake.email(),
            "Phone": fake.phone_number()
        }
        
        doctors.append(doctor)
    
    return doctors


def generate_doctor_availability():
    """Generate doctor_availability.json data"""
    availability_data = []
    
    for i in range(1, DOCTOR_AVAILABILITY + 1):
        doctor_id = f"DOC{str(i).zfill(4)}"
        
        # Randomly select 3-6 days when doctor is available
        num_days = random.randint(3, 6)
        available_days_indices = random.sample(range(7), num_days)
        available_days_indices.sort()
        
        # Create availability schedule
        availability_schedule = {}
        
        for day_idx in available_days_indices:
            day_abbr = DAY_ABBREVIATIONS[day_idx]
            day_full = DAYS_OF_WEEK[day_idx]
            
            # Randomly select 1-3 time slots for each day
            num_slots = random.randint(1, 3)
            selected_slots = random.sample(TIME_SLOTS, num_slots)
            
            availability_schedule[day_abbr] = {
                "day": day_full,
                "time_slots": selected_slots
            }
        
        availability_entry = {
            "DoctorID": doctor_id,
            "AvailabilityDays": list(availability_schedule.keys()),
            "Schedule": availability_schedule
        }
        
        availability_data.append(availability_entry)
    
    return availability_data


def save_to_json(data, filename):
    """Save data to JSON file with proper formatting"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Generated: {filename}")


def main():
    """Main function to generate both JSON files"""
    print("🏥 Generating Doctor Database...\n")
    
    # Generate doctors data
    print("👨‍⚕️ Creating doctors.json...")
    doctors_data = generate_doctors_data()
    save_to_json(doctors_data, "doctors.json")
    print(f"   Total Doctors: {len(doctors_data)}\n")
    
    # Generate availability data
    print("📅 Creating doctor_availability.json...")
    availability_data = generate_doctor_availability()
    save_to_json(availability_data, "doctor_availability.json")
    print(f"   Total Availability Records: {len(availability_data)}\n")
    
    # Display sample data
    print("="*60)
    print("📋 SAMPLE DATA")
    print("="*60)
    
    print("\n🔹 Sample Doctor:")
    print(json.dumps(doctors_data[0], indent=2))
    
    print("\n🔹 Sample Availability:")
    print(json.dumps(availability_data[0], indent=2))
    
    print("\n" + "="*60)
    print("✅ Data generation complete!")
    print("="*60)
    
    # Statistics
    cities_count = {}
    specialities_count = {}
    
    for doc in doctors_data:
        cities_count[doc['City']] = cities_count.get(doc['City'], 0) + 1
        specialities_count[doc['Speciality']] = specialities_count.get(doc['Speciality'], 0) + 1
    
    print("\n📊 STATISTICS:")
    print("\nDoctors by City:")
    for city, count in sorted(cities_count.items()):
        print(f"   {city}: {count} doctors")
    
    print("\nDoctors by Speciality:")
    for spec, count in sorted(specialities_count.items()):
        print(f"   {spec}: {count} doctors")


if __name__ == "__main__":
    main()