# from typing import Optional,List
from fastapi import FastAPI
# from fastapi.params import Body
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


my_posts = [{"id":1,'title':'some title','content':'some content'},{'id':2,'title':'second post','content':'body of second post'}]


    
while True:   
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='harishmani',password='',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successfull!')
        break
    except Exception as error:
        print('connection to the database failed')
        print('error: ',error ) 
        time.sleep(2)   


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the fast api"}

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
         
# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
           
# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return {"data":posts}
    


    
