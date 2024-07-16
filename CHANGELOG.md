# Changelog

### 🚀 Features

- Added db student repository.
- Completed API CRUD for students and contests.
- Created CodeForces request sender with auth.
- Implemented MoodleGradesFileCreator and endpoint.
- Made emails and handles case-insensitive.
- Added CORS middleware.
- Created (copied) DependenciesContainer.
- Added assignment name to MoodleResultsData CSV file.
- Implemented update or create logic for PUT request and bulk student endpoint.
- Added health check for CodeForces.
- Implemented late submission policy.
- Added faker package for testing.
- Moved student-related files to `features/students`.
- Separated contests service into two features.
- Refactored to improve naming and structure.
- Added adaptive and responsive design for mobile.
- Changed styles for better visual control.
- Enhanced logging and error messages.

### 🐛 Bug Fixes

- Fixed db name typo.
- Corrected status code and response message handling.
- Fixed issues with file creation and request double sending.
- Handled null points and emails.
- Fixed timezone stability for contest start_time.
- Addressed merge conflicts and linter issues.
- Resolved URL bugs and infinite redirection.
- Fixed routing and imports in Docker and main.py.

### 🛠️ Refactors

- Improved naming conventions and method extraction.
- Moved persistence-related modules to infrastructure.
- Separated external and internal imports.
- Added return types to endpoint functions.
- Optimized code by removing unnecessary lambdas and imports.
- Renamed and reorganized folders and files for better clarity.
- Replaced number status codes with proper enums.
- Changed Dockerfile and nginx config.
- Enhanced code readability and maintainability.

### ⚙️ Miscellaneous Tasks

- Updated `requirements.txt`.
- Improved logging and console messages.
- Fixed formatting and linting issues.
- Added `__init__.py` to necessary directories.
- Moved tests and Dockerfile to root directory.
- Removed unnecessary dependencies and files.
- Enhanced documentation and code comments.
