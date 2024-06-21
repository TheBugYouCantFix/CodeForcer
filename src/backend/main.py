from fastapi import FastAPI, status
from uvicorn import run
from contracts.student_data import StudentData
from students_service import StudentsService
from db_students_repository import DBStudentsRepository
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
repository = DBStudentsRepository('students.db')
service = StudentsService(repository)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.get("/")
async def root():
    return "initial project"


@app.post("/students")
async def create_student(student: StudentData, status_code=status.HTTP_201_CREATED):
    return service.create_student(student)


@app.get("/students/{email_or_handle}")
async def get_student_by_email_or_handle(email_or_handle: str, status_code=status.HTTP_200_OK):
    return service.get_student_by_email_or_handle(email_or_handle)


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
