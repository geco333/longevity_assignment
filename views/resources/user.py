from datetime import datetime

import pytz
from flask import request
from flask_restful import Resource

from app import app
from db import db
from models.PhysicalActivity import PhysicalActivity
from models.User import UserSchema, User, NewUserSchema


class Users(Resource):
    def get(self):
        """Returns a list of all entities in the user table."""

        users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        schema = UserSchema(many=True)

        return schema.dump(users)

    def post(self):
        """Create a new `User` entity in the user table."""

        app.logger.debug(f"Request payload: {request.json}")

        schema = NewUserSchema()
        validated_data = schema.load(request.json)

        user = User(**validated_data)

        db.session.add(user)
        db.session.commit()

        app.logger.debug("New user added successfully.")

        return {
            "response": "New user added successfully.",
            "user": schema.dump(user)
        }


class SingleUser(Resource):
    def get(self, user_id: int):
        """Get all information for a single user."""

        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
        schema = UserSchema()

        app.logger.debug(f"user: {user}")

        return schema.dump(user)

    def put(self, user_id: int):
        """Update a users' data."""

        app.logger.debug(f"Request payload: {request.json}")

        schema = UserSchema()
        validated_data = schema.load(request.json)

        if user := db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none():
            app.logger.debug(f"Current user data: {user}")

            for field, updated_value in validated_data.items():
                current_value = getattr(user, field)

                if current_value != updated_value:
                    app.logger.debug(f"Updated {field}: {current_value} -> {updated_value}")
                    setattr(user, field, updated_value)

            user.updatedDateTime = datetime.now(tz=pytz.UTC)

            db.session.commit()

            app.logger.debug("User updated successfully.")

            return {
                "response": "User updated successfully.",
                "user": schema.dump(user)
            }

        return {"error": f"Did not find user ID {user_id}"}

    def delete(self, user_id: int):
        """Delete all users' data."""

        if user := db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none():
            db.session.delete(user)
            db.session.commit()

            app.logger.debug(f"User {user_id} removed successfully.")

            return {"response": f"User {user_id} removed."}

        return {"error": f"Did not find user ID {user_id}"}


class UserHealthScore(Resource):
    def get(self, user_id: int):
        """Calculate health score for a single user."""

        all_users = db.session.execute(db.select(PhysicalActivity)).scalars()
        all_users = list(all_users.all())

        user_physical_activities = db.session.execute(db.select(PhysicalActivity).filter_by(user_id=user_id)).scalars()
        user_physical_activities = list(user_physical_activities.all())

        user_exercising_hours = sum([row.exercising_hours for row in user_physical_activities])
        user_steps = sum([row.steps for row in user_physical_activities])
        user_km = sum([row.km for row in user_physical_activities])

        total_exercising_hours = sum([row.exercising_hours for row in all_users])
        total_steps = sum([row.steps for row in all_users])
        total_km = sum([row.km for row in all_users])

        health_score = user_exercising_hours / total_exercising_hours
        health_score += user_steps / total_steps
        health_score += user_km / total_km

        health_score = f"{health_score:.3}"

        return {"health_score": health_score}
