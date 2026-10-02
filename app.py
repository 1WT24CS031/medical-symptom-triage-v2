from flask import Flask, redirect, url_for

app = Flask(__name__)

# Secret key for Flask sessions
app.secret_key = "medical_symptom_triage_secret_key"


# Import blueprints
from routes.auth import auth
from routes.predict import predict
from routes.history import history


# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(predict)
app.register_blueprint(history)


# Home route
@app.route("/")
def home():
    return redirect(url_for("auth.login"))


# Run application
if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )