import pytest 
from app import schemas

def test_get_all_posts(authorized_client,test_posts):
    res= authorized_client.get("/smposts/")
    print(res.json())
    assert res.status_code==200
    
def test_unauthorized_user_get_all_posts(client,test_posts):
    res=client.get("/smposts/")
    assert res.status_code==401
    
def test_unauthorized_user_get_one_post(client,test_posts):
    res=client.get(f"/smposts/{test_posts[0].id}")
    assert res.status_code==401
    
def test_get_one_post_not_exist(authorized_client,test_posts):
    res=authorized_client.get(f"/smposts/2309")
    assert res.status_code==404
    
def test_get_one_post(authorized_client,test_posts):
    res=authorized_client.get(f"/smposts/{test_posts[0].id}")
    print(res.json())

@pytest.mark.parametrize("title,content,published",[
    ("new title","new content",False),
    ("favo kdrama","dramacool",True),
    ("dailymotion","kdrama",True),
])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res=authorized_client.post("/smposts/",json={"title":title,"content":content,"published":published})
    created_post= schemas.PostResponse(**res.json())
    assert res.status_code==201
    assert created_post.title==title
    assert created_post.content==content
    assert created_post.user_id==test_user['id']
    
def test_create_post_default_published_true(authorized_client,test_user,test_posts):
    res=authorized_client.post("/smposts/",json={"title":"default published","content":"checking default publishing"})
    created_post= schemas.PostResponse(**res.json())
    assert res.status_code==201
    assert created_post.title=="default published"
    assert created_post.content=="checking default publishing"
    # assert schemas.Post(created_post.published)==True
    assert created_post.user_id==test_user['id']
    
def test_unauthorized_user_create_post(client,test_posts):
    res=client.post("/smposts/",json={"title":"default published","content":"checking default publishing"})
    assert res.status_code==401
    
def test_unauthorized_user_delete_post(client,test_posts,test_user):
    res=client.delete(f"/smposts/{test_posts[0].id}")
    assert res.status_code==401
    
def test_delete_post_success(authorized_client,test_posts,test_user):
    res=authorized_client.delete(f"/smposts/{test_posts[0].id}")    
    assert res.status_code==204
    
def test_delete_post_non_exist(authorized_client,test_posts,test_user):
    res=authorized_client.delete(f"/smposts/2309")
    assert res.status_code==404
    
def test_delete_other_user_post(authorized_client,test_posts,test_user):
    res=authorized_client.delete(f"/smposts/{test_posts[3].id}")
    assert res.status_code==403

def test_update_post(authorized_client,test_user,test_posts):
    data={
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[0].id
    }
    res=authorized_client.put(f"/smposts/{test_posts[0].id}",json=data)
    updated_post=schemas.Post(**res.json())
    assert res.status_code==200
    assert updated_post.title==data['title']
    assert updated_post.content==data['content']
    
def test_update_other_user_post(authorized_client,test_posts,test_user):
    data={
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[3].id
    }
    res=authorized_client.put(f"/smposts/{test_posts[3].id}",json=data)
    assert res.status_code==403

def test_unauthorized_user_update_post(client,test_posts,test_user):
    data={
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[3].id
    }
    res=client.put(f"/smposts/{test_posts[0].id}",json=data)
    assert res.status_code==401
    
def test_update_post_non_exist(authorized_client,test_posts,test_user):
    data={
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[3].id
    }
    res=authorized_client.put(f"/smposts/2309",json=data)
    assert res.status_code==404