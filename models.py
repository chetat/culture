from app import sqlalchemy as db, create_app
from json import JSONEncoder
from datetime import datetime


user_type = db.Table(
    "user_type",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("utype_id", db.Integer,
              db.ForeignKey("utypes.id"),
              primary_key=True),
    db.Column("created_at", db.DateTime,
              default=datetime.utcnow())
)

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("role_id", db.Integer,
              db.ForeignKey("roles.id"),
              primary_key=True)
)

movies_appear = db.Table(
    "movies_appear",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("movie_id", db.Integer,
              db.ForeignKey("movies.id"),
              primary_key=True),
)

user_tracks = db.Table(
    "user_tracks",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("track_id", db.Integer,
              db.ForeignKey("tracks.id"),
              primary_key=True),
    db.Column("created_at", db.DateTime,
              default=datetime.utcnow())
)

user_books = db.Table(
    "user_books",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("book_id", db.Integer,
              db.ForeignKey("books.id"),
              primary_key=True),
)

user_album = db.Table(
    "user_album",
    db.Column('user_id', db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column('album_id', db.Integer,
              db.ForeignKey("albums.id"),
              primary_key=True)
)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String)
    city = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                                                   nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    tracks = db.relationship("Track", backref="albums", lazy=True)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "tacks": [tack.serialize for track in tracks]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


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
    bio = db.Column(db.String)
    utypes = db.relationship("UType", secondary=user_type,
                            backref=db.backref('Users',
                                               cascade="all,delete"),
                            lazy=True)
    roles = db.relationship("Role", secondary=user_roles,
                            backref=db.backref('Users',
                                               cascade="all,delete"),
                            lazy=True)
    addresses = db.relationship('Address', backref='users', lazy=True)
    track = db.relationship("Track", backref="users", lazy=True)
    movies = db.relationship("Movie", secondary=movies_appear,
                             backref=db.backref('Users',
                                                cascade="all,delete"),
                             lazy=True)
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
        user_t = ''.join([u_type.serialize["name"] for u_type in self.utypes])
        return {
            "id": self.id,
            "name": self.name,
            "other_name": self.aka,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_type": user_t,
            # "tracks": self.track,
            "role": roles
        }

    def __repr__(self):
        return f"<User {self.id} {self.name}>"


class UType(db.Model):
    __tablename__ = "utypes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship("Users", secondary=user_type,
                            backref=db.backref('UType',
                                               cascade="all,delete"),
                            lazy=True)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def serialize(self):
        return {
            "name": self.name,
            "id": self.id
        }


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

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": [genre.serialize["name"] for genre in self.genres]
        }


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, index=True)
    synopsis = db.Column(db.String)
    parental_guide = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("Users", secondary=movies_appear,
                                 backref=db.backref('Movie',
                                                    cascade="all,delete"),
                                 lazy=True)
    trailer_url = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    duration = db.Column(db.String)
    release_date = db.Column(db.DateTime, index=True, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "synopsis": self.synopsis,
            "pg": self.parental_guide,
            "user_id": self.user_id,
            "genre_id": self.genre_id,
            "category_id": self.category_id,
            "release_date": self.release_date,
            "duration": self.duration,
            "trailer_url": self.trailer_url,
            # Experimental
        }


class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
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

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id
        }
