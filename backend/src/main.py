from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from uvicorn import run

from src.features.students.route import router as students_router
from src.features.contests.route import router as contests_router
from src.features.moodle_grades.route import router as moodle_grades_router

app = FastAPI(title='CodeForcer')

app.include_router(students_router, prefix='/api/students')
app.include_router(contests_router, prefix='/api/contests')
app.include_router(moodle_grades_router, prefix='/api/moodle-grades')


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
