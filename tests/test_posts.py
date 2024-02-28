# testcases for posts rourter

import pytest
from app.schemas import PostResponse, PostOutResponse

@pytest.mark.parametrize("title, content, published", [
    ("new awesome title", "new awesome content", True),
    ("let's test title", "let's test content", False),
    ("Best title ever", "Best content ever", True),
    ("Worst title ever", "Worst content ever", False),
])
def test_authorized_create_post(authorized_client, test_user, test_posts, title, content, published):
    data = {
        "title": title,
        "content": content,
        "published": published
    }
    res = authorized_client.post("/posts/create", json=data)
    output = PostResponse(**res.json())
    assert res.status_code == 201
    assert output.title == title
    assert output.content == content
    assert output.published == published


def test_authorized_create_post_default_published_true(authorized_client, test_user, test_posts):
    data = {
        "title": "test new title ",
        "content": "test new content ",
    }
    res = authorized_client.post("/posts/create", json=data)
    output = PostResponse(**res.json())
    assert res.status_code == 201
    assert output.title == data['title']
    assert output.content == data['content']
    assert output.published == True

def test_authorized_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_anyone_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 200

def test_authoried_get_post_by_id(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    output = PostOutResponse(**res.json())
    assert res.status_code == 200
    assert output.Post.id == test_posts[0].id
    assert output.Post.title == test_posts[0].title
    assert output.Post.content == test_posts[0].content

def test_anyone_get_post_by_id(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    output = PostOutResponse(**res.json())
    assert res.status_code == 200
    assert output.Post.id == test_posts[0].id
    assert output.Post.title == test_posts[0].title
    assert output.Post.content == test_posts[0].content

def test_post_not_found(authorized_client, test_posts):
    res = authorized_client.get("/posts/10000")
    assert res.status_code == 404

def test_authorized_get_user_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/myposts")
    assert len(res.json()) == 3
    assert res.status_code == 200

def test_unauthorized__get_user_posts(client, test_posts):
    res = client.get("/posts/myposts")
    assert res.status_code == 401

def test_unauthorized_create_post(client, test_user, test_posts):
    data = {
        "title": "test new title ",
        "content": "test new content ",
    }
    res = client.post("/posts/create", json=data)
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_found(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/10000")
    assert res.status_code == 404

def test_delete_post_not_owner(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post_success(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
     }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data["content"]

def test_update_post_not_found(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
     }
    res = authorized_client.put(f"/posts/33333", json=data)
    assert res.status_code == 404

def test_update_post_not_owner(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
     }
    res = authorized_client.put(f"/posts/4", json=data)
    assert res.status_code == 403