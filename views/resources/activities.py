from datetime import datetime

import pytz
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app import app
from db import db
from models.PhysicalActivity import PhysicalActivity, PhysicalActivitySchema
from models.SleepActivity import SleepActivity, SleepActivitySchema
from models.User import User


def get_activity(activity: str) -> tuple:
    """Return the activity model object and its corresponding schema object."""

    match activity:
        case "physical":
            return PhysicalActivity, PhysicalActivitySchema
        case "sleep":
            return SleepActivity, SleepActivitySchema
        case _:
            raise ValidationError(f"No such activity: {activity}")


class Activities(Resource):
    def get(self, activity: str):
        """Returns all data for the given activity_id."""

        activity, schema = get_activity(activity)

        activity = db.session.execute(db.select(activity).order_by(activity.id)).scalars()
        schema = schema(many=True)

        return schema.dump(activity)


class Activity(Resource):
    def get(self, activity: str, activity_id: int):
        """Returns all data for the given activity_id."""

        activity, schema = get_activity(activity)
        schema = schema()

        if activity := db.session.execute(db.select(activity).filter_by(id=activity_id)).scalar_one_or_none():
            return schema.dump(activity)

        return {"error": "Did not find activity ID."}

    def put(self, activity: str, activity_id: int):
        """Update a single activities' data."""

        app.logger.debug(f"Request payload: {request.json}")

        activity, schema = get_activity(activity)
        schema = schema()
        validated_data = schema.load(request.json)

        if activity := db.session.execute(db.select(activity).filter_by(id=activity_id)).scalar_one_or_none():
            app.logger.debug(f"Current activity data: {activity}")

            for field, updated_value in validated_data.items():
                current_value = getattr(activity, field)

                if current_value != updated_value:
                    app.logger.debug(f"Updated {field}: {current_value} -> {updated_value}")
                    setattr(activity, field, updated_value)

            activity.updatedDateTime = datetime.now(tz=pytz.UTC)

            db.session.commit()

            app.logger.debug("Activity updated successfully.")

            return {
                "response": "Activity updated successfully.",
                "activity": schema.dump(activity)
            }

        return {"error": f"Did not find activity ID {activity_id}"}

    def delete(self, activity: str, activity_id: int):
        """Delete all users' data."""

        activity, schema = get_activity(activity)

        if activity := db.session.execute(db.select(activity).filter_by(id=activity_id)).scalar_one_or_none():
            db.session.delete(activity)
            db.session.commit()

            app.logger.debug(f"Activity {activity_id} removed successfully.")

            return {"response": f"Activity {activity_id} removed."}

        return {"error": f"Did not find activity ID {activity_id}"}


class UserActivities(Resource):
    def get(self, user_id: int, activity: str):
        """Get all information for a single user."""

        activity, schema = get_activity(activity)

        activities = db.session.execute(db.select(activity).filter_by(user_id=user_id)).scalars()
        schema = schema(many=True)

        return schema.dump(activities)

    def post(self, user_id: int, activity: str):
        """Create new activity data for the given user."""

        app.logger.debug(f"Request payload: {request.json}")

        activity, schema = get_activity(activity)
        schema = schema()
        validated_data = schema.load(request.json)

        if db.session.execute(db.select(User).filter_by(id=user_id)).one_or_none():
            new_activity = activity(**validated_data)
            new_activity.user_id = user_id

            db.session.add(new_activity)
            db.session.commit()

            app.logger.debug("Activity added successfully.")

            return {
                "response": "Activity added successfully.",
                "activity": schema.dump(new_activity)
            }

        return {"error": f"Did not find user ID {user_id}"}
