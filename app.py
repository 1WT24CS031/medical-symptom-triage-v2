from flask import Flask, redirect, url_for

from config import Config

app = Flask(__name__)

app.secret_key = Config.FLASK_SECRET_KEY

from routes.auth import auth
from routes.predict import predict
from routes.history import history

app.register_blueprint(auth)
app.register_blueprint(predict)
app.register_blueprint(history)


@app.route("/")
def home():
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )