from flask import Flask, jsonify, make_response
from flask_cors import cross_origin

import api
import auth

app = Flask(__name__)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello, world!')


@app.route("/user/<email>")
@cross_origin(headers=["Content-Type", "Authorization"])
@auth.requires_auth
@auth.requires_scope('read:users')
def user_by_email(email):
    user = api.get_user_by_email(email)
    return jsonify(data=user)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


@app.errorhandler(auth.AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
