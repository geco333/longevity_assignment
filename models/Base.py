from datetime import datetime
from typing import Optional

import pytz
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    """Base object for all database models."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    insertedDateTime: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),
                                                                 default=datetime.now(tz=pytz.UTC))
    updatedDateTime: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),
                                                                default=datetime.now(tz=pytz.UTC))

    def __repr__(self):
        return ('{' + f"id: {self.id}, "
                      f"insertedDateTime: {self.insertedDateTime}, "
                      f"updatedDateTime: {self.updatedDateTime}, ")
