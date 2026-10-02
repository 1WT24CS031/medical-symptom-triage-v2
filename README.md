# 🩺 Medical Symptom Triage V2

An AI-assisted medical symptom triage web application that allows users to enter symptoms and receive an educational, model-based assessment of a possible condition.

> **Important:** This project is for educational and demonstration purposes only. It is not a medical diagnostic system and should not replace professional medical advice or emergency care.

---

## 📌 Project Overview

**Medical Symptom Triage V2** is an improved version of a machine-learning-based symptom assessment application.

The application combines:

* A **Flask web application**
* A **Machine Learning classification model**
* **MySQL database**
* **JWT-based authentication**
* Secure password hashing
* Prediction history
* Model confidence scores
* Automated testing through GitHub Actions

Users can create an account, log in securely, enter symptoms, view an AI-assisted assessment, and review their previous predictions.

---

## ✨ Features

### 👤 User Authentication

* User registration
* Secure password hashing
* User login and logout
* JWT-based authentication
* Protected dashboard
* Session-based user management
* Automatic password migration for older plain-text passwords

### 🩺 Symptom Assessment

* Enter or select symptoms
* Machine-learning-based prediction
* Display of predicted condition
* Model confidence score
* General triage guidance
* Medical safety disclaimer

### 📋 Prediction History

* Stores previous assessments
* Displays prediction history for the logged-in user
* Users can access only their own prediction records

### 🤖 Machine Learning

* Text-based symptom classification
* TF-IDF vectorization
* Classification model trained on an expanded dataset
* Model evaluation using a held-out test set
* 4-fold cross-validation
* Confusion matrix and evaluation visualizations

### 🗄️ Database

MySQL is used to store:

* User accounts
* Hashed passwords
* Prediction records
* Symptoms
* Predicted conditions
* Confidence scores
* Timestamps

### 🔐 Security

* Password hashing using Werkzeug
* JWT authentication
* Protected routes
* User-specific prediction history
* Environment variables for sensitive configuration
* `.env` excluded from Git using `.gitignore`

### ⚙️ CI

GitHub Actions is configured to automatically install dependencies and verify the project environment.

---

## 🧠 Machine Learning Dataset

The current V2 dataset contains:

* **230 rows**
* **23 conditions**
* **10 synthetic symptom examples per condition**

The dataset is designed for **educational and software-development purposes**.

It does **not** represent real clinical patient data and has not been medically validated.

### Conditions included

The dataset contains conditions such as:

* Allergy
* Asthma
* Diabetes
* Migraine
* UTI
* Viral Respiratory Infection
* And other symptom-based categories

---

## 📊 Model Evaluation

The V2 model was evaluated using a held-out test set and 4-fold cross-validation.

### Test Set

**Accuracy:** 93.10%

### 4-Fold Cross-Validation

| Fold               | Accuracy   |
| ------------------ | ---------- |
| Fold 1             | 96.55%     |
| Fold 2             | 94.83%     |
| Fold 3             | 94.74%     |
| Fold 4             | 96.49%     |
| **Mean**           | **95.65%** |
| Standard Deviation | 0.87%      |

These results represent performance on the project's **synthetic educational dataset**.

They should not be interpreted as medical diagnostic accuracy or clinical performance.

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask
* MySQL
* PyJWT
* Werkzeug

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

### Data Visualization

* Matplotlib
* Seaborn

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Development & Version Control

* Visual Studio Code
* Git
* GitHub
* GitHub Actions

---

## 📂 Project Structure

```text
My Project - V2/
│
├── app.py
├── config.py
├── database.sql
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── dataset/
│   ├── symptoms.csv
│   └── symptoms_backup.csv
│
├── ml/
│   ├── train_model.py
│   └── test_model.py
│
├── models/
│   ├── model.pkl
│   ├── vectorizer.pkl
│   └── confusion_matrix.png
│
├── routes/
│   ├── auth.py
│   ├── predict.py
│   ├── history.py
│   └── jwt_utils.py
│
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── predict.html
│   ├── result.html
│   └── history.html
│
├── static/
│   └── css/
│       └── style.css
│
├── database/
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/1WT24CS031/medical-symptom-triage-v2.git
```

Navigate into the project:

```bash
cd medical-symptom-triage-v2
```

---

## 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure MySQL

Create a MySQL database:

```sql
CREATE DATABASE medical_triage;
```

Then configure the required database settings in your `.env` file.

Example:

