from datetime import datetime

import pytz
from flask import request
from flask_restful import Resource

from app import app
from db import db
from models.PhysicalActivity import PhysicalActivity, PhysicalActivitySchema
from models.SleepActivity import SleepActivity, SleepActivitySchema
from models.User import User


class Activities(Resource):
    def get(self):
        """Returns a list of all entities in the physical_activity table."""

        users = db.session.execute(db.select(PhysicalActivity).order_by(PhysicalActivity.id)).scalars()
        schema = PhysicalActivitySchema(many=True)

        return schema.dump(users)


class SinglePhysicalActivity(Resource):
    def get(self, activity_id: int):
        """Returns all data for the given activity_id."""

        if activity := db.session.execute(db.select(PhysicalActivity).filter_by(id=activity_id)).scalar_one_or_none():
            schema = PhysicalActivitySchema()

            return schema.dump(activity)

        return {"error": "Did not find activity ID."}

    def put(self, activity_id: int):
        """Update a single activities' data."""

        app.logger.debug(f"Request payload: {request.json}")

        schema = PhysicalActivitySchema()
        validated_data = schema.load(request.json)

        if activity := db.session.execute(db.select(PhysicalActivity).filter_by(id=activity_id)).scalar_one_or_none():
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

    def delete(self, activity_id: int):
        """Delete all users' data."""

        if activity := db.session.execute(db.select(PhysicalActivity).filter_by(id=activity_id)).scalar_one_or_none():
            db.session.delete(activity)
            db.session.commit()

            app.logger.debug(f"Activity {activity_id} removed successfully.")

            return {"response": f"Activity {activity_id} removed."}

        return {"error": f"Did not find activity ID {activity_id}"}


class UserActivities(Resource):
    @staticmethod
    def _get_activity(activity: str) -> tuple:
        match activity:
            case "physical":
                return PhysicalActivity, PhysicalActivitySchema
            case "sleep":
                return SleepActivity, SleepActivitySchema
            case _:
                raise Exception()

    def get(self, user_id: int, activity: str):
        """Get all information for a single user."""

        activity, schema = self._get_activity(activity)

        activities = db.session.execute(db.select(activity).filter_by(user_id=user_id)).scalars()
        schema = schema(many=True)

        return schema.dump(activities)

    def post(self, user_id: int, activity: str):
        """Create new activity data for the given user."""

        app.logger.debug(f"Request payload: {request.json}")

        activity, schema = self._get_activity(activity)
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
