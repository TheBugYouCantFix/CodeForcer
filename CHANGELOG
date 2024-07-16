🚀 Features

    Added db student repository.
    Implemented create_student method for students_service.py.
    Added status code retrieval and student get request.
    Added 400 exceptions.
    Completed API CRUD.
    Created CodeForces request sender with auth.
    Added stub function for get_contest.
    Made emails and handles case-insensitive.
    Began to implement the feature.
    Added necessary CodeForces models.
    Contest status retrieval works.
    Domain redesign.
    Domain methods for contest.
    Implemented getting contest with mapped emails but without submissions selections.
    Implemented select_single_submission_for_each_student method for contest.
    Added selection logic to application layer with stub selector.
    Added Moodle results data.
    Refined Moodle results data.
    Implemented MoodleGradesFileCreator.
    Completed MoodleGradesFileCreator and Moodle grades endpoint.
    Added lower method to the student class.
    Implemented validate_handle method.
    Refactored a method and inserted it into student creation.
    Added CORS middleware.
    code_forces_contests_provider.py now accepts two request senders factories as injected dependencies.
    Created (copied) DependenciesContainer.
    API uses new dependencies container.
    Added assignment name to MoodleResultsData and wrote it to the beginning of the CSV file.
    Added start time and duration to domain Contest.
    Added start time and duration to contracts Contest.
    Made separate contest page.
    Worked on undefined participants copying.
    Change states, data validation, onloading event, routing.
    Made requests with environment variable for contests and handles.
    Divided form components, added for single handles.
    Added methods to students_repository.py interface.
    Implemented update or create logic for PUT request.
    Added get_all_students to students_repository.
    Added get_all_students to students_service.
    Added get_all_students endpoint.
    Implemented update or create logic for PUT /students/file.
    Added CodeForces health check when calling it.
    Bad request response for creating student with invalid handle.
    Proper response message for student not found.
    Added handle validation when updating student.
    Added the main fields of LateSubmissionRulesData base model.
    Added submission time to SubmissionData.
    Implemented late submission policy.
    Added faker package.
    Primitive domain contest faking.
    Advanced contests faking.
    Changed form elements.
    Moved student-related files to features/students.
    Handled penalty (0.0 <= penalty <= 1.0).
    Separated contests service into two features.
    Merged all logic of creation Moodle grades file into a single file.
    Extracted create_student endpoint into create_student.py.
    Extracted all students features into separate files.
    Table of contents in README.md.
    Updated table of contents.
    Changed styles for more visual control.
    Changed styles, logging, error messages.
    Created faker for POST Moodle grades request data.
    Made generated Moodle grades data look more real.
    Added adaptive for main structure.
    Added adaptive for theme button on mobile.
    Changed globals for adaptive.
    Made adaptive for mobile.
    Made responsive for settings page.
    Added logic for logging result.
    Changed file request, changed method.
    Changed request method.
    Update or create student by email or handle.

🐛 Bug Fixes

    Fixed db name typo.
    Fixed status code display.
    student_exists method fix.
    Submission points are float now.
    Fixed accessing test contest.
    Made student_grade_map a method object instead of a field.
    Fixed file creation problem.
    Replaced ContestParticipant with Student with nullable email.
    Removed nonexistent import.
    Added contests_provider injection into students_service in container.py.
    Entered right origins.
    Handle null points.
    Renamed points to max_points in Problem.
    Replaced number values of enums with actual names.
    Made Application services transient.
    Removed plagiarism-related fields and logic.
    Handled null emails.
    Removed unnecessary field.
    CfPhase brought back.
    Added start time and duration to contest.
    Changed homepage to root directory, changed links.
    Removed unnecessary imports and props.
    Resolve problem with request double sending.
    Resolved URL bug, changed initial states.
    Add conditional rendering for no submissions case.
    Changed styles to more general.
    Changed request method and URL.
    Removed visual bugs.
    Fixed non-stable timezone for contest start_time.
    Added file deletion.
    Code style.
    Merge request conflicts.
    Standard import "datetime.datetime" should be placed before third party import.
    Updated tests to match new domain.
    Added submission time.
    Renamed the submission time field.
    Fixed unrelated tests.
    Properly redid try-except statement in code_forces_request_sender.py.
    Fixed HTTPExceptions in db_students_repository.py.
    Fixed late submission policy.
    Made student hashable.
    Tests __init__.py.
    Linter fix.
    Fixed filename.
    Actually added __init__.py everywhere.
    Matched .gitlab-ci.yml with folders restructure.
    Fixed imports in main.py.
    Endpoints routing works now.
    docker-compose.yml root path.
    Changed dockerfiles.
    Fixed path for pylint.
    Fixed the response JSON error.
    Added timeout to get requests.
    Removed deprecated Hashable.
    Removed unnecessary .keys() for dict iterating.
    Typo in README.md.
    Deleted wrong requirement.
    Saving data in db after rebuild.
    Added more logging, error responses.
    Added new path for config.
    Fixed problem with infinite redirection.
    Contest duration.
    Deleted unneeded CORS.
    Moved students.db to db directory.
    Docker compose volume and DB_CONNECTION_STRING in env.
    Linting.
    Changed responsive styles.
    Responsive.
    Unexpected visual bug with bottom of the page.
    Unexpected visual bug with bottom of the page.
    Visual bugs.
    StudentsRepository interface.

