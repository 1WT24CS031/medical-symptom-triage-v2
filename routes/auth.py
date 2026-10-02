from flask import Blueprint, render_template, request, redirect, session
import mysql.connector
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from routes.jwt_utils import jwt_required

auth = Blueprint("auth", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )


def create_jwt_token(user_id, user_name):
    payload = {
        "user_id": user_id,
        "user_name": user_name,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        Config.JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return token


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Hash password before storing it
        hashed_password = generate_password_hash(password)

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, hashed_password)
            )

            connection.commit()

            return redirect("/login")

        except mysql.connector.Error as err:

            if connection:
                connection.rollback()

            return f"Registration Error: {err}"

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            user = cursor.fetchone()

            if not user:
                return "Invalid Login"

            stored_password = user["password"]

            # Check hashed password
            if stored_password.startswith("scrypt:"):

                password_valid = check_password_hash(
                    stored_password,
                    password
                )

            else:

                # Migrate old plaintext password
                password_valid = stored_password == password

                if password_valid:

                    new_hashed_password = generate_password_hash(password)

                    cursor.execute(
                        """
                        UPDATE users
                        SET password = %s
                        WHERE id = %s
                        """,
                        (new_hashed_password, user["id"])
                    )

                    connection.commit()

            if password_valid:

                # Store user information in Flask session
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]

                # Create JWT
                token = create_jwt_token(
                    user["id"],
                    user["name"]
                )

                # Store JWT temporarily in session
                session["jwt_token"] = token

                return redirect("/dashboard")

            return "Invalid Login"

        except mysql.connector.Error as err:

            if connection:
                connection.rollback()

            return f"Login Error: {err}"

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("login.html")


@auth.route("/dashboard")
@jwt_required
def dashboard():

    return render_template("dashboard.html")


@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")