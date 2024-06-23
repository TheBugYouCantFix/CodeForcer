from fastapi import FastAPI, status
from uvicorn import run
from contracts.student_data import StudentData
from students_service import StudentsService
from infrastructure.persistence.db_students_repository import DBStudentsRepository
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

repository = DBStudentsRepository('students.db')
service = StudentsService(repository)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )


@app.get("/")
async def root():
    return "initial project"


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentData):
    return service.create_student(student_data)


@app.get("/students/{email_or_handle}", status_code=status.HTTP_200_OK)
async def get_student_by_email_or_handle(email_or_handle: str):
    return service.get_student_by_email_or_handle(email_or_handle)


@app.put("/students/{email}", status_code=status.HTTP_200_OK)
async def update_student(email: str, updated_student_data: StudentData):
    return service.update_student(email, updated_student_data)


@app.delete("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(email: str):
    return service.delete_student(email)


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
