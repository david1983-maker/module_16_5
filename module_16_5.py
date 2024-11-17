from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')
# users = {'1': "Имя:Example,возраст:18"}
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get(path='/user/{user_id}')
def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id]})


@app.post('/user/{username}/{age}')
def post_user(username: str, age: int) -> User:
    if users:
        user_id = users[-1].id + 1
    else:
        user_id = 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int, username: str, age: int, user: str = Body()) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
        else:
            raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id)
        return f'{user_id} DELETE'
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")
