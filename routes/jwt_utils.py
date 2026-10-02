from functools import wraps

import jwt
from flask import request, session, redirect
from config import Config


def verify_jwt_token(token):

    try:
        payload = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


def jwt_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        token = session.get("jwt_token")

        if not token:
            return redirect("/login")

        payload = verify_jwt_token(token)

        if not payload:
            session.clear()
            return redirect("/login")

        # Keep user information synchronized with the verified token
        session["user_id"] = payload["user_id"]
        session["user_name"] = payload["user_name"]

        return function(*args, **kwargs)

    return decorated_function