🛠️ Refactors

    Cosmetic changes.
    Cleanup commit.
    Renamed to match the domain.
    Improved naming in students_service.py and extracted method to function.
    Swapped functions to match CRUD order.
    Improved naming in main.py.
    Replaced creating db with ensuring it is created.
    Moved persistence-related modules into infrastructure.
    Separated external imports from internal imports.
    Moved singleton_meta.py to utils.
    Moved students_service.py and students_repository.py into application.students.
    Renamed persistence to storage.
    Moved all dependent entities of Contest into contest.py and refactored them.
    Merged Phase and Verdict enums into a single file enums.py.
    Renamed get contest endpoint.
    Moved dependencies to container.py.
    Renamed service to students_service.
    Renamed repository to students_repository.
    Deleted root endpoint.
    Extracted all contests-related logic from presentation layer to infrastructure.
    Added return types to endpoint functions.
    Replaced success status code for PUT student to 204 no content.
    Removed JSON serialization from contests provider.
    Renamed contests/{contest_id} endpoint to contests/{contest_id}/results.
    Moved all files into frontend folder.
    Refined import of container into main.py.
    Removed unnecessary return statement.
    Swapped backend and src folders.
    Cosmetic changes.
    Extracted parsing of contest standings code_forces_request_sender.py.
    Merged scrap_results function into get_contest_results method.
    Made send_request method private.
    Replaced BaseModels with dataclasses.
    Added prefix Cf to all CodeForces dataclasses.
    Moved all CodeForces-related files into infrastructure/code_forces.
    Extracted parsing of CodeForces objects into separate functions.
    Added __future__ annotations.
    Changed signature of select_single_submission_for_each_student to use selector from list.
    Optimizations.
    Removed asterisk (*) imports.
    Added separate methods for marking grades, plagiarism, and writing to file.
    Added defaultdict instead of a regular dict.
    Used __future__ annotations to get rid of quotes in typehints.
    Improved the for loop.
    Removed case insensitivity from main.py.
    Removed unnecessary lower_data method from student_data.py.
    Added case insensitivity to db_students_repository.py.
    Added dependency injection for contests_provider in StudentsService.
    Introduced constant for CodeForces API URL.
    Renamed field in problem.
    Renamed endpoint to /students/bulk.
    Moved a couple of things.
    Created match case expression for file extensions.
    Moved code_forces_request_sender.py and created interfaces for it.
    Refactored dependencies_container.
    Moved ensuring DB creation into DBContext.
    Made StudentsRepository transient.
    Swapped attributes of ContestData.
    Replaced boundary with router.
    Replaced elements with object routing.
    Moved API functions to separate file.
    Changed structure for components, made several separate instead.
    Made POST method as exported function, changes inside method.
    Made an environment variable for URL.
    Divide forms, made them separate.
    Made /students/file request PUT.
    Removed else.
    Removed verdict enum from domain.
    Fixed list typehints.
    Removed unnecessary lambdas.
    Replaced unused parameter with _.
    Fixed linter issues.
    Formatting fixes.
    Specified test names.
    BaseModels in moodle_results_data.py.
    BaseModels in student_data.py.
    Removed unnecessary directory nesting.
    Replaced number status codes with proper enums.
    Exceptions formatting.
    Refactor.
    Renamed LateSubmissionRulesData to LateSubmissionPolicyData.
    time_expired to extra_time.
    Renamed a field.
    Use contest faking for map_handles_to_emails test.
    Renamed tests/domain folder, deleted unneeded folder.
    Removed URLs.
    Removed environment vars.
    Changed Dockerfile and nginx config.
    Made the variable snake_case.
    Added the final pylint recommendation.
    Renamed unit test files.
    Added watch for development containerization.
    Pylint fixes.
    Added almost hot update for development mode.
    Pylint fixes.
    Changed folders, separated styled components.
    Added more data to grades object.
    Changed inner props, added navigation status control.
    Added separated components, made form for late policy settings.

⚙️ Miscellaneous Tasks

    Created frontend folder.
    Added missed dependencies to requirements.txt.
    Moved frontend folder to root.
    Deleted README.md.
    Moved remaining files into frontend folder.
    Updated requirements.txt.
    Removed deprecated comment.
    Fixed formatting.
    Fixed formatting.
    Transferred creation of the filename to API layer.
    Added contest name to the header row of the file for clarity.
    Removed phase attribute.
    Removed unnecessary dependencies.
    Add console logging for clarification.
    Add new red color.
    Renamed tests folder to tests.
    Additional empty lines.
    Added __init__.py everywhere, made backend to be the root, moved tests to root.
    Moved Dockerfile and .gitignore to root.
    Got rid of student_data.py.
    Moved contests-related files to features/contests.
    Moved Moodle grades-related files to features/moodle_grades.
    Moved CodeForces infrastructure files to features/contests/code_forces.
    Got rid of infrastructure directory.
    Added another origin for CORS.
    Removed unnecessary rule.
    Fixed linting problems.
    Removed env directory from compose.
    Deleted useless logo.
    Updated logging, design.
    Fixed linting.
    Added blank data for grades request.
    Removed useless font linking.

