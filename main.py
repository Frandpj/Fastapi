from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from bd.database import engine, Base
from routers.movie import router_movie
from routers.user import login_user


app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Primeros pasos de una api',
    version='0.0.1'
)

app.include_router(router_movie)
app.include_router(login_user)


Base.metadata.create_all(bind=engine)

@app.get('/', tags=['inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo</h2>')