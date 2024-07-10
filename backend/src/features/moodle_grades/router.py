from datetime import datetime

from fastapi import APIRouter
from starlette import status
from starlette.responses import StreamingResponse

from src.container import container
from src.features.moodle_grades.models import MoodleResultsData
from src.features.moodle_grades.file_creator import MoodleGradesFileCreator

router = APIRouter()


@router.post("/moodle_grades", status_code=status.HTTP_200_OK)
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
