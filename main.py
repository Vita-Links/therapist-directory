from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI()

# ✅ FIXED: CORS Configuration (Allows frontend to access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.105:3000"],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# PostgreSQL Database Connection
DATABASE_URL = os.getenv("DATABASE_URL", "dbname=therapist_db user=postgres password=yourpassword host=therapist-db")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# Therapist Type Response Model
class TherapistTypeResponse(BaseModel):
    therapist_types: List[str]

# Therapist Registration Model
class TherapistCreate(BaseModel):
    name: str
    specialty: str
    location: str
    email: str

# Therapist Response Model
class TherapistResponse(TherapistCreate):
    id: int

# ✅ Root Endpoint (Check if API is running)
@app.get("/")
def read_root():
    return {"message": "Therapist Directory API is running!"}

# ✅ Fetch Therapist Types
@app.get("/therapist-types", response_model=TherapistTypeResponse)
def get_therapist_types():
    therapist_types = [
        "Acupuncturist", "Aromatherapist", "Ayurvedic Practitioner", "Bodywork Therapist",
        "Chiropractor", "Craniosacral Therapist", "Crystal Healer", "Energy Healer",
        "Herbalist", "Holistic Health Coach", "Homeopath", "Hypnotherapist",
        "Integrative Health Practitioner", "Kinesiologist", "Massage Therapist",
        "Meditation Coach", "Naturopathic Doctor", "Nutritional Therapist", "Osteopath",
        "Physiotherapist", "Psychotherapist", "Reiki Practitioner", "Reflexologist",
        "Sound Healer", "Spiritual Healer", "Tai Chi Instructor",
        "Traditional Chinese Medicine (TCM) Practitioner", "Yoga Therapist",
        "Cognitive Behavioral Therapist (CBT)", "Art Therapist", "Music Therapist",
        "Somatic Therapist", "Shamanic Practitioner", "Life Coach", "Breathwork Coach",
        "Functional Medicine Practitioner", "Holistic Nutritionist", "Sports Therapist"
    ]
    return {"therapist_types": therapist_types}

# ✅ Register a Therapist
@app.post("/register", response_model=TherapistResponse)
def register_therapist(therapist: TherapistCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO therapists (name, specialty, location, email) VALUES (%s, %s, %s, %s) RETURNING id",
        (therapist.name, therapist.specialty, therapist.location, therapist.email)
    )

    therapist_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return {**therapist.dict(), "id": therapist_id}

# ✅ Get a Therapist by ID
@app.get("/therapist/{therapist_id}", response_model=TherapistResponse)
def get_therapist(therapist_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, specialty, location, email FROM therapists WHERE id = %s", (therapist_id,))
    therapist = cursor.fetchone()

    cursor.close()
    conn.close()

    if therapist:
        return {"id": therapist[0], "name": therapist[1], "specialty": therapist[2], "location": therapist[3], "email": therapist[4]}
    else:
        raise HTTPException(status_code=404, detail="Therapist not found")

# ✅ Update a Therapist
@app.put("/therapist/{therapist_id}", response_model=TherapistResponse)
def update_therapist(therapist_id: int, therapist: TherapistCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE therapists SET name = %s, specialty = %s, location = %s, email = %s WHERE id = %s RETURNING id",
        (therapist.name, therapist.specialty, therapist.location, therapist.email, therapist_id)
    )

    updated_therapist_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if updated_therapist_id:
        return {**therapist.dict(), "id": therapist_id}
    else:
        raise HTTPException(status_code=404, detail="Therapist not found")

# ✅ Search Therapists
@app.get("/search", response_model=List[TherapistResponse])
def search_therapists(name: str = None, specialty: str = None, location: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, specialty, location, email FROM therapists WHERE TRUE"
    params = []

    if name:
        query += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if specialty:
        query += " AND specialty ILIKE %s"
        params.append(f"%{specialty}%")
    if location:
        query += " AND location ILIKE %s"
        params.append(f"%{location}%")

    cursor.execute(query, tuple(params))
    therapists = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{"id": t[0], "name": t[1], "specialty": t[2], "location": t[3], "email": t[4]} for t in therapists]
