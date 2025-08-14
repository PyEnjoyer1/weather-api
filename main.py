from fastapi import FastAPI




app = FastAPI()


@app.get("/{city}")
async def root(city: str):
    
    return {"message": "Hello World"}