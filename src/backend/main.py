from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

@app.get("/")
async def root():
    return "initial project"

if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
