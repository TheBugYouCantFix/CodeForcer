from datetime import datetime

from fastapi import FastAPI, status
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.features.students.router import router as students_router
from src.application.contests.contests_service import ContestsService
from src.application.moodle_grades.moodle_grades_file_creator import MoodleGradesFileCreator
from src.contracts.moodle_results_data import MoodleResultsData
from src.domain.contest import Contest
from src.container import container

app = FastAPI()
app.include_router(students_router)

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


@app.get("/contests/{contest_id}/results", status_code=status.HTTP_200_OK)
async def get_results(contest_id: int, key: str, secret: str):
    return container[ContestsService].get_contest_results(contest_id, key, secret)


@app.get("/contests/{contest_id}", status_code=status.HTTP_200_OK)
async def get_contest(contest_id: int, key: str, secret: str) -> Contest:
    return container[ContestsService].get_contest(contest_id, key, secret)


@app.post("/moodle_grades", status_code=status.HTTP_200_OK)
async def get_grades(results_data: MoodleResultsData) -> StreamingResponse:
    filename = f"moodle_grades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    file = container[MoodleGradesFileCreator].create_file(results_data)
    content_length = len(file.getvalue())
    file.seek(0)

    return StreamingResponse(
        file,
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'text/csv; charset=utf-8',
            'Content-Length': str(content_length),
        },
        media_type='text/csv'
    )


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
