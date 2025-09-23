from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.models import UserBody
from api.utils import get_item_by_id, get_item_index_by_id
from db.orm import get_session
from db.models import User


users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False},
]

router = APIRouter()


@router.get("/users")
def get_users(session: Session = Depends(get_session)):
    with session:
        stmt = select(User)
        users_data = session.scalars(stmt).all()

    users_data_response = [
        {
            "user_id": user.id_number,
            "username": user.username,
            "password": user.password,
            "is_admin": user.is_admin,
        }
        for user in users_data
    ]
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"result": users_data_response})


@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    with session:
        stmt = select(User).where(User.id_number == user_id)
        target_user = session.scalars(stmt).first()

    if not target_user:
        message = {"error": f"User with id {user_id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    response_target_user = {
        "user_id": target_user.id_number,
        "username": target_user.username,
        "password": target_user.password,
        "is_admin": target_user.is_admin,
    }

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"result": response_target_user})


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(body: UserBody, session: Session = Depends(get_session)):
    new_user = User(**body.model_dump())
    with session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    return {"message": "New user added", "details": new_user}


@router.delete("/users/{user_id}", include_in_schema=True)
def delete_user_by_id(user_id: int, session: Session = Depends(get_session)):
    with session:
        stmt = select(User).where(User.id_number==user_id)
        target_user = session.scalars(stmt).first()

    if not target_user:
        message = {"error": f"User with id {user_id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)
    else:
        session.delete(target_user)
        session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/users/{user_id}")
def update_user(user_id:int, body: UserBody, session: Session = Depends(get_session)):
    with session:
        stmt = select(User).where(User.id_number == user_id)
        target_user = session.scalars(stmt).first()

        if not target_user:
            message = {"error": f"User with id {user_id} does not exist"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=message)
        else:
            update_user = target_user
            for field, value in body.model_dump().items():
                setattr(update_user, field, value)
            session.commit()
            session.refresh(update_user)

        response_update_user = {
         "user_id": update_user.id_number,
         "username": update_user.username,
         "password": update_user.password,
         "is_admin": update_user.is_admin,
        }

    message = {"message": f"User with id {user_id} updated",
               "new_value": response_update_user}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)
