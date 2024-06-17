from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def __init__(self, title, content, owner_id):
        self.title = title
        self.content = content
        self.owner_id = owner_id

    @classmethod
    def create_post(cls, db, title, content, owner_id):
        post = cls(title=title, content=content, owner_id=owner_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @classmethod
    def delete_post(cls, db, post_id, owner_id):
        post = db.query(cls).filter(cls.id == post_id, cls.owner_id == owner_id).first()
        if post:
            db.delete(post)
            db.commit()
            return True
        return False
