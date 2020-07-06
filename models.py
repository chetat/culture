from app import sqlalchemy as db, create_app
from json import JSONEncoder
from datetime import datetime


user_roles = db.Table("user_role",
                      db.Column("user_id", db.Integer,
                                db.ForeignKey("users.id"),
                                primary_key=True),
                      db.Column("role_id", db.Integer,
                                db.ForeignKey("roles.id"),
                                primary_key=True),
                      db.Column("created_at", db.DateTime,
                                default=datetime.utcnow())
                      )
user_profession = db.Table(
    "user_profession",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("profession_id", db.Integer,
              db.ForeignKey("professions.id"),
              primary_key=True)
)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    users = db.relationship("Users", secondary=user_roles,
                            backref=db.backref('Role',
                                               cascade="all,delete"),
                            lazy=True)

    @property
    def serialize(self):
        return {
            "name": self.name,
            "id": self.id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    aka = db.Column(db.String, index=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    phone = db.Column(db.String)
    city = db.Column(db.String)
    professions = db.relationship("Profession", secondary=user_profession,
                                  backref=db.backref('Users',
                                                     cascade="all,delete"),
                                  lazy=True)
    roles = db.relationship("Role", secondary=user_roles,
                            backref=db.backref('Users',
                                               cascade="all,delete"),
                            lazy=True)
    track = db.relationship("Track", backref="users", lazy=True)
    movies = db.relationship("Movie", backref="users", lazy=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print(e)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def serialize(self):
        roles = ''.join([role.serialize["name"] for role in self.roles])
        return {
            "id": self.id,
            "name": self.name,
            "other_name": self.aka,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "role": roles,
            "profession": [profession.serialize["name"] for profession in self.professions]

        }

    def __repr__(self):
        return f"<User {self.id} {self.name}>"


class Profession(db.Model):
    __tablename__ = 'professions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user = db.relationship("Users", secondary=user_profession,
                           backref=db.backref('Profession',
                                              cascade="all,delete"),
                           lazy=True)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genres = db.relationship("Genre", backref="categories", lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, index=True)
    synopsis = db.Column(db.String)
    parental_guide = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trailer_url = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    cast = db.Column(db.ARRAY(db.String()))
    crew = db.Column(db.ARRAY(db.String()))
    producer = db.Column(db.ARRAY(db.String()))
    duration = db.Column(db.DateTime())
    release_date = db.Column(db.DateTime, index=True, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    featured_artists = db.Column(db.ARRAY(db.String()))
    producers = db.Column(db.ARRAY(db.String()))
    song_writers = db.Column(db.ARRAY(db.String()))
    duration = db.Column(db.DateTime())
    release_date = db.Column(db.DateTime, index=True, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
