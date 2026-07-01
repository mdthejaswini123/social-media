import time
import random

from fastapi import Depends, FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from app.routers import auth
from .database import engine, get_db
from . import models, schemas, utils
from .routers import post, user
# to create the tables in the database, we can use the metadata of the Base class that we defined in the database.py file, and call the create_all() method on it, passing the engine as an argument, like this:
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# connect to the database using psycopg2
# we will use a while loop to keep trying to connect to the database until we succeed, and we will print a message if the connection fails and wait for 2 seconds before trying again
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres",
                                password="ThejuSilo@123", cursor_factory=RealDictCursor)
    # create a cursor object to execute SQL queries
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "published": True, "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "published": False, "id": 2}]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_post_index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None


@app.get("/")
async def root():
    return {"message": "welocme to fastapi"}

# to include the routers for the post and user endpoints, we can use the include_router() method of the FastAPI app object, and pass the router objects that we defined in the post.py and user.py files as arguments, like this:
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
