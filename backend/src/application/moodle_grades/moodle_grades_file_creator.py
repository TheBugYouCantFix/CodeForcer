import io
import csv
from datetime import datetime
from collections import defaultdict

from contracts.moodle_results_data import MoodleResultsData, ProblemData


class MoodleGradesFileCreator:
    def create_file(self, results_data: MoodleResultsData) -> tuple[io.StringIO, str]:
        filename = f"moodle_grades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        student_grade_map: defaultdict[str, list[float | str]] = defaultdict(lambda: [0, ''])

        file = io.StringIO()
        writer = csv.writer(file)
        writer.writerow(['Email', 'Grade', 'Feedback'])

        self.mark_grades(results_data.contest.problems, student_grade_map)
        self.mark_plagiarism(results_data.plagiarizers, student_grade_map)

        self.write_to_file(writer, student_grade_map)

        return file, filename

    def mark_grades(self, problems: list[ProblemData], student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for problem in problems:
            self.update_grades(problem, student_grade_map)

    @staticmethod
    def update_grades(problem: ProblemData, student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for submission in problem.submissions:
            problem_points = submission.points / problem.max_points * problem.max_grade

            student_grade_map[submission.author_email][0] += problem_points

    @staticmethod
    def mark_plagiarism(plagiarizers: list[str], student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for email in plagiarizers:
            student_grade_map[email] = [0, 'Plagiarism detected']

    @staticmethod
    def write_to_file(writer: csv.writer, student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for email, (grade, feedback) in student_grade_map.items():
            writer.writerow([email, grade, feedback])
