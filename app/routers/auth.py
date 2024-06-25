from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oauth2

router=APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm= Depends(), db:Session=Depends(database.get_db)):
    user= db.query(models.User).filter(models.User.email==user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail ="Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.e_password):  #here user_credentials.password is plain_password and user.password is hashed_password
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail ="Invalid Credentials")
    
    # We'll create the token 
    # Return the token
    
    access_token= oauth2.create_access_token(data={"user_id":user.id})  #only user_id is passed as payload
    return {"access_token": access_token,"token_type":"bearer" }