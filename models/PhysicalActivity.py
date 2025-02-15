from typing import Optional

from marshmallow.fields import Int
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class PhysicalActivity(db.Model):
    """Contains a users' physical activity information."""

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    exercising_hours: Mapped[Optional[int]] = mapped_column(default=0)
    steps: Mapped[Optional[int]] = mapped_column(default=0)
    km: Mapped[Optional[int]] = mapped_column(default=0)


class PhysicalActivitySchema(SQLAlchemyAutoSchema):
    """Validation schema for the `PhysicalActivity` object."""

    class Meta:
        model = PhysicalActivity
        exclude = ["id"]

    exercising_hours = Int()
    steps = Int()
    km = Int()
