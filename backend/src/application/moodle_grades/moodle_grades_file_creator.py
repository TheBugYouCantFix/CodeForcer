from fastapi.responses import FileResponse

import csv
from datetime import datetime
from typing import Dict

from contracts.moodle_results_data import MoodleResultsData, ProblemData


class MoodleGradesFileCreator:
    student_grade_map: Dict[str, float] = {}

    def create_file(self, results_data: MoodleResultsData) -> FileResponse:
        filename = f"moodle_grades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Email', 'Grade', 'Feedback'])

            for problem in results_data.contest.problems:
                self.update_grades(problem)

        for email, grade in self.student_grade_map.items():
            if email in results_data.plagiarizers:
                self.student_grade_map[email] = 0
                writer.writerow([email, grade, 'Plagiarism detected'])
            else:
                writer.writerow([email, grade, ''])

        return FileResponse(filename, filename=filename, media_type='csv')

    def update_grades(self, problem: ProblemData) -> None:
        for submission in problem.submissions:
            problem_points = submission.points / problem.max_points * problem.max_grade

            if self.student_grade_map.get(submission.author_email) is None:
                self.student_grade_map[submission.author_email] = problem_points
            else:
                self.student_grade_map[submission.author_email] += problem_points
