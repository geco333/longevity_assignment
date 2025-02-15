from datetime import datetime

import pytz
from flask import request
from flask_restful import Resource

from app import app
from db import db
from models.Blood import BloodTest, BloodTestSchema
from models.User import User


class BloodTests(Resource):
    def get(self):
        """Returns all blood tests data."""

        activity = db.session.execute(db.select(BloodTest).order_by(BloodTest.id)).scalars()
        schema = BloodTestSchema(many=True)

        return schema.dump(activity)


class BloodTestActions(Resource):
    def get(self, blood_test_id: int):
        """Returns all data for the given blood_test_id."""

        schema = BloodTestSchema()

        if activity := db.session.execute(db.select(BloodTest).filter_by(id=blood_test_id)).scalar_one_or_none():
            return schema.dump(activity)

        return {"error": "Did not find blood test ID."}

    def put(self, blood_test_id: int):
        """Update a single blood tests' data."""

        app.logger.debug(f"Request payload: {request.json}")

        schema = BloodTestSchema()
        validated_data = schema.load(request.json)

        if blood_test := db.session.execute(db.select(BloodTest).filter_by(id=blood_test_id)).scalar_one_or_none():
            app.logger.debug(f"Current blood test data: {blood_test}")

            for field, updated_value in validated_data.items():
                current_value = getattr(blood_test, field)

                if current_value != updated_value:
                    app.logger.debug(f"Updated {field}: {current_value} -> {updated_value}")
                    setattr(blood_test, field, updated_value)

            blood_test.updatedDateTime = datetime.now(tz=pytz.UTC)

            db.session.commit()

            app.logger.debug("Blood test updated successfully.")

            return {
                "response": "Blood test updated successfully.",
                "blood_test": schema.dump(blood_test)
            }

        return {"error": f"Did not find blood_test ID {blood_test_id}"}

    def delete(self, blood_test_id: int):
        """Delete all users' data."""

        if blood_test := db.session.execute(db.select(BloodTest).filter_by(id=blood_test_id)).scalar_one_or_none():
            db.session.delete(blood_test)
            db.session.commit()

            app.logger.debug(f"Blood test {blood_test_id} removed successfully.")

            return {"response": f"Blood test {blood_test_id} removed."}

        return {"error": f"Did not find Blood test ID {blood_test_id}"}


class UserBloodTestActions(Resource):
    def get(self, user_id: int):
        """Get all information for a single users' blood tests."""

        activities = db.session.execute(db.select(BloodTest).filter_by(user_id=user_id)).scalars()
        schema = BloodTestSchema(many=True)

        return schema.dump(activities)

    def post(self, user_id: int):
        """Create new blood test for the given user."""

        app.logger.debug(f"Request payload: {request.json}")

        schema = BloodTestSchema()
        validated_data = schema.load(request.json)

        if db.session.execute(db.select(User).filter_by(id=user_id)).one_or_none():
            new_activity = BloodTest(**validated_data)
            new_activity.user_id = user_id

            db.session.add(new_activity)
            db.session.commit()

            app.logger.debug("Blood test added successfully.")

            return {
                "response": "Blood test added successfully.",
                "activity": schema.dump(new_activity)
            }

        return {"error": f"Did not find user ID {user_id}"}
