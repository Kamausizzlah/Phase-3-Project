from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="author")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def create_user(cls, db, username, password):
        user = cls(username=username, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def get_user(cls, db, username):
        return db.query(cls).filter(cls.username == username).first()
