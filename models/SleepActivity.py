from typing import Optional

from marshmallow.fields import Int
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class Activity:
    pass


class SleepActivity(db.Model):
    """Contains a users' physical activity information."""

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    total_hours: Mapped[Optional[int]] = mapped_column(default=0)
    wake_ups: Mapped[Optional[int]] = mapped_column(default=0)


class SleepActivitySchema(SQLAlchemyAutoSchema):
    """Validation schema for the `SleepActivity` object."""

    class Meta:
        model = SleepActivity
        exclude = ["id"]

    total_hours = Int()
    wake_ups = Int()
