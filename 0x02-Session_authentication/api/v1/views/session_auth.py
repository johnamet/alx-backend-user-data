#!/usr/bin/env python3
"""
The session api view module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
@app_views.route('/auth_session/login/', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    Authenticate a session
    """

    form = request.form

    password = form.get('password')
    email = form.get('email')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({"email": email})

    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_list[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session = auth.create_session(user.id)

    resp = jsonify(User.to_json())

    resp.set_cookie(os.getenv('SESSION_NAME'), session)
    return resp