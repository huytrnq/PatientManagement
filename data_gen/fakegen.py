import mysql.connector
from faker import Faker
import random
from datetime import datetime

# Initialize Faker
fake = Faker()

# Function to generate a random date between two dates
def random_date(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    random_date = fake.date_between(start_date=start_date, end_date=end_date)
    return random_date

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',         # e.g., 'localhost'
    port=3306,                # e.g., 3306
    database='CareNet',   # Replace with your database name
    user='root',     # Replace with your username
    password='Huytr1997'  # Replace with your password
)

cursor = conn.cursor()

# Function to create fake user data
def create_fake_user(role):
    username = fake.user_name()
    firstname = fake.first_name()
    lastname = fake.last_name()
    gender = random.choice(['male', 'female', 'other'])
    phone = fake.phone_number()
    email = fake.email()
    address = fake.address()
    password = fake.password()  # You should use a proper password hashing in a real scenario
    if role == 'doctor':
        occupation = random.choice(["Oncology Specialist","Pediatrician","ENT Specialist","Cardiologist",
                                    "Dermatologist","Neurologist","Orthopedic Surgeon","Psychiatrist","Rheumatologist",
                                "Gastroenterologist","Endocrinologist","Urologist","Nephrologist","Pulmonologist",
                                "Radiologist","General Practitioner","Obstetrician","Gynecologist","Allergist","Immunologist"])
    else:
        occupation = fake.job()
    license_number = fake.bothify(text='??####') if role == 'doctor' else None
    expiry_date = fake.date_this_century() if role == 'doctor' else None
    date_of_birth = fake.date_of_birth()
    affiliations = fake.company() if role == 'doctor' else None
    profile_path = "default_user.png"

    return (username, firstname, lastname, role, gender, phone, email, address, password,
            occupation, license_number, expiry_date, date_of_birth, affiliations, profile_path)

# Function to create fake medical information
def create_fake_medical_info(user_id):
    weight = round(random.uniform(50, 100), 2)
    height = round(random.uniform(1.5, 2.0), 2)
    allergies = random.choice([
        "Pollen Allergy",
        "Dust Mite Allergy",
        "Pet Allergy",
        "Mold Allergy",
        "Food Allergy",
        "Insect Sting Allergy",
        "Latex Allergy",
        "Drug Allergy",
        "Cockroach Allergy",
        "Perfume Allergy",
        "Nickel Allergy",
        "Bee Sting Allergy",
        "Peanut Allergy",
        "Tree Nut Allergy",
        "Milk Allergy",
        "Egg Allergy",
        "Wheat Allergy",
        "Soy Allergy",
        "Shellfish Allergy",
        "Fish Allergy"
    ])
    current_medication = random.choice([
        "Atorvastatin (Lipitor)",
        "Levothyroxine (Synthroid)",
        "Lisinopril (Prinivil)",
        "Metformin (Glucophage)",
        "Amlodipine (Norvasc)",
        "Metoprolol (Lopressor)",
        "Omeprazole (Prilosec)",
        "Simvastatin (Zocor)",
        "Losartan (Cozaar)",
        "Albuterol (ProAir HFA)",
        "Gabapentin (Neurontin)",
        "Hydrochlorothiazide (Microzide)",
        "Sertraline (Zoloft)",
        "Furosemide (Lasix)",
        "Acetaminophen/Hydrocodone (Vicodin)",
        "Fluticasone (Flonase)",
        "Amoxicillin (Amoxil)",
        "Azithromycin (Zithromax)",
        "Prednisone (Deltasone)",
        "Ibuprofen (Advil, Motrin)"
    ])
    genetic_conditions = random.choice([
        "Cystic Fibrosis",
        "Down Syndrome",
        "Huntington's Disease",
        "Sickle Cell Anemia",
        "Hemophilia",
        "Marfan Syndrome",
        "Duchenne Muscular Dystrophy",
        "Tay-Sachs Disease",
        "Phenylketonuria (PKU)",
        "Fragile X Syndrome",
        "Thalassemia",
        "Turner Syndrome",
        "Klinefelter Syndrome",
        "Neurofibromatosis",
        "Albinism",
        "Achondroplasia",
        "Angelman Syndrome",
        "Prader-Willi Syndrome",
        "Becker Muscular Dystrophy",
        "Williams Syndrome"
    ])
    last_surgery = random_date("2020-01-01", "2024-01-01")
    insurance = random.choice([
        "Allianz Care",
        "AXA PPP Healthcare",
        "Bupa Global",
        "Cigna Global",
        "DKV Seguros",
        "Generali Global Health",
        "Aviva Health",
        "Sanitas",
        "Mapfre Health",
        "Aetna International",
        "PZU Health",
        "Menzis",
        "CZ Groep",
        "Mediq",
        "Achmea",
        "Mutua Madrileña",
        "Uniqa Health",
        "La Mondiale Europartner",
        "Adeslas",
        "VitalityHealth"
    ])
    blood_pressure = f"{random.randint(90, 140)}/{random.randint(60, 90)} mmHg"
    pulse = f"{random.randint(60, 100)} / min"
    abdomen = random.choice([
            "Abdominal Pain",
            "Bloating",
            "Constipation",
            "Diarrhea",
            "Nausea",
            "Vomiting",
            "Heartburn",
            "Indigestion",
            "Cramping",
            "Loss of Appetite",
            "Gas",
            "Swelling",
            "Tenderness",
            "Stomach Cramps",
            "Blood in Stool",
            "Unexplained Weight Loss",
            "Frequent Urination",
            "Abdominal Muscle Spasms",
            "Belching",
            "Feeling Full Quickly"
    ])
    xray_path = ""
    ultrasound_path = ""

    return (user_id, weight, height, allergies, current_medication, genetic_conditions, last_surgery,
            insurance, blood_pressure, pulse, abdomen, xray_path, ultrasound_path)

