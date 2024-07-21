#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, request, jsonify, abort, redirect, url_for, make_response
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    The index function
    :return: JSON response with a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user():
    """
    Register user
    :return: JSON response with user creation status
    """

    try:
        data = request.get_json(force=True)
    except Exception:
        data = request.form

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Invalid data"}), 400

    email = data['email']
    password = data['password']

    try:
        user = AUTH.register_user(email=email, password=password)

        if user:
            return jsonify({"email": user.email,
                            "message": "user created"}), 200
        else:
            return jsonify({"message": "Invalid data"}), 400

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def register_session():
    """
    Creates a session_id for a user
    :return: jsonify response with session_id creation status
    """

    try:
        data = request.get_json(force=True)
    except Exception:
        data = request.form.to_dict()

    email = data.get("email")
    password = data.get("password")

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Invalid data"}), 400

    login = AUTH.valid_login(email=email, password=password)
    if login:
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response, 200
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs out a user
    :return: jsonify response with session_id deletion status
    """
    cookies = request.cookies
    session_id = cookies.get("session_id")

    if session_id:
        user = AUTH.get_user_from_session_id(session_id=session_id)
        if user:
            print(user)
            AUTH.destroy_session(user_id=user.id)
            return redirect("/"), 302
        else:
            abort(403)
    else:
        abort(403)


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile():
    """
    Profile of the user
    :return: jsonify response with user profile status
    """

    cookies = request.cookies
    session_id = cookies.get("session_id")

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
        else:
            abort(403)
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password():
    """
    Resets the password for a user
    :return: jsonify response with password reset status
    """

    try:
        data = request.get_json(force=True)
    except Exception:
        data = request.form

    email = data.get("email")

    if not data or 'email' not in data:
        abort(403)

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """
    Updates the password for a user
    :return:
    """

    try:
        data = request.get_json(force=True)
    except Exception:
        data = request.form

    email = data.get("email")
    reset_token = data.get("reset_token")
    new_password = data.get("new_password")

    if not data or 'password' not in data or \
            'new_password' not in data or \
            'reset_token' not in data:
        abort(403)
    try:
        AUTH.update_password(reset_password=reset_password,
                             password=new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
