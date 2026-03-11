""" imports """
import random
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_to_db(long_url: str, custom_slug: str, db: Session):
    try:
        new_link = models.Link(long_url=long_url, slug=custom_slug)
        db.add(new_link)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        ) from e

def create_slug(letters: str) -> str:
    custom_slug = ('').join(random.choice(letters) for _ in range(6))
    return custom_slug

@app.get('/')
def read_root(request: Request):
    return templates.TemplateResponse(request, 'index.html', {
        'request': request,
    })

@app.post('/', status_code=201)
def create_url(request: Request, long_url: Annotated[str, Form()],
custom_slug: Annotated[str, Form(min_length=3, max_length=15, pattern=r"^\S+$")] = None,
db: Session = Depends(get_db)):
    if not (long_url.startswith("http://") or long_url.startswith("https://")):
        long_url = "https://" + long_url
    existing_url = db.query(models.Link).filter(models.Link.long_url == long_url).first()
    if existing_url:
        return templates.TemplateResponse(request, 'index.html', {
        'response': 'This link is already existing.',
        'request': request,
        'path': existing_url.slug
        }, status_code=200)
    if custom_slug:
        slug_check = db.query(models.Link).filter(models.Link.slug == custom_slug).first()
        if slug_check:
            raise HTTPException(status_code=400,
                                detail='Slug is already exists. Please enter another slug.')
        add_to_db(long_url=long_url, custom_slug=custom_slug, db=db)
        return templates.TemplateResponse(request, 'index.html',
                                  {'response': 'Link added successfully.',
                                   'request': request,
                                                          'path': custom_slug}, status_code=201)
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    custom_slug = create_slug(letters)
    while db.query(models.Link).filter(models.Link.slug == custom_slug).first():
        custom_slug = create_slug(letters)
    add_to_db(long_url=long_url, custom_slug=custom_slug, db=db)
    return templates.TemplateResponse(request, 'index.html',
                                      {'response': 'Link added successfully.',
                                       'request': request,
                                                              'path': custom_slug}, status_code=201)

@app.get('/admin/cleanup')
def clean_older_links(db: Session = Depends(get_db)):
    bound = datetime.now() - timedelta(days=3)
    try:
        removed = db.query(models.Link).filter(models.Link.created_at < bound).delete()
        db.commit()
        return {'result': f'Cleanup is completed. {removed} links deleted.'}
    except Exception as e:
        db.rollback()
        print(f'There is an error occurred: {e}')
        raise HTTPException(status_code=500, detail=f'An error occurred during database cleanup.{e}') from e

@app.get('/{get_slug}')
def redirect(get_slug: str, db: Session = Depends(get_db)):
    founded_query = db.query(models.Link).filter(models.Link.slug == get_slug).first()
    if founded_query:
        now = datetime.now()
        if founded_query.created_at is not None:
            if now - founded_query.created_at > timedelta(days=3):
                db.delete(founded_query)
                db.commit()
                raise HTTPException(status_code=410, detail='This link has expired after 3 days.')
        get_link = founded_query.long_url
        return RedirectResponse(url=get_link)
    raise HTTPException(status_code=404, detail='URL not found')

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse(request, 'error.html', {'status_code': exc.status_code,
                                                     'request': request,
                                                     'error_message': exc.detail
                                                     },
                                      status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(request, 'error.html',
                                      {'status_code': 422,
                                       'request': request,
                                       'error_message': 'Invalid input values'}, status_code=422)
