# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import random, os
from PIL import Image

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    userId: Optional[str] = None

class ConsultRequest(BaseModel):
    symptoms: str
    age: Optional[int] = None
    gender: Optional[str] = None
    userId: Optional[str] = None

class ImageReq(BaseModel):
    filepath: str
    originalname: Optional[str] = None

# --------- Chatbot endpoint ----------
@app.post("/chatbot")
async def chatbot(q: Query):
    # TODO: integrate real LLM here.
    question = q.question.lower()
    # quick rules for emergency detection (simple)
    # emergency_keywords = ["chest pain", "breath", "shortness", "unconscious", "severe bleeding", "blood"]

    emergency_keywords = [
  "heart pain","heart attack", " chest pain", "pressure in chest",
  "chest tightness", "palpitations", "dil tez dhadak rha h",
  "breath rukna", "saans ruk rahi hai","stroke",  "ek side sun ho gaya", "speech problem",
  "bol nahi pa raha", "chakkar aa rahe hain", "tez sir dard",
  "brain hemorrhage", "vision blur", "behosh ho gaya",
  "accident", "injuries", "bleeding ruk nahi rahi", "fracture",
  "haddi toot gayi", "sir pe chot", "blood bahut nikal raha",
   " asthma attack", "oxygen kam",
  "choking", "saans atak gayi", "breathless ho raha hun",
  "allergy severe", "lips suj gaye", "ankh sujna", "body pe rashes",
  "itching with swelling", "sanse me dikkat allergy se",
  "103 fever", "bohot tez bukhar", "fits", "seizure",
  "shivering uncontrollable", "bachcha tez bukhar"
]
    if any(k in question for k in emergency_keywords):
        return {"answer": "Emergency detected. Please call local emergency services immediately or go to nearest hospital.", "emergency": True}

    # sample reply logic
    replies = [
        "Aap thoda rest karein aur garam paani piyen. Agar 48 ghante me improvement na ho to doctor ko dikhaen.",
        "Yeh lakshan aam taur par infection se jude ho sakte hain. Over-the-counter paracetamol consider karein agar bukhar ho.",
        "Pet dard ke liye halka khana aur adrak ka kadha faydemand ho sakta hai."
    ]
    return {"answer": random.choice(replies), "emergency": False}

# --------- Health consultation logic ----------

@app.post("/consult")
async def consult(c: ConsultRequest):
    s = c.symptoms.lower()
    suggestion = {}
    recommendation = []

    # Fever
    if "fever" in s or "temperature" in s or "flu" in s or "bukhar" in s:
        suggestion = {
            "probable": "Bukhar halki level ka hai ya high? Saath me khansi, ulti ya chills ho rahe hain?",
            "home_remedies": [
                "1. Gunguna paani piyo aur hydrated raho\n"
                "2. Zyada mehnat mat karo, rest lo\n"
                "3. Thandi patti forehead par rakh sakte ho\n"
            ],
            "medicine": [
                "1. Paracetamol 500 mg (agar allergy ya koi problem nahi hai)\n"
                "2. ORS ya nimbu paani agar dehydration lag raha ho"
            ],
                "when_to_see_doctor": "Agar 2 din se zyada rahe, 102°F se upar ho, ya vomiting/breathing issue ho to doctor ko dikhao."
        }
        recommendation.append("Har 4-6 ghante me temperature check karte raho.")

    # Headache / Migraine
    elif "headache" in s or "head pain" in s:
        suggestion = {
            "probable": "Headache kis type ka hai — stress wala, migraine type ya dehydration ki wajah se?",
            "home_remedies": [
            "1. Panni piyo aur dark, quiet room me rest karo\n"
            "2. Forehead ya neck par warm/cold compress lagao\n"
            "3. Screen aur tez light se thoda break lo\n"
        ],
        "medicine": [
            "Paracetamol 500 mg ya ibuprofen (agar suit karta ho)"
        ],
        "when_to_see_doctor": "Agar 2 din se zyada rahe, vomiting, weakness, ya vision change ho to turant doctor ko dikhao."
        }
        recommendation.append("Triggers jaise stress, food, ya नींद observe karo.")

