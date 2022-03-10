from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from backend.app import oauth2, schemas
from backend.app.database import get_db
from backend.app.repository import users

router = APIRouter()

# /users/
# /users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
    post: schemas.UserCreate,
    db: Session = Depends(get_db),
    # current_user: int = Depends(oauth2.get_current_user),
):
    return users.create_user(post, db)


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return users.get_user(id, db)


@router.get("/", response_model=List[schemas.UserOut])
def get_user_all(
    response: Response,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return users.get_user_all(response, db)


@router.put("/edit")
def change_password(
    mode: schemas.UpdatePassword,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return users.change_password(mode, db, current_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    return users.delete_product(id, db)
