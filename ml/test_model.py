import joblib


# Load the trained model pipeline
model = joblib.load("models/model.pkl")


# Test different symptom combinations
test_cases = [
    "fever, cough, sore throat",
    "headache, nausea, vomiting, sensitivity to light",
    "burning urination, frequent urination, lower abdominal pain",
    "wheezing, cough, shortness of breath, chest tightness",
    "sneezing, itchy eyes, runny nose, watery eyes",
    "increased thirst, frequent urination, increased hunger, fatigue"
]


print("====================================")
print("MEDICAL SYMPTOM TRIAGE - MODEL TEST")
print("====================================")


for symptoms in test_cases:

    prediction = model.predict([symptoms])

    print()
    print("Symptoms:", symptoms)
    print("Predicted:", prediction[0])


print()
print("====================================")
print("TEST COMPLETED")
print("====================================")