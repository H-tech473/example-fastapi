from fastapi import FastAPI, Depends
# from fastapi.params import Body
# from random import randrange 
from typing import List
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
get_db()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database='fastapi', user='postgres', password='12345', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Db is connected")
#         break
#     except Exception as error:
#         print("Connection failed")
#         print("Error: ", error)
#         time.sleep(2)

# my_posts = [{"title": "title1", "content": "content1", "id": 1}, {"title": "favorite foods", "content":"content2", "id": 2}]

# def find_post(ind):
#     for p in my_posts:
#         if p["id"] == ind:
#             return p
        
# def find_index(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

app.include_router(post.app)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "hello world"}

