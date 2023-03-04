from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middleware.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.auth import auth_router
import uvicorn
import os


app = FastAPI()
app.title = "First FastAPI App " #Here we select the title of our App
app.version = "0.1.9" #Here we can indicate our actual app version 
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(auth_router)


Base.metadata.create_all(bind=engine)  

'''Not really nedded JsonResponse because FastAPI return by default in that format, is just nedded in a specific moments '''


#home
@app.get('/', tags=['home'], status_code=status.HTTP_200_OK)#With tags we can separate our diferents routes by name to identify them easily.
def message():
    return HTMLResponse(status_code=status.HTTP_200_OK, content='<h1>Hello world!</h1>')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)))