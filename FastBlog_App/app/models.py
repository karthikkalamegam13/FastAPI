
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    comments = relationship("Comment", back_populates="blog")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    blog_id = Column(Integer, ForeignKey("blogs.id"))

    blog = relationship("Blog", back_populates="comments")
