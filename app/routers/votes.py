from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Vote, Post
from ..schemas import VoteBase
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/votes",
    tags=["votes"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(vote:VoteBase, db: Session = Depends(get_db), current_user:int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found")
    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.direction == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} have already voted on post {vote.post_id}")
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': f"User id: {current_user.id} voted on post {vote.post_id} successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not exists")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': f"User id: {current_user.id} unvoted on post {vote.post_id} successfully"}