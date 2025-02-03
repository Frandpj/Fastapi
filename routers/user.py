from fastapi import APIRouter
from pydantic import BaseModel
from user_jwt import createToken
from fastapi.responses import JSONResponse

login_user = APIRouter()

class User(BaseModel):
    email: str
    password: str

@login_user.post('/login', tags=['authentication'])
def login(user: User):
    if user.email == 'prueba@prueba.com' and user.password == '123':
        token: str = createToken(dict(user))
        print(token)
        return JSONResponse(content=token)