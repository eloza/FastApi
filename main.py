from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

# Cheap database as a list
db: List[User] = [
    User(
        id=uuid4(),
        first_name="Janet",
        last_name="Weiss",
        gender=Gender.female,
        roles=[Role.student],
    ),
    User(
        id=uuid4(),
        first_name="Brad",
        last_name="Majors",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
]


@app.get("/")
async def root():
    return {"hello": "world"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"message": "User registered successfully", "id": user.id, "user": user}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted successfully"}
    raise HTTPException(
        status_code=404, detail=f"user with id {user_id} does not exist"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return {"message": "User updated successfully"}
    raise HTTPException(
        status_code=404, detail=f"User with id: {user_id} does not exist."
    )
