from fastapi import FastAPI, status
from uvicorn import run
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from domain.student import Student
from contracts.student_data import StudentData
import container

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentData) -> Student:
    return container.students_service.create_student(student_data)


@app.get("/students/{email_or_handle}", status_code=status.HTTP_200_OK)
async def get_student_by_email_or_handle(email_or_handle: str) -> Student:
    return container.students_service.get_student_by_email_or_handle(email_or_handle)


@app.put("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(email: str, updated_student_data: StudentData) -> None:
    container.students_service.update_student(email, updated_student_data)


@app.delete("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(email: str) -> None:
    container.students_service.delete_student(email)


@app.get("/contests/{contest_id}/results", status_code=status.HTTP_200_OK)
async def get_results(contest_id: int, key: str, secret: str):
    return container.contests_service.get_contest(contest_id, key, secret)


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
