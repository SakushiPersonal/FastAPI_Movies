from fastapi import FastAPI

app = FastAPI()
app.title = "First FastAPI App " #Here we select the title of our App
app.version = "0.0.2" #Here we can indicate our actual app version 

@app.get('/', tags=['home'])#With tags we can separate our diferents routes by name to identify them easily.
def message():
    return "Hello world!"