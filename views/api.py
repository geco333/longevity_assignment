from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from blueprints.resources.users import Users

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_blueprint, errors=api_blueprint.errorhandler)

api.add_resource(Users, "/users")
api.add_resource(Users, "/users/<user_id>")


@api_blueprint.errorhandler(ValidationError)
def handle_validation(exp):
    return jsonify(exp.message)