# Cough & Cold / Sore throat
    elif "cough" in s or "cold" in s or "sore throat" in s:
        suggestion = {
            "probable": "Cough dry hai ya saath me khich-khich, balgam ya fever bhi hai?",
            "home_remedies": [
                "1. Garm paani ya honey-lemon water piyo (agar >1 saal age ho)\n"
                "2. Steam inhalation lo ya namak wale garam paani se gargle karo\n"
                "3. Dhool, smoke aur thandi cheeze avoid karo\n"
            ],
                "medicine": [
                "1. Dry cough ke liye dextromethorphan syrup\n"
                "2. Balgam ho to expectorant syrup (doctor ke kehne par)\n"
        ],
        "when_to_see_doctor": "Agar 7 din se zyada rahe, saans lene me dikkat ho ya high fever ho to consult karo."
        }
        recommendation.append("Agar asthma ya lung problem ho to delay mat karo.")

# Throat infection / Tonsillitis
    elif "throat" in s or "tonsillitis" in s:
        suggestion = {
            "probable": "Gala bahut dard kar raha hai ya nigalne me dikkat ho? White spots ya swelling bhi hai?",
            "home_remedies": [
                "1. Namak wale warm water se gargle karo\n"
                "2. Soft aur light food lo\n"
                "3. Hydrated raho\n"
            ],
            "medicine": [
                "1. Dard ke liye paracetamol le sakte ho\n"
                "2. Agar bacterial infection ho to doctor antibiotic suggest karega\n"
            ],
            "when_to_see_doctor": "Agar bukhar high ho, gala band ho, ya swelling zyada ho to doctor ko dikhao."
        }
        recommendation.append("Antibiotics bina checkup ke mat lo.")

        # Stomach pain / Abdominal pain
    elif "stomach" in s or "abdominal" in s or "stomach pain" in s:
        suggestion = {
            "probable": "Dard pet ke ek side hai ya pura? Saath me vomiting, gas ya fever bhi hai?",
            "home_remedies": [
                "1. Halka khana lo jaise khichdi, daliya ya banana\n"
                "2. Gunguna paani piyo\n"
                "3. Pet pe warm compress rakh sakte ho cramps ke liye\n"
            ],
            "medicine": [
                "1. Antacid agar acidity related pain ho\n"
                "2. Gas ke liye simethicone (doctor ki salah se)\n"
            ],
            "when_to_see_doctor": "Agar dard zyada ho, vomiting band na ho, ya 1-2 din me relief na mile."
        }
        recommendation.append("Agar dard achanak aur sharp ho to emergency check karao.")

        # Vomiting / Nausea
    elif "vomit" in s or "vomiting" in s or "nausea" in s:
        suggestion = {
            "probable": "Lagatar ulti ho rahi hai ya thodi-thodi? Bukhar, pet dard ya dehydration bhi hai?",
            "home_remedies": [
                "1. Chhote ghunto me ORS ya nimbu paani piyo\n"
                "2. Jab tak ulti rong na ho, solid food avoid karo\n"
                "3. Adrak ka paani ya choti sip help karega\n"
            ],
            "medicine": [
                "1. Ondansetron sirf doctor ki salah se\n"
                "2. ORS mandatory hai dehydration rokne ke liye\n"
            ],
            "when_to_see_doctor": "Agar 6 ghante se zyada ho raha ho, khoon aa raha ho ya kuch digest na ho raha ho."
        }
        recommendation.append("Dehydration avoid karo warna drip lag sakti hai.")

    # Diarrhea / Loose motion
    elif "diarrhea" in s or "loose motion" in s:
        suggestion = {
            "probable": "Stool watery hai ya blood aa raha hai? Bukhar ya pet dard bhi saath hai?",
            "home_remedies": [
                "1. ORS regular piyo\n"
                "2. BRAT diet follow karo (banana, rice, apple sauce, toast)\n"
                "3. Dahi, oily aur spicy food avoid karo\n"
            ],
            "medicine": [
                "1. ORS sachets must\n"
                "2. Zinc supplement (bachon me)\n"
            ],
            "when_to_see_doctor": "Agar 2 din se zyada chale, weakness ho ya stool me blood ho."
        }
        recommendation.append("Hydration sabse zaruri hai diarrhea me.")

    # Acidity / Gas / Heartburn
    elif "acidity" in s or "heartburn" in s or "gas" in s or "indigestion" in s:
        suggestion = {
            "probable": "Acidity khane ke baad hoti hai ya बार-बार? Kya spicy aur oily food trigger karta hai?",
            "home_remedies": [
                "1. Chhota aur frequent meal lo\n"
                "2. Sone se pehle heavy food avoid karo\n"
                "3. Paani piyo aur thoda walk karo\n"
            ],
            "medicine": [
                "1. Antacid jaldi relief ke liye\n"
                "2. Pantoprazole ya omeprazole (doctor advice se)\n"
            ],
            "when_to_see_doctor": "Agar frequently ho raha ho ya chest pain ke sath."
        }
        recommendation.append("Smoking, coffee aur junk food kam karo.")

    # Skin allergy / Itching
    elif "allergy" in s or "itch" in s or "itching" in s or "hives" in s:
        suggestion = {
            "probable": "Kya itching body ke ek part tak hai ya sab jagah? Koi naya food, soap ya medicine use kiya?",
            "home_remedies": [
                "1. Cool compress lagao\n"
                "2. Fragrance-free moisturizer lagao\n"
                "3. Cotton loose kapde pehno\n"
            ],
            "medicine": [
                "1. Cetirizine ya loratadine itching ke liye\n"
                "2. Topical steroid cream sirf doctor ke kehne par\n"
            ],
            "when_to_see_doctor": "Agar face/lips swell ho rahe ho ya breathing issue ho."
        }
        recommendation.append("Agar anaphylaxis ho raha ho to emergency call karo.")

    # Rash
    elif "rash" in s or "red spots" in s or "eruption" in s:
        suggestion = {
            "probable": "Rash khujli wala hai, spread ho raha hai ya fever ke saath hai?",
            "home_remedies": [
                "1. Narm paani se clean karo aur dry rakho\n"
                "2. Scratch mat karo\n"
                "3. Cold compress laga sakte ho\n"
            ],
            "medicine": [
                "1. Emollient cream dryness ke liye\n"
                "2. Steroid cream sirf doctor ke kehne par\n"
            ],
            "when_to_see_doctor": "Agar rash rapidly spread ho ya pus aaye."
        }
        recommendation.append("Self medication avoid karo, especially steroids.")

        # Burns
    elif "burn" in s or "burns" in s:
        suggestion = {
            "probable": "Jala कितना gehra hai? Sirf lalpan hai ya phir blisters/phaaphole bhi bane hain?",
            "home_remedies": [
                "1. Thande paani ke neeche 10–15 min tak burn area rakho\n"
                "2. Saaf kapde ya sterile gauze se cover karo\n"
                "3. Ice direct mat lagao\n"
            ],
            "medicine": [
                "1. Antiseptic cream ya burn ointment\n"
                "2. Dard ke liye paracetamol\n"
            ],
            "when_to_see_doctor": "Agar bada area ho, chehre/haath/par jala ho ya infection ka doubt ho."
        }
        recommendation.append("Severe burn me turant hospital jana chahiye.")

    # Body aches / Myalgia
    elif "body pain" in s or "body ache" in s or "muscle pain" in s:
        suggestion = {
            "probable": "Dard pura sharir me hai (flu type) ya specific muscle/joint me?",
            "home_remedies": [
                "1. Rest karo aur halki stretching kar sakte ho\n"
                "2. Gunguna paani ya warm shower helpful hai\n"
                "3. Hydrated raho\n"
            ],
            "medicine": [
                "Paracetamol ya ibuprofen agar suit kare"
            ],
            "when_to_see_doctor": "Agar pain ke sath swelling, redness, fever ya injury ho."
        }
        recommendation.append("Agar dard long-term ho to checkup zaruri hai.")

    # Eye infection / Conjunctivitis
    elif "eye" in s or "conjunctivitis" in s or "red eye" in s:
        suggestion = {
            "probable": "Aankh lal hai, paani ya discharge aa raha hai, ya light se problem ho rahi hai?",
            "home_remedies": [
                "1. Gungune paani se aankh saaf rakho\n"
                "2. Cold ya warm compress laga sakte ho\n"
                "3. Aankh ko rub mat karo\n"
            ],
            "medicine": [
                "1. Lubricating eye drops\n"
                "2. Antibiotic drops sirf doctor ke kehne par\n"
            ],
            "when_to_see_doctor": "Agar dard, vision blur ya zyada discharge ho."
        }
        recommendation.append("Contact lenses ho to use mat karo jab tak thik na ho.")

    # Ear pain / Infection
    elif "ear" in s or "earache" in s or "ear pain" in s:
        suggestion = {
            "probable": "Kya ear me discharge, block feeling ya hearing loss bhi aa raha hai?",
            "home_remedies": [
                "1. Warm compress ear ke bahar se laga sakte ho\n"
                "2. Kaan me kuch insert mat karo\n"
            ],
            "medicine": [
                "1. Dard ke liye paracetamol\n"
                "2. Antibiotic ya eardrops doctor ke according\n"
            ],
            "when_to_see_doctor": "Agar pain severe ho ya discharge dikhe."
        }
        recommendation.append("Bacho ke ear pain me delay mat karo.")

    # Toothache / Dental pain
    elif "tooth" in s or "toothache" in s or "dental" in s:
        suggestion = {
            "probable": "Dard sharp hai ya dull? Swelling, fever ya sensitivity bhi hai?",
            "home_remedies": [
                "1. Warm salt water se gargle karo\n"
                "2. Cold pack cheek pe laga sakte ho\n"
                "3. Hard/very hot/cold cheeze avoid karo\n"
            ],
            "medicine": [
                "Paracetamol ya ibuprofen dard ke liye"
            ],
            "when_to_see_doctor": "Agar swelling, pus ya continuous pain ho to dentist dikhao."
        }
        recommendation.append("Self filling ya random gel mat use karo.")

    # Period pain / Menstrual cramps
    elif "period" in s or "menstrual" in s or "cramps" in s:
        suggestion = {
            "probable": "Cramps mild hain ya severe bleeding ke sath dard ho raha hai?",
            "home_remedies": [
                "1. Hot water bottle lower abdomen pe rakho\n"
                "2. Thoda stretching ya walk helpful ho sakta hai\n"
                "3. Paani aur diet pe dhyan do\n"
            ],
            "medicine": [
                "Ibuprofen ya meftal spas doctor ki salah se"
            ],
            "when_to_see_doctor": "Agar bleeding zyada ho, irregular cycles ya unbearable pain ho."
        }
        recommendation.append("Track karo ki pain har cycle same pattern me hai ya nahi.")

        # Asthma / Breathing issues
    elif "asthma" in s or "wheeze" in s or "breath" in s or "shortness" in s:
        suggestion = {
            "probable": "Saans lene me dikkat sudden hai ya purani problem hai? Wheezing, chest tightness ya cough bhi hai?",
            "home_remedies": [
                "1. Seedhe baitho aur deep breathing karo\n"
                "2. Agar inhaler doctor ne diya hai to use karo\n"
                "3. Dhool, smoke aur cold air se door raho\n"
            ],
            "medicine": [
                "1. Salbutamol inhaler agar prescribed ho\n"
                "2. Controller inhaler regular use karo doctor ke kehne par\n"
            ],
            "when_to_see_doctor": "Agar saans lene me zyada problem ho, lips blue ho ya inhaler kaam na kare."
        }
        recommendation.append("Asthma action plan follow karo agar doctor ne diya ho.")

    # Diabetes / Sugar issues
    elif "diabetes" in s or "blood sugar" in s or "sugar" in s:
        suggestion = {
            "probable": "Kya bar-bar pyaas, frequent urine, weakness ya weight loss ho raha hai?",
            "home_remedies": [
                "1. Cheeni aur sugary drinks avoid karo\n"
                "2. Fiber-rich diet lo aur hydrated raho\n"
                "3. Regular walking helpful hai\n"
            ],
            "medicine": [
                "Aapki prescribed diabetes wali medicine lo, bina skip kiye"
            ],
            "when_to_see_doctor": "Agar sugar high ho, confusion, chakkar ya dehydration feel ho."
        }
        recommendation.append("Sugar monitor karo aur values note karo.")

    # High BP / Hypertension
    elif "bp" in s or "blood pressure" in s or "hypertension" in s:
        suggestion = {
            "probable": "Sir dard, dizziness, ya chest pressure feel ho raha hai? Ya BP high reading aayi?",
            "home_remedies": [
                "1. Salt kam karo aur pani theek se lo\n"
                "2. Stress avoid karo, deep breathing try karo\n"
                "3. Thoda walk daily helpful hai\n"
            ],
            "medicine": [
                "Prescribed BP tablet time pe lo"
            ],
            "when_to_see_doctor": "Agar BP bahut high ho (>180/120) ya chest pain/vision change ho."
        }
        recommendation.append("Regular monitoring zaruri hai.")

    # Weakness / Fatigue
    elif "weak" in s or "fatigue" in s or "tired" in s or "weakness" in s:
        suggestion = {
            "probable": "Weakness sudden aayi hai ya dheere dheere badh rahi hai? Saath me fever, weight loss ya dizziness to nahi?",
            "home_remedies": [
                "1. Paani aur nutrition pe focus karo\n"
                "2. Sufficient sleep lo\n"
                "3. Light activity ya stretching try karo\n"
            ],
            "medicine": [
                "Multivitamin ya supplements sirf doctor ke advice se"
            ],
            "when_to_see_doctor": "Agar weakness persistent ho ya sath me kisi aur symptoms ke sath ho."
        }
        recommendation.append("Blood test ya checkup ki zarurat ho sakti hai.")

    # Default fallback
    else:
        suggestion = {
            "probable": "Symptoms clear nahin lage — thoda aur explain kar sakte ho? Kab se hai aur kaisa feel ho raha hai?",
            "home_remedies": [
                "1. Paani piyo aur rest karo\n"
                "2. Triggers observe karo (khana, stress, activity)\n"
            ],
            "medicine": [
                "OTC painkiller sirf zarurat ho to lo"
            ],
            "when_to_see_doctor": "Agar symptoms worsen ho ya samajh na aaye to doctor se milo."
        }
        recommendation.append("Thoda aur details doge to better guide kar paunga.")

    return {
    "suggestion": suggestion,
    "recommendation": recommendation
}



