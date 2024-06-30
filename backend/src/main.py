from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import StreamingResponse
from uvicorn import run
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from contracts.moodle_results_data import MoodleResultsData
from domain.contest import Contest
from domain.student import Student
from contracts.student_data import StudentData
from container import students_service, contests_service, moodle_grades_file_creator

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentData) -> Student | None:
    return students_service.create_student(student_data)


@app.get("/students/{email_or_handle}", status_code=status.HTTP_200_OK)
async def get_student_by_email_or_handle(email_or_handle: str) -> Student:
    return students_service.get_student_by_email_or_handle(email_or_handle)


@app.put("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(email: str, updated_student_data: StudentData) -> None:
    students_service.update_student(email, updated_student_data)


@app.delete("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(email: str) -> None:
    students_service.delete_student(email)


@app.get("/contests/{contest_id}/results", status_code=status.HTTP_200_OK)
async def get_results(contest_id: int, key: str, secret: str):
    return contests_service.get_contest_results(contest_id, key, secret)


@app.get("/contests/{contest_id}", status_code=status.HTTP_200_OK)
async def get_contest(contest_id: int, key: str, secret: str) -> Contest:
    contest = contests_service.get_contest(contest_id, key, secret)
    return contest


@app.post("/upload-csv", status_code=status.HTTP_201_CREATED)
async def upload_csv(file: UploadFile = File(...)):
    students_service.process_csv_file(file)


@app.post("/moodle_grades", status_code=status.HTTP_200_OK)
async def get_grades(results_data: MoodleResultsData) -> StreamingResponse:
    file, filename = moodle_grades_file_creator.create_file(results_data)
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
