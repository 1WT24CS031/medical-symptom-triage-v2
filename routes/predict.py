from flask import Blueprint, render_template, request, session, redirect
import joblib
import mysql.connector
from config import Config
from routes.jwt_utils import jwt_required
import os


predict = Blueprint("predict", __name__)


# =====================================================
# LOAD ML MODEL
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "model.pkl"
)

# V2 model = TF-IDF + Logistic Regression Pipeline
model = joblib.load(MODEL_PATH)


# =====================================================
# DISEASE INFORMATION
# =====================================================

disease_info = {

    "Common Cold": {
        "description": "A common viral infection that may cause a runny nose, cough, sore throat and mild fever.",
        "next_step": "Rest, drink enough fluids and monitor how you feel. If symptoms become severe or continue for a long time, consider consulting a healthcare professional."
    },

    "Flu": {
        "description": "Influenza may cause fever, cough, fatigue, body aches and other respiratory symptoms.",
        "next_step": "Rest and stay hydrated. Seek medical advice if symptoms are severe or getting worse."
    },

    "Allergy": {
        "description": "Allergies can cause sneezing, itchy eyes, runny nose, watery eyes or nasal congestion.",
        "next_step": "Try to identify possible triggers and monitor your symptoms. Consult a healthcare professional if symptoms are persistent or troublesome."
    },

    "Migraine": {
        "description": "A migraine can cause moderate to severe headache and may be associated with nausea or sensitivity to light.",
        "next_step": "Rest in a quiet environment and keep track of your symptoms. Seek professional advice if headaches are severe, unusual or recurring."
    },

    "Gastroenteritis": {
        "description": "Gastroenteritis can cause symptoms such as nausea, vomiting, diarrhea and stomach discomfort.",
        "next_step": "Stay hydrated and monitor your symptoms. Consider medical advice if symptoms are severe or persistent."
    },

    "Urinary Tract Infection": {
        "description": "A urinary tract infection may cause burning during urination, frequent urination and lower abdominal discomfort.",
        "next_step": "Consider speaking with a healthcare professional for proper evaluation, especially if symptoms are persistent or severe."
    },

    "Viral Respiratory Infection": {
        "description": "Viral respiratory infections may cause symptoms such as cough, sore throat, congestion, fever or fatigue.",
        "next_step": "Rest, stay hydrated and monitor your symptoms. Seek medical attention if breathing becomes difficult or symptoms become severe."
    },

    "Tonsillitis": {
        "description": "Tonsillitis can cause sore throat, swollen tonsils, difficulty swallowing and sometimes fever.",
        "next_step": "Stay hydrated and monitor your symptoms. Consider medical evaluation if symptoms are severe or persistent."
    },

    "Acid Reflux": {
        "description": "Acid reflux can cause heartburn, chest discomfort, sour taste or irritation in the throat.",
        "next_step": "Monitor your symptoms and consider professional advice if symptoms are frequent, severe or persistent."
    },

    "Constipation": {
        "description": "Constipation can involve infrequent bowel movements, hard stools or difficulty passing stool.",
        "next_step": "Stay hydrated, maintain a balanced diet and monitor your symptoms. Seek medical advice if symptoms are severe or persistent."
    },

    "Iron Deficiency Anemia": {
        "description": "Iron deficiency anemia may cause fatigue, weakness, dizziness or shortness of breath.",
        "next_step": "Consider medical testing and professional evaluation rather than relying on symptoms alone for diagnosis."
    },

    "Diabetes": {
        "description": "Possible symptoms can include increased thirst, frequent urination, increased hunger and fatigue.",
        "next_step": "A symptom-based prediction cannot diagnose diabetes. Consider getting appropriate medical testing and professional evaluation."
    },

    "Asthma": {
        "description": "Asthma can cause symptoms such as wheezing, coughing, chest tightness and shortness of breath.",
        "next_step": "Monitor your breathing symptoms. If you experience severe difficulty breathing, seek emergency medical care."
    },

    "Arthritis": {
        "description": "Arthritis can involve joint pain, stiffness, swelling or reduced movement.",
        "next_step": "Monitor your symptoms and consider professional evaluation if pain, swelling or stiffness persists."
    },

    "Eczema": {
        "description": "Eczema can cause dry, itchy, inflamed or irritated skin.",
        "next_step": "Avoid known irritants and keep the skin moisturized. Consider professional advice if symptoms are persistent or severe."
    },

    "Muscle Strain": {
        "description": "A muscle strain can cause localized pain, tenderness, stiffness or discomfort after physical activity.",
        "next_step": "Rest the affected area and monitor your symptoms. Seek medical advice if pain is severe or does not improve."
    },

    "Dental Problem": {
        "description": "Dental problems can cause tooth pain, sensitivity, gum discomfort or swelling.",
        "next_step": "Consider scheduling an evaluation with a dental professional, particularly if pain or swelling persists."
    },

    "Ear Infection": {
        "description": "An ear infection may cause ear pain, pressure, reduced hearing or other ear-related symptoms.",
        "next_step": "Consider professional medical evaluation, especially if pain is severe, persistent or accompanied by fever."
    },

    "Sinusitis": {
        "description": "Sinusitis may cause facial pressure, nasal congestion, headache or thick nasal discharge.",
        "next_step": "Monitor your symptoms and consider medical advice if symptoms are severe, persistent or worsening."
    },

    "Vertigo": {
        "description": "Vertigo can cause a sensation of spinning, dizziness or loss of balance.",
        "next_step": "Avoid activities that could cause injury while dizzy and consider professional medical evaluation, particularly if symptoms are sudden or severe."
    },

    "Insomnia": {
        "description": "Insomnia can involve difficulty falling asleep, staying asleep or getting enough restful sleep.",
        "next_step": "Maintain a regular sleep schedule and monitor your sleep pattern. Consider professional advice if sleep problems persist."
    },

    "Anxiety": {
        "description": "Anxiety may involve excessive worry, nervousness, restlessness or physical symptoms such as a rapid heartbeat.",
        "next_step": "Monitor your symptoms and consider speaking with a qualified healthcare professional if they persist or interfere with daily life."
    },

    "Depressive Symptoms": {
        "description": "Depressive symptoms may include persistent sadness, loss of interest, low energy or changes in sleep and appetite.",
        "next_step": "Consider speaking with a qualified healthcare professional for proper evaluation and support."
    }
}


