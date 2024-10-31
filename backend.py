from fastapi import FastAPI
import uvicorn


app = FastAPI()

# Define una ruta de FastAPI
@app.get("/")
async def read_root():
    return {"message": "Hello World"}
