from flask import jsonify, Blueprint
from flask_restful import Api
from marshmallow import ValidationError

from views.resources.activities import Activities, UserActivities, Activity
from views.resources.blood_test import BloodTests, BloodTestActions, UserBloodTestActions
from views.resources.user import SingleUser, Users, UserHealthScore

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint, errors=blueprint.errorhandler)

api.add_resource(Users, "/users")
api.add_resource(SingleUser, "/users/<user_id>")
api.add_resource(UserBloodTestActions, "/users/<user_id>/blood")
api.add_resource(UserActivities, "/users/<user_id>/<activity>")
api.add_resource(UserHealthScore, "/users/<user_id>/get_health_score")

api.add_resource(Activities, "/<activity>")
api.add_resource(Activity, "/<activity>/<activity_id>")

api.add_resource(BloodTests, "/blood")
api.add_resource(BloodTestActions, "/blood/<blood_test_id>")


@blueprint.errorhandler(ValidationError)
def handle_validation(exp):
    return jsonify(exp.messages)
