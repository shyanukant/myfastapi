import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.main import app
from app.database import get_db
from app.database import Base
from app.config import settings
from app.models import Post, Vote
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.user}:{settings.password}@{settings.host}/{settings.database}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    print("my session fixture run")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    data = {
        "email": "testemail@gmail.com",
        "phone": "1234567890",
        "password": "testpassword"
    }
    res = client.post("/users/create", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    data = {
        "email": "testshyanukant@gmail.com",
        "phone": "9876543210",
        "password": "testshyanu"
    }
    res = client.post("/users/create", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):    
    client.headers= {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data =  [{
        "title": "test title",
        "content": "test content",
        "owner_id": test_user['id']
    },
    {
        "title": "test title 2",
        "content": "test content 2",
        "owner_id": test_user['id']
    },
    {
        "title": "test title 3",
        "content": "test content 3",
        "owner_id": test_user['id']
    },
    {
        "title": "test title 1 by user2",
        "content": "test content 1 by user2",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return Post(**post)

    posts_map = map(create_post_model, post_data)
    posts_list = list(posts_map)
    session.add_all(posts_list)
    session.commit()
    posts = session.query(Post).all()
    return posts

@pytest.fixture
def test_votes(session, test_posts, test_user):
    new_vote = Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()