# --------- Image analysis endpoint ----------
@app.post("/analyze-image")
async def analyze_image(req: ImageReq):
    fp = req.filepath
    if not os.path.exists(fp):
        return {"error": "file_not_found"}
    # Basic sanity: open image to validate
    try:
        img = Image.open(fp)
        w,h = img.size
    except Exception as e:
        return {"error": "invalid_image", "detail": str(e)}

    # Dummy image classification heuristics (placeholder)
    # e.g., if width>height -> maybe document/photo etc.
    result = {"originalname": req.originalname, "width": w, "height": h, "analysis": []}
    # Fake rule examples
    if w > h:
        result["analysis"].append("Looks like a photo (landscape). Could be non-skin image.")
    else:
        result["analysis"].append("Portrait image. If this is a skin lesion image, ensure good lighting.")
    # For emergency detection example:
    # return some likely tags
    result["tags"] = ["skin", "lesion_candidate"] if "skin" in req.originalname.lower() else ["general"]
    return result

# health recommendations endpoint (can be called by frontend)
@app.post("/recommend")
async def recommend(body: dict):
    # body can contain userId or recent history - placeholder
    # Return some generic personalized suggestions
    return {"recommendations": ["Drink 2-3L water daily", "Walk 30 mins daily", "If chronic symptoms, see specialist"]}




