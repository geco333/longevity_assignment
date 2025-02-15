from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

from views.api import blueprint

app.register_blueprint(blueprint)

with app.app_context():
    from db import db

    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
