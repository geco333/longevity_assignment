from flask import request
from flask_restful import Resource

from db import db
from models.User import UserSchema, User


class UserList(Resource):
    def get(self):
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        schema = UserSchema(many=True)

        return schema.dump(users)

    def post(self):
        schema = UserSchema()
        validated_data = schema.load(request.json)

        user = User(**validated_data)

        db.session.add(user)
        db.session.commit()

        return schema.dump(user)


class UserResource(Resource):
    def get(self, user_id: int):
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
        schema = UserSchema()

        return schema.dump(user)
