from sqlalchemy.orm import Mapped, mapped_column

from models import db


class User(db.Model):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