```env
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=medical_triage

FLASK_SECRET_KEY=your_flask_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

> Do not upload your `.env` file or real credentials to GitHub.

---

## 5. Set Up Database Tables

Run the SQL commands from:

```text
database.sql
```

This creates the required database tables for users and predictions.

---

## 6. Train the Model

If you want to retrain the machine-learning model:

```bash
python ml/train_model.py
```

The trained model and vectorizer are saved inside:

```text
models/
```

---

## 7. Test the Model

Run:

```bash
python ml/test_model.py
```

This performs sample symptom predictions to verify that the trained model is working.

---

## 8. Run the Flask Application

Start the application:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 🔄 Application Flow

```text
User
  │
  ▼
Register / Login
  │
  ▼
JWT Authentication
  │
  ▼
Dashboard
  │
  ▼
Enter Symptoms
  │
  ▼
TF-IDF Vectorization
  │
  ▼
Machine Learning Model
  │
  ▼
Predicted Condition
  │
  ▼
Confidence Score
  │
  ▼
Save Prediction to MySQL
  │
  ▼
View Result / History
```

---

# 🔐 Authentication Flow

The application uses JWT-based authentication to protect user-specific routes.

When a user logs in:

1. The application verifies the user's credentials.
2. The password is checked against the securely stored password hash.
3. A JWT token is generated.
4. The token is stored in the user's session.
5. Protected routes verify the token before allowing access.

The prediction history also uses the authenticated user's ID so users can access only their own records.

---

# 🤖 Machine Learning Workflow

The machine-learning pipeline follows these general steps:

```text
Symptoms Dataset
       ↓
Data Preparation
       ↓
Text Processing
       ↓
TF-IDF Vectorization
       ↓
Model Training
       ↓
Model Evaluation
       ↓
Save Model + Vectorizer
       ↓
Flask Prediction
```

The saved files are:

```text
models/model.pkl
models/vectorizer.pkl
```

---

# 📈 Confidence Score

The application displays a confidence score generated by the machine-learning model.

The confidence score indicates how strongly the model's output supports the predicted class within the model's learned classification space.

**It is not the probability that the user actually has the condition.**

For this reason, confidence scores should not be interpreted as medical certainty.

---

# 🛡️ Medical Safety Disclaimer

This application is an **educational AI/ML project**.

It:

* Does not provide a medical diagnosis.
* Does not replace a doctor or qualified healthcare professional.
* Should not be used for emergency medical decisions.
* Uses a synthetic, non-clinical dataset.
* Provides model-based educational information only.

If someone is experiencing a serious or emergency medical condition, they should seek appropriate professional or emergency medical care.

---

# 🧪 Testing

The project includes a model testing script:

```bash
python ml/test_model.py
```

Example test cases include symptoms associated with:

* Viral respiratory infection
* Migraine
* UTI
* Asthma
* Allergy
* Diabetes

These tests are intended to verify the software and model pipeline, not to validate medical diagnosis.

---

# 🔄 Version 2 Improvements

Compared with the earlier version, V2 includes improvements such as:

* Expanded symptom dataset
* Improved model evaluation
* Cross-validation
* Prediction confidence score
* JWT authentication
* Secure password hashing
* User-specific prediction history
* Improved database handling
* Protected routes
* CI workflow with GitHub Actions
* Better project organization
* Improved user interface

---

# 🔮 Future Improvements

Possible future improvements include:

* Larger and medically validated datasets
* More robust NLP-based symptom processing
* Additional model comparison
* Improved explainability of predictions
* Better accessibility
* More comprehensive automated testing
* API-based architecture
* Deployment to a cloud platform
* Integration with professional healthcare resources

---

# 📚 Learning Objectives

This project demonstrates practical experience with:

* Python
* Flask
* Machine Learning
* Natural Language Processing concepts
* Scikit-learn
* Pandas
* MySQL
* SQL
* REST-style backend development
* Authentication
* JWT
* Password hashing
* Git and GitHub
* GitHub Actions
* HTML and CSS
* Model evaluation
* Cross-validation
* Software project structure

---

# 👩‍💻 Author

**Suhana Shaikh**

Computer Science / AI-ML Student

GitHub:
https://github.com/1WT24CS031

---

## ⭐ Acknowledgement

This project was developed as an educational project to explore the integration of **Machine Learning, Python, Flask, MySQL, authentication, and web development** into a single application.

---

## ⚠️ Disclaimer

**Medical Symptom Triage is an educational software project and should not be considered a medical device or professional medical advice. The machine-learning model is trained on synthetic data and has not been clinically validated.**
