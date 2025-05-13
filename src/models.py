
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[list["Posts"]] = relationship(back_populates="user")
    following: Mapped[list["Followers"]] = relationship(
        back_populates="following")
    followed: Mapped[list["Followers"]] = relationship(
        back_populates="followed")
    comentarios: Mapped[list["Comentario"]
                        ] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "followers": [follower.serialize() for follower in self.followers],
            "posts": [post.serialize() for post in self.posts]
            # do not serialize the password, its a security breach
        }


class Followers(db.Model):
    __tablename__ = 'followers'

# como te conectas a la tabla
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)

# el valor de los id
    following: Mapped["User"] = relationship(back_populates="following")
    # el valor de followers.followed se va a mostrar en users.followed
    followed: Mapped["User"] = relationship(back_populates="followed")

    def serialize(self):
        return {
            "id": self.id,

        }


class Posts(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    comentarios: Mapped[list["Comentario"]
                        ] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user": self.user.name,
            "comentarios":  [comentario.serialize() for comentario in self.comentarios]
        }


class Comentario(db.Model):
    __tablename__ = 'comentario'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    # esa clave establece que un comentario solo puede tener un usuario

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comentarios", )

    post: Mapped["Posts"] = relationship(back_populates="comentarios")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text

        }
