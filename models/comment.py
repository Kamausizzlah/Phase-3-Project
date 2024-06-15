from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

    def __init__(self, content, post_id, author_id):
        self.content = content
        self.post_id = post_id
        self.author_id = author_id

    @classmethod
    def create_comment(cls, db, content, post_id, author_id):
        comment = cls(content=content, post_id=post_id, author_id=author_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    
    @classmethod
    def delete_comment(cls, db, post_id, author_id):
        comment = db.query(cls).filter(cls.id == post_id, cls.author_id == author_id).first()
        if comment:
            db.delete(comment)
            db.commit()
            return True
        return False
