from flask_sqlalchemy import SQLAlchemy

from models.Base import Base

db = SQLAlchemy(model_class=Base)
