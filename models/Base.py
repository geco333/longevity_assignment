from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    insertedDateTime: Mapped[Optional[int]]
    updatedDateTime: Mapped[Optional[int]]

    def __repr__(self):
        return ('{' + f"id: {self.id}, "
                      f"insertedDateTime: {self.insertedDateTime}, "
                      f"updatedDateTime: {self.updatedDateTime}")


db = SQLAlchemy(model_class=Base)
