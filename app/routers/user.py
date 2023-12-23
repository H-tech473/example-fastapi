from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, main
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post("/", status_code=201, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

    #hash the password
    
    use = db.query(models.User).filter(models.User.email == user.email).first()
    if use:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")

    user.password = utils.hashfunc(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    return user