# =====================================================
# TRIAGE INFORMATION
# =====================================================

triage_info = {

    "Common Cold": {
        "level": "Non-Urgent",
        "message": "Your result does not usually require immediate medical attention. Rest, stay hydrated and monitor your symptoms."
    },

    "Allergy": {
        "level": "Non-Urgent",
        "message": "This result is generally non-urgent. Monitor your symptoms and consider medical advice if they persist or become troublesome."
    },

    "Acid Reflux": {
        "level": "Non-Urgent",
        "message": "Monitor your symptoms and consider professional advice if they become frequent, severe or persistent."
    },

    "Constipation": {
        "level": "Non-Urgent",
        "message": "This result is generally non-urgent. Maintain hydration and monitor your symptoms."
    },

    "Eczema": {
        "level": "Non-Urgent",
        "message": "This result is generally non-urgent. Monitor your symptoms and consider professional advice if they persist or become severe."
    },

    "Insomnia": {
        "level": "Non-Urgent",
        "message": "Monitor your sleep pattern and consider professional advice if sleep problems persist."
    },

    "Migraine": {
        "level": "Moderate",
        "message": "Consider consulting a healthcare professional, particularly if the headache is severe, unusual, persistent or recurring."
    },

    "Urinary Tract Infection": {
        "level": "Moderate",
        "message": "Consider consulting a healthcare professional for proper evaluation, especially if symptoms are persistent or worsening."
    },

    "Diabetes": {
        "level": "Moderate",
        "message": "A symptom-based prediction cannot diagnose diabetes. Consider appropriate medical testing and professional evaluation."
    },

    "Flu": {
        "level": "Moderate",
        "message": "Monitor your symptoms and consider medical advice if symptoms are severe, persistent or getting worse."
    },

    "Gastroenteritis": {
        "level": "Moderate",
        "message": "Stay hydrated and monitor your condition. Seek medical care if symptoms become severe or signs of dehydration occur."
    },

    "Anxiety": {
        "level": "Moderate",
        "message": "Consider speaking with a qualified healthcare professional if symptoms persist or interfere with daily life."
    },

    "Depressive Symptoms": {
        "level": "Moderate",
        "message": "Consider speaking with a qualified healthcare professional for proper evaluation and support."
    },

    "Iron Deficiency Anemia": {
        "level": "Moderate",
        "message": "Consider appropriate medical testing and professional evaluation rather than relying only on symptoms."
    },

    "Arthritis": {
        "level": "Moderate",
        "message": "Consider professional evaluation if joint pain, swelling or stiffness persists."
    },

    "Muscle Strain": {
        "level": "Moderate",
        "message": "Rest the affected area and monitor your symptoms. Seek medical advice if pain is severe or does not improve."
    },

    "Dental Problem": {
        "level": "Moderate",
        "message": "Consider dental evaluation, especially if pain or swelling persists."
    },

    "Ear Infection": {
        "level": "Moderate",
        "message": "Consider professional medical evaluation if pain is severe, persistent or accompanied by fever."
    },

    "Sinusitis": {
        "level": "Moderate",
        "message": "Monitor your symptoms and consider medical advice if symptoms are severe, persistent or worsening."
    },

    "Tonsillitis": {
        "level": "Moderate",
        "message": "Stay hydrated and consider medical evaluation if symptoms are severe or persistent."
    },

    "Vertigo": {
        "level": "Moderate",
        "message": "Avoid activities that could cause injury while dizzy and consider professional medical evaluation."
    },

    "Viral Respiratory Infection": {
        "level": "Moderate",
        "message": "Monitor your symptoms and seek medical attention if breathing becomes difficult or symptoms become severe."
    },

    "Asthma": {
        "level": "Urgent",
        "message": "Breathing problems can become serious. Seek prompt medical attention, especially if you are experiencing severe difficulty breathing."
    }
}


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_db_connection():

    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )


