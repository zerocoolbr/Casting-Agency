import os
from sqlalchemy import Column, String, Integer, Enum, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_user = "postgres"
database_password = "docker"
database_host = "localhost"
dabase_port = 5432
database_name = "capstone"
database_uri = "postgresql://{}:{}@{}:{}/{}".format(
    database_user, database_password, database_host, dabase_port, database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path if os.environ.get('FLASK_ENV') == 'development' else \
        os.environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Actors(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), unique=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("female", "male", name="gender_enum", create_type=False))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return json.dumps(self.format())


class Movies(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=False)
    release_date = Column(DateTime, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return self.format()
