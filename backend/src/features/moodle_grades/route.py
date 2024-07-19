from fastapi import APIRouter

from .create_grades_file import router as create_grades_router
from .get_submission_selectors import router as submission_selectors_router

router = APIRouter()

router.include_router(create_grades_router)
router.include_router(submission_selectors_router)
