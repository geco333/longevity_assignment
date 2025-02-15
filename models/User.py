from marshmallow import validate, validates_schema, ValidationError
from marshmallow.fields import String, Int
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class User(db.Model):
    """User object containing basic personal user information."""

    __table_args__ = (
        UniqueConstraint("username", "email"),
    )

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    gender: Mapped[str]
    age: Mapped[int]

    def __repr__(self):
        return super().__repr__() + (f"username: {self.username}, "
                                     f"email: {self.email}, "
                                     f"gender: {self.gender}, "
                                     f"age: {self.age}"
                                     + "}")


class UserSchema(SQLAlchemyAutoSchema):
    """Validation schema for the `User` object."""

    class Meta:
        model = User
        exclude = ["id"]

    username = String(required=True)
    email = String(required=True, validate=[validate.Email()])
    age = Int(required=True)
    gender = String(required=True, validate=[validate.OneOf(["male", "female"])])


class NewUserSchema(UserSchema):
    @validates_schema
    def validate_email(self, data, **kwargs):
        """Queries the database to see if the request emil already exists,
        if so raise a `ValidationError`"""

        email = data.get("email")

        if db.session.execute(db.select(User).filter_by(email=email)).one_or_none():
            raise ValidationError(f"Email already exists in database.")

    @validates_schema
    def validate_username(self, data, **kwargs):
        """Queries the database to see if the request username already exists,
        if so raise a `ValidationError`"""

        username = data.get("username")

        if db.session.execute(db.select(User).filter_by(username=username)).one_or_none():
            raise ValidationError(f"Username already exists in database.")
