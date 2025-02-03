from fastapi import Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder

router_movie = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
    overview: str = Field(default='Descripcion de la pelicula', min_length=5, max_length=60)
    year: str = Field(default='2025', min_length=4, max_length=4)
    rating: int = Field(ge=1, le=10)
    category: str = Field(default='Categoria', min_length=3, max_length=15)

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'prueba@prueba.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')

@router_movie.get('/movies', tags=['movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

# Busqueda por parametro que mete el usuario
@router_movie.get('/movies/{id}', tags=['movies'], status_code=200)
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(id == ModelMovie.id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

# Buqueda por queryparams (no los mete el usuario)
@router_movie.get('/movies/', tags=['movies'], status_code=200)
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    db = Session()
    data = db.query(ModelMovie).filter(category == ModelMovie.category).first()
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@router_movie.post('/movies', tags=['movies'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    new_movie = ModelMovie(**dict(movie))
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={'message': 'Se ha cargado una nueva pelicula', 'movies': [dict(movie) for m in ModelMovie]})

@router_movie.put('/movies/{id}', tags=['movies'], status_code=200)
def update_movie(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(id == ModelMovie.id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'No se encontro el recurso'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(content={'message': 'Se ha modificado la pelicula'})

# Busqueda por parametro que mete el usuario
@router_movie.delete('/movies/{id}', tags=['movies'], status_code=200)
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(id == ModelMovie.id).first()
    if not data:
        return JSONResponse(content={'message': 'No se encontro el recurso'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Se ha eliminado la pelicula'})
