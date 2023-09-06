from .. import models,schemas,oauth2
from typing import List
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func
from ..database import  get_db
from .. import oauth2
# app = FastAPI()

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/',response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user),limit:int =10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts=cursor.fetchall()
    # posts=db.query(models.Post).filter(models.Post.owner_id ==current_user.id).all()
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()    
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results
    # return posts

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # cursor.execute(f"INSERT INTO posts (title,content,published) VALUES({post.title},{post.content},{post.published})")
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(**post.model_dump())
    # print(current_user.id)
    # print(current_user.email)
    new_post=models.Post(owner_id=current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get('/posts/latest')
# def get_latest_post():
#     latest_post=my_posts[len(my_posts)-1]
#     return {'details':latest_post}

@router.get('/{id}',response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
    # post=cursor.fetchone()
    # post = find_post(id) 
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'message':f'post with id {id} was not found'}
    return post

@router.delete('/{id}')
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #find the index in the array that has required id
    # cursor.execute("""DELETE FROM posts WHERE id=%s returning *""",(str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} does not exist')
    # my_posts.pop(index)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'not authorised to perform the requested action')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put('/{id}',response_model=schemas.Post)
def update_posts(id:int,updated_post:schemas.PostCreate, db: Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s,published=%s WHERE id=%s returning * """, (post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post withn id: {id} doesnot exist')
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
