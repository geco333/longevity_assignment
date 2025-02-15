from marshmallow.fields import Int
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class Activity:
    pass


class BloodTest(db.Model):
    """Contains a users' physical activity information."""

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    cbc: Mapped[int] = mapped_column(default=0)
    wbc: Mapped[int] = mapped_column(default=0)
    rbc: Mapped[int] = mapped_column(default=0)
    hct: Mapped[int] = mapped_column(default=0)
    hgt: Mapped[int] = mapped_column(default=0)


class BloodTestSchema(SQLAlchemyAutoSchema):
    """Validation schema for the `SleepActivity` object."""

    class Meta:
        model = BloodTest
        exclude = ["id"]

    cbc = Int()
    wbc = Int()
    rbc = Int()
    hct = Int()
    hgt = Int()
