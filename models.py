from app import sqlalchemy as db, create_app
from json import JSONEncoder
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash


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
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("movie_id", db.Integer,
              db.ForeignKey("movies.id"),
              primary_key=True),
    db.Column("role_id", db.Integer,
              db.ForeignKey("roles.id"),
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
    db.Column("role_id", db.Integer,
              db.ForeignKey("roles.id"),
              primary_key=True),
)

user_albums = db.Table(
    "user_albums",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("album_id", db.Integer,
              db.ForeignKey("albums.id"),
              primary_key=True),
    db.Column("role_id", db.Integer,
              db.ForeignKey("roles.id"),
              primary_key=True),
)

user_books = db.Table(
    "user_books",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("book_id", db.Integer,
              db.ForeignKey("books.id"),
              primary_key=True),
    db.Column("role_id", db.Integer,
              db.ForeignKey("roles.id"),
              primary_key=True),
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
    profile_pic = db.Column(db.String)
    utypes = db.relationship("UType", secondary=user_type,
                             backref=db.backref('Users',
                                                cascade="all, delete-orphan",
                                                single_parent=True),
                             lazy=True)
    roles = db.relationship("Role", secondary=user_roles,
                            backref=db.backref('Users',
                                               cascade="all, delete-orphan",
                                               single_parent=True),
                            lazy=True)
    addresses = db.relationship('Address', backref='users', lazy=True)
    tracks = db.relationship("Track", secondary=user_tracks,
                             backref=db.backref('Users',
                                                cascade="all, delete-orphan",
                                                single_parent=True),
                             lazy=True)
    movies = db.relationship("Movie", secondary=movies_appear,
                             backref=db.backref('Users',
                                                cascade="all, delete-orphan",
                                                single_parent=True),
                             lazy=True)
    books = db.relationship("Book", secondary=user_books,
                            backref=db.backref('Users',
                                               cascade="all, delete-orphan",
                                               single_parent=True),
                            lazy=True)
    albums = db.relationship("Album", secondary=user_albums,
                             backref=db.backref('Users',
                                                cascade="all, delete-orphan",
                                                single_parent=True),
                             lazy=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(password)

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
            "image": self.profile_pic,
            "bio": self.bio
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
    tracks = db.relationship("Track", backref="categories", lazy=True)
    albums = db.relationship("Album", backref="categories", lazy=True)
    books = db.relationship("Book", backref="categories", lazy=True)
    movies = db.relationship("Movie", backref="categories", lazy=True)

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
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("Users", secondary=movies_appear,
                            backref=db.backref('Movie',
                                               cascade="all, delete-orphan",
                                               single_parent=True),
                            single_parent=True,
                            lazy=True)
    trailer_url = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    duration = db.Column(db.String)
    release_date = db.Column(db.DateTime, index=True, nullable=True)
    cover_url = db.Column(db.String)

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
            "uploader_id": self.uploader_id,
            "genre_id": self.genre_id,
            "category_id": self.category_id,
            "release_date": self.release_date,
            "duration": self.duration,
            "trailer_url": self.trailer_url,
            "cover_url": self.cover_url
        }


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String())
    artist_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("Users", secondary=user_albums,
                            backref=db.backref('Album',
                                               cascade="all, delete-orphan",
                                               single_parent=True),
                            lazy=True)
    tracks = db.relationship("Track", backref="albums", lazy=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    duration = db.Column(db.String())
    url = db.Column(db.String())
    release_date = db.Column(db.DateTime, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    album_cover_url = db.Column(db.String)
    @property
    def serialize(self):
        return {
            "id": self.id,
            "album_link": self.url,
            "album_title": self.album_name,
            "duration": self.duration,
            "cover_url": self.album_cover_url,
            "category_id": self.category_id,
            "release_date": self.release_date,
        }

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
    song_title = db.Column(db.String())
    artist_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    url = db.Column(db.String())
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    users = db.relationship("Users", secondary=user_tracks,
                            backref=db.backref('Track',
                                               cascade="all, delete-orphan",
                                               single_parent=True),
                            lazy=True)
    duration = db.Column(db.String())
    release_date = db.Column(db.DateTime, index=True)

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
            "track_link": self.url,
            "song_title": self.song_title,
            "duration": self.duration,
            "release_date": self.release_date,
        }


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    users = db.relationship("Users", secondary=user_books,
                            backref=db.backref('Book',
                                               cascade="all, delete-orphan",
                                               single_parent=True),
                            lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    url = db.Column(db.String())
    release_date = db.Column(db.DateTime, index=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"))

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
            "title": self.book_name,
            "author_id": self.author_id,
            "book_url": self.url,
            "uploader_id": self.uploader_id,
            "genre_id": self.genre_id,
            "category_id": self.category_id,
            "release_date": self.release_date
        }


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    tracks = db.relationship("Track", backref="genres", lazy=True)
    books = db.relationship("Book", backref="genres", lazy=True)
    movies = db.relationship("Movie", backref="genres", lazy=True)

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
