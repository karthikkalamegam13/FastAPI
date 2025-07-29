
from pydantic import BaseModel
from typing import List, Optional

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    blog_id: int

    class Config:
        orm_mode = True

class BlogBase(BaseModel):
    title: str
    body: str

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True
