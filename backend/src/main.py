from fastapi import FastAPI
from uvicorn import run

from src.features.students.route import router as students_router
from src.features.contests.route import router as contests_router
from src.features.moodle_grades.route import router as moodle_grades_router
from src.features.moodle_grades.submissions_archive import router as submissions_archive_router

app = FastAPI(title='CodeForcer')

app.include_router(students_router, prefix='/api/students')
app.include_router(contests_router, prefix='/api/contests')
app.include_router(moodle_grades_router, prefix='/api/moodle-grades')
app.include_router(submissions_archive_router, prefix='/api/')


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
