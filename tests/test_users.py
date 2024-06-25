from app import schemas
from jose import jwt
import pytest # type: ignore
from app.config import settings

# def test_root(client):
#     res= client.get("/")
#     print(res.json())
#     assert res.json() ==["Welcome to my API"]
    
def test_create_user(client):
    res=client.post("/users/",json={"email":"aadhyaj@gmail.com","e_password":"aadhyajason23"})
    new_user=schemas.UserResponse(**res.json())
    assert res.json().get("email")=="aadhyaj@gmail.com"
    assert res.status_code==201
    
def test_login_user(client,test_user):
    res=client.post("/login",data={"username":test_user['email'],"password":test_user['e_password']})
    login_res=schemas.Token(**res.json())
    payload= jwt.decode(login_res.access_token, settings.secret_key,algorithms=[settings.algorithm])
    id= payload.get("user_id")
    assert id==test_user['id']
    assert login_res.token_type=="bearer"
    assert res.status_code==200
    
def test_incorrect_login(test_user,client):
    res=client.post("/login",data={"username":test_user['email'],"password":"wrongPassword"})
    assert res.status_code==403
    assert res.json().get("detail")=='Invalid Credentials'