# =====================================================
# HEALTH CHECK / PREDICTION
# =====================================================

@predict.route("/predict", methods=["GET", "POST"])
@jwt_required
def prediction():

    # -------------------------------------------------
    # GET REQUEST
    # -------------------------------------------------

    if request.method == "GET":

        return render_template("predict.html")


    # -------------------------------------------------
    # GET USER SYMPTOMS
    # -------------------------------------------------

    symptoms = request.form.get(
        "symptoms",
        ""
    ).strip()


    # Check empty input
    if not symptoms:

        return render_template(
            "predict.html",
            error="Please enter at least one symptom."
        )


    # -------------------------------------------------
    # ML PREDICTION
    # -------------------------------------------------

    disease = model.predict(
        [symptoms]
    )[0]


    # -------------------------------------------------
    # CONFIDENCE SCORE
    # -------------------------------------------------

    confidence_score = None


    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            [symptoms]
        )[0]


        confidence_score = max(
            probabilities
        ) * 100


        confidence_score = round(
            confidence_score,
            2
        )


    # -------------------------------------------------
    # DISEASE INFORMATION
    # -------------------------------------------------

    info = disease_info.get(

        disease,

        {
            "description":
                "This result represents the closest match found by the current educational dataset.",

            "next_step":
                "Monitor your symptoms and consider speaking with a qualified healthcare professional if symptoms continue or become concerning."
        }
    )


    # -------------------------------------------------
    # TRIAGE INFORMATION
    # -------------------------------------------------

    triage = triage_info.get(

        disease,

        {
            "level": "Moderate",

            "message":
                "Consider speaking with a qualified healthcare professional if your symptoms continue, worsen or become concerning."
        }
    )


    # =================================================
    # SAVE PREDICTION + CONFIDENCE TO MYSQL
    # =================================================

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()


        cursor.execute(

            """
            INSERT INTO predictions
            (
                user_id,
                symptoms,
                prediction,
                confidence_score
            )
            VALUES (%s, %s, %s, %s)
            """,

            (
                session["user_id"],
                symptoms,
                disease,
                confidence_score
            )
        )


        connection.commit()


        # Get newly created prediction ID
        prediction_id = cursor.lastrowid


    except mysql.connector.Error as err:

        if connection:

            connection.rollback()


        return f"Prediction Database Error: {err}", 500


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()


    # =================================================
    # SHOW RESULT PAGE
    # =================================================

    return render_template(

        "result.html",

        prediction_id=prediction_id,

        disease=disease,

        symptoms=symptoms,

        confidence_score=confidence_score,

        description=info["description"],

        next_step=info["next_step"],

        triage_level=triage["level"],

        triage_message=triage["message"]
    )


# =====================================================
# VIEW OLD RESULT
# =====================================================

@predict.route("/result/<int:prediction_id>")
@jwt_required
def view_result(prediction_id):

    user_id = session["user_id"]

    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(

            """
            SELECT
                id,
                symptoms,
                prediction,
                confidence_score,
                created_at
            FROM predictions
            WHERE id = %s
            AND user_id = %s
            """,

            (
                prediction_id,
                user_id
            )
        )


        record = cursor.fetchone()


    except mysql.connector.Error as err:

        return f"Database Error: {err}", 500


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()


    # -------------------------------------------------
    # RESULT NOT FOUND
    # -------------------------------------------------

    if not record:

        return "Assessment not found", 404


    disease = record["prediction"]


    # -------------------------------------------------
    # DISEASE INFORMATION
    # -------------------------------------------------

    info = disease_info.get(

        disease,

        {
            "description":
                "This result represents the closest match found by the current educational dataset.",

            "next_step":
                "Monitor your symptoms and consider speaking with a qualified healthcare professional if symptoms continue or become concerning."
        }
    )


    # -------------------------------------------------
    # TRIAGE INFORMATION
    # -------------------------------------------------

    triage = triage_info.get(

        disease,

        {
            "level": "Moderate",

            "message":
                "Consider speaking with a qualified healthcare professional if your symptoms continue, worsen or become concerning."
        }
    )


    # =================================================
    # SHOW OLD RESULT
    # =================================================

    return render_template(

        "result.html",

        prediction_id=record["id"],

        disease=disease,

        symptoms=record["symptoms"],

        confidence_score=record["confidence_score"],

        description=info["description"],

        next_step=info["next_step"],

        triage_level=triage["level"],

        triage_message=triage["message"]
    )