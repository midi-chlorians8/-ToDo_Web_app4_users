from fastapi import Depends, FastAPI

from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from sqlalchemy.util._concurrency_py3k import greenlet_spawn
from fastapi import Depends, HTTPException
from app.schemas import NoteCreate, NoteRead, NoteUpdate
from app.db import Note, get_user_db
from fastapi_users import FastAPIUsers
from uuid import UUID
from app.users import *
app = FastAPI()
from fastapi_users.models import ID, OAP, UP
from typing import Type
from sqlalchemy.orm import Session
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import insert
from pydantic import parse_obj_as



fastapi_users = FastAPIUsers[User, UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
    # user = await greenlet_spawn(userdb.get, userdb.user_table.id)

 # user2: User= userdb.user_table.id
    # user2 = await greenlet_spawn(userdb.get, userdb.user_table.id)
@app.post("/notes", response_model=NoteRead, dependencies=[Depends(current_active_user)])
async def create_note(
    note: NoteCreate,  current_user: User = Depends(current_active_user),userdb:SQLAlchemyUserDatabase=Depends(get_user_db)
):
    # user_table = userdb.user_table
    # # user_db = await greenlet_spawn(userdb.get, current_user,current_user.id)
    # db_note = Note(**note.dict(), user_id=current_user.id)
    # # current_user.notes.append(db_note)
    # # user_table.add(db_note)
    # # await user_table.commit()
    # # await user_table.refresh(db_note)
    # return db_note
    # db_note = Note(**note.dict(), user_id=current_user.id)
    # userdb.session.add(db_note)
    # userdb.session.commit()
    # userdb.session.refresh(db_note)
    # return {
    #     "id": db_note.id,
    #     "title": db_note.title,
    #     "content": db_note.content,
    #     "user_id": db_note.user_id,
    # }
    db_note.drop_all()
    note_dict = parse_obj_as(dict, note)

    stmt = insert(Note).values(**note_dict).returning(Note.id)
    result = await userdb.session.execute(stmt)
    new_id = result.fetchone()[0]

    # db_note = Note(**note.dict(), user_id=current_user.id)
    # db_note.id = result.scalars().first()
    

    db_note = Note(**note.dict(), id=new_id, user_id=current_user.id)
    # db_note.id = new_id
    userdb.session.add(db_note)

    await userdb.session.commit()
    await userdb.session.refresh(db_note)
    return db_note.as_dict()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()