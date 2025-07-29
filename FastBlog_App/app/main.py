from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db)
    return templates.TemplateResponse("blogs.html", {"request": request, "blogs": blogs})

@app.get("/blogs/{blog_id}", response_class=HTMLResponse)
def read_blog(request: Request, blog_id: int, db: Session = Depends(get_db)):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return templates.TemplateResponse("blog.html", {"request": request, "blog": db_blog})

@app.get("/new", response_class=HTMLResponse)
def new_blog_form(request: Request):
    return templates.TemplateResponse("create_blog.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
def create_blog_form(request: Request, title: str = Form(...), body: str = Form(...), db: Session = Depends(get_db)):
    blog = schemas.BlogCreate(title=title, body=body)
    crud.create_blog(db=db, blog=blog)
    return RedirectResponse(url="/", status_code=303)

@app.post("/blogs/{blog_id}/comments", response_class=HTMLResponse)
def create_comment_form(request: Request, blog_id: int, text: str = Form(...), db: Session = Depends(get_db)):
    comment = schemas.CommentCreate(text=text)
    crud.create_comment(db=db, comment=comment, blog_id=blog_id)
    return RedirectResponse(url=f"/blogs/{blog_id}", status_code=303)