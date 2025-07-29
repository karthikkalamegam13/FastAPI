
from sqlalchemy.orm import Session
from . import models, schemas

def get_blog(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).offset(skip).limit(limit).all()

def create_blog(db: Session, blog: schemas.BlogCreate):
    db_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_blog(db: Session, blog_id: int, blog: schemas.BlogCreate):
    db_blog = get_blog(db, blog_id)
    if db_blog:
        db_blog.title = blog.title
        db_blog.body = blog.body
        db.commit()
        db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = get_blog(db, blog_id)
    if db_blog:
        db.delete(db_blog)
        db.commit()
    return db_blog

def get_comments(db: Session, blog_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).filter(models.Comment.blog_id == blog_id).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: schemas.CommentCreate, blog_id: int):
    db_comment = models.Comment(**comment.dict(), blog_id=blog_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
