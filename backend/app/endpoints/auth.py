from fastapi import APIRouter, Depends, status

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from backend.app.database import get_db

from backend.app.repository import auth

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
def create_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    # current_user: int = Depends(oauth2.get_current_user),
):
    return auth.login(db, user_credentials)
