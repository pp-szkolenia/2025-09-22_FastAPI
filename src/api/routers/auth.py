from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import User
from db.orm import get_session
from api.models import UserLogin, Token
from api import utils, oauth2


router = APIRouter(tags=["authentication"])


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    with session:
        stmt = select(User).where(User.username == user_credentials.username)
        user = session.scalars(stmt).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    payload = {"user_id": user.id_number, "is_admin": user.is_admin}
    access_token = oauth2.create_access_token(data=payload)
    return {"access_token": access_token, "token_type": "bearer"}
