from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.features.students.router import router as students_router
from src.features.contests import router as contests_router
from src.features.moodle_grades import router as moodle_grades_router

app = FastAPI()
app.include_router(students_router)
app.include_router(contests_router)
app.include_router(moodle_grades_router)

origins = [
    "https://code-forcer.netlify.app",
    "http://code-forcer.netlify.app",
    "http://mashfeii.ru",
    "https://mashfeii.ru",
    "http://codeforcer.mashfeii.ru"
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://10.90.137.106:5173",
    "http://10.90.137.106:80",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
