from fastapi import FastAPI, UploadFile, File, status
from uvicorn import run
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from domain.student import Student
from contracts.student_data import StudentData
from container import students_service, contests_service

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentData) -> Student:
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


#not implemented yet
@app.get("/contests/{contest_id}", status_code=status.HTTP_200_OK)
async def get_contest(contest_id: int, key: str, secret: str):
    return contests_service.get_contest(contest_id, key, secret)


@app.post("/upload-csv", status_code=status.HTTP_201_CREATED)
async def upload_csv(file: UploadFile = File(...)):
    students_service.process_csv_file(file)


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
