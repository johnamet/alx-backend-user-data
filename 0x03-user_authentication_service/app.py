#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, request, jsonify
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
    data = None

    try:
        data = request.get_json(force=True)
    except Exception:
        data = request.form

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Invalid data"}), 400

    email = data['email']
    password = data['password']

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
