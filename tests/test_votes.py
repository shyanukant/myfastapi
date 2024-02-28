# testcases for votes rourter
def test_vote_on_post(authorized_client, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "direction": 1
    }
    res = authorized_client.post('/votes/', json=data)
    assert res.status_code == 201

def test_vote_twice_post_conflict(authorized_client, test_posts, test_votes):
    data = {
        "post_id": test_posts[3].id,
        "direction": 1
    }
    res = authorized_client.post('/votes/', json=data)
    assert res.status_code == 409

def test_delete_vote_on_post(authorized_client, test_posts, test_votes):
    data = {
        "post_id": test_posts[3].id,
        "direction": 0
    }
    res = authorized_client.post('/votes/', json=data)
    assert res.status_code == 201

def test_delete_vote_non_exist(authorized_client, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "direction": 0
    }
    res = authorized_client.post('/votes/', json=data)
    assert res.status_code == 404

def test_vote_on_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post('/votes/', json={"post_Id": 666, "direction": 1})
    res.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    res = client.post('/votes/', json={"post_Id": test_posts[0].id, "direction": 1})
    res.status_code == 401