from fastapi import FastAPI, Body
from pydantic import BaseModel


app = FastAPI()

class Movie(BaseModel):
    id:int
    title: str
    overview: str
    year: int
        
        



movies = [
    {
  "id": 5,
  "title": "la mascara",
  "overview": "hola mundo",
  "year": 2024,
  "rating": 10,
  "category": "suspenso"
    },
    {
  "id": 4,
  "title": "romulus alien",
  "overview": "hola mundo",
  "year": 2024,
  "rating": 10,
  "category": "suspenso"
    },
        {
  "id": 7,
  "title": "prometeo",
  "overview": "hola mundo",
  "year": 2024,
  "rating": 10,
  "category": "suspenso"
    }
    
]
app.title = "que pasa gentita"
app.version = "2.2.0"
@app.get('/', tags=["home"])
def home():
    return "hola mundo"
@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies
@app.post('/movies', tags=['Movies'])
def create_movie(id: int = Body(),
                 title: str=Body(),
                 overview:str= Body(), 
                 year:int = Body(),
                 rating:float = Body(),
                 category:str = Body()):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category,
        
    })
    return movies
@app.put('/movies/{id}', tags=['Movies'])
def update_movies(
    id:int,
                 title: str=Body(),
                 overview:str= Body(), 
                 year:int = Body(),
                 rating:float = Body(),
                 category:str = Body()):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
    return movies

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int): 
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return movies

 