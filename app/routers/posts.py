from fastapi import  Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import  get_db
from ..models import Post, Vote
from ..schemas import PostCreate, PostResponse, PostOutResponse
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)
# This route is used to create a new post
@router.post('/create', response_model=PostResponse)
async def create_post(post: PostCreate, db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# This route is used to get all posts of a user which is logged in 
@router.get('/myposts', response_model=List[PostOutResponse])
async def get_user_posts(db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    posts = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Post.id==Vote.post_id, isouter=True).group_by(Post.id).filter(Post.owner_id==current_user.id)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not exists")
    return posts

# This route is used to Get all posts with pagination and search
@router.get('/', response_model=List[PostOutResponse])
async def get_posts(db:Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ''):
    # posts = db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Post.id==Vote.post_id, isouter=True).group_by(Post.id).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not exists")
    return posts

# This route is used to get a post by id
@router.get('/{id}', response_model=PostOutResponse)
async def get_post_by_id(id: int, db:Session = Depends(get_db)):
    # post = db.query(Post).filter(Post.id==id).first()
    post = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Post.id==Vote.post_id, isouter=True).group_by(Post.id).filter(Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return post

# This route is used to delete a post by id and only owner of the post can delete the post
@router.delete('/{id}')
async def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id==id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            details="Not allowed to delete this post. You are not owner of this post")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# This route is used to update a post by id and only owner of the post can update the post
@router.put('/{id}', response_model=PostResponse)
async def update_post(id: int, updated_post:PostCreate, db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id==id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            details="Not allowed to update this post. You are not owner of this post")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()