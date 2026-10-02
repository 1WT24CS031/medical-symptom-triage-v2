from flask import Blueprint, render_template, session
import mysql.connector

from config import Config
from routes.jwt_utils import jwt_required


history = Blueprint("history", __name__)


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )


# =========================
# HISTORY
# =========================

@history.route("/history")
@jwt_required
def view_history():

    user_id = session["user_id"]

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                symptoms,
                prediction AS predicted_condition,
                created_at
            FROM predictions
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        records = cursor.fetchall()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    return render_template(
        "history.html",
        history=records
    )