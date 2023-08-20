import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json



# DB_HOST = os.getenv('DB_HOST', 'e:5432')  
# DB_USER = os.getenv('DB_USER', 'shammaaas')  
# DB_NAME = os.getenv('DB_NAME', 'casting_agency')
# DB_PATH = 'postgresql+psycopg2://{}@{}/{}'.format(DB_USER, DB_HOST, DB_NAME)
DB_PATH = os.environ['DATABASE_URL']



db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
     db.create_all()
    

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime(), nullable=False)
    actors = db.relationship('Actor', cascade="all, delete", backref='movies')


    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
      
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            }


class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    movie_id = Column(Integer, db.ForeignKey('movies.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }