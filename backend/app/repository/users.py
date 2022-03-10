from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from backend.app import models, oauth2, schemas, utils


def create_user(user: schemas.UserCreate, db: Session):
    verify_email = db.query(models.User).filter(models.User.email == user.email).first()
    verify_username = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if verify_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="a user with this email already exists",
        )
    if verify_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="a user with this username already exists",
        )
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )
    return user


def get_user_all(response: Response, db: Session):
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id:  does not exist",
        )
    response.headers["Content-Range"] = f"0-9/{len(user)}"
    response.headers["X-Total-Count"] = "30"
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    return user


def change_password(
    mode: schemas.UpdatePassword,
    db: Session,
    current_user: int = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if not utils.verify(mode.actual_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password does not match",
        )
    hashed_pass = utils.hashpass(mode.new_password)
    user.password = hashed_pass
    db.commit()
    return {"msg": "Password changed successfully"}