# Function to create fake appointments
def create_fake_appointment(doctor_id, patient_id):
    date = fake.date_this_year()
    time = fake.time()
    status = random.choice(['scheduled', 'completed', 'cancelled'])
    title = random.choice(['Check-up', 'Follow-up', 'Consultation', 'Treatment', 'Operation', 'Survey', 'Other'])

    return (doctor_id, patient_id, date, time, status, title)

# Insert fake doctors and patients
doctor_ids = []
patient_ids = []

for _ in range(20):  # Insert 20 doctors
    while True:
        user_data = create_fake_user('doctor')
        try:
            cursor.execute("""
                INSERT INTO `user` (username, firstname, lastname, role, gender, phone, email, address, password,
                occupation, license_number, expiry_date, date_of_birth, affiliations, profile_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, user_data)
            doctor_id = cursor.lastrowid
            doctor_ids.append(doctor_id)
            break
        except mysql.connector.errors.IntegrityError:
            continue  # Retry with a new username

for _ in range(500):  # Insert 300 patients
    while True:
        user_data = create_fake_user('patient')
        try:
            cursor.execute("""
                INSERT INTO `user` (username, firstname, lastname, role, gender, phone, email, address, password,
                occupation, license_number, expiry_date, date_of_birth, affiliations, profile_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, user_data)
            patient_id = cursor.lastrowid
            patient_ids.append(patient_id)
            
            # Add medical info for patients
            medical_info_data = create_fake_medical_info(patient_id)
            cursor.execute("""
                INSERT INTO `medical_info` (user_id, weight, height, allergies, current_medication, genetic_conditions,
                last_surgery, insurance, blood_pressure, pulse, abdomen, xray_path, ultrasound_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, medical_info_data)
            break
        except mysql.connector.errors.IntegrityError:
            continue  # Retry with a new username

# Insert fake appointments
for _ in range(300):  # Insert 100 appointments
    doctor_id = random.choice(doctor_ids)
    patient_id = random.choice(patient_ids)
    appointment_data = create_fake_appointment(doctor_id, patient_id)
    cursor.execute("""
        INSERT INTO `appointment` (doctor_id, patient_id, date, time, status, title)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, appointment_data)

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()
