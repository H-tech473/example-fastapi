from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteResponse)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    verify = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not verify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {vote.post_id} is not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote1 = vote_query.first()

    if vote.dir == 1:
        if vote1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on the post {vote.post_id}")
        voted = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(voted)
        db.commit()
        return {"message": "Successfully voted"}
    else:
        if not vote1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has'nt already voted on the post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}