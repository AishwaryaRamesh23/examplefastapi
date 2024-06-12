from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter  # to create web application; to handle HTTP responses and exceptions
from sqlalchemy import or_,func
from sqlalchemy.orm import Session
from ..import models,schemas,oauth2
from ..database import get_db
from typing import Optional

router=APIRouter(
    prefix="/smposts",
    tags=['Posts']
)

@router.get("/",response_model=list[schemas.PostOut])    # retrieves all posts from the database using SQL query and returns them
#@router.get("/")
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search: Optional[str]=""):
    #cursor.execute("""SELECT * FROM smposts""")
    #posts=cursor.fetchall()
    """posts=db.query(models.Post).filter(models.Post.user_id==current_user.id).all() [To get post of the particular user alone]"""
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #to search 2 words with space in middle (use %20 between the words)
    
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.Post,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):   ##we have to copy and paste the input argument into path operation function.
    #cursor.execute("""INSERT INTO smposts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title, post.content, post.published))
    #new_post =cursor.fetchone()      
    #conn.commit()                    
    new_post= models.Post(user_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post        # Using that variable to return the created/inserted post

@router.get("/{id}",response_model=schemas.PostOut) # to retrieve post by its ID
def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)): # here id is converted as int to ensure only valid "id" is inserted
    #cursor.execute("""SELECT * FROM smposts WHERE id=%s""",[id]) # to avoid SQL injection attack ==> %s is the place holder; query parameters should be a sequence or a mapping
    #post=cursor.fetchone()
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    """if post.user_id!=current_user.id: 
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")""" #if we want to retireve only the posts of the particular user we can use this
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)      # deletes a post by its ID
def delete_post(id:int,db:Session=Depends(get_db),current_user :int=Depends(oauth2.get_current_user)):
   #cursor.execute("""DELETE FROM smposts WHERE id=%s RETURNING * """ ,[id])
   #deleted_post=cursor.fetchone()
   #conn.commit()
   post_query=db.query(models.Post).filter(models.Post.id==id)
   post=post_query.first()
   if post==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")
   if post.user_id!=current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
   post_query.delete(synchronize_session=False)
   db.commit()
   return Response (status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)           # updates a post by its ID and returns updated post
def update_post(id:int,updated_post:schemas.Post,db:Session=Depends(get_db),current_user :int=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE smposts SET id=%s, title=%s, content=%s, published=%s WHERE id=%s RETURNING* """,(post.id,post.title,post.content,post.published,id))
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")
    if post.user_id!=current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()