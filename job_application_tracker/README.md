Job Application Tracker API
This project is a RESTful API built with FastAPI and SQLModel to track job applications. It features a relational database, user authentication, role-based access control, and a custom middleware. The API is designed to allow users to manage their own applications while providing administrators with full control over public job listings.

Features
Relational Database: Uses SQLModel to define and manage two primary tables: JobListing (public job posts) and JobApplication (user-specific applications).

Authentication & Authorization: Implements JWT-based authentication to secure endpoints.

Role-Based Access Control:

Admin-Only Endpoints: For creating, updating, and deleting job listings.

User-Only Endpoints: For applying to listings and viewing personal applications.

Public Endpoints: For viewing all job listings.

Search Functionality: Allows users to search for job listings by position and company.

Middleware: Includes a custom middleware to enforce the presence of the User-Agent header, rejecting requests that do not specify a client.

CORS Configuration: Securely allows requests from specified origins, enabling cross-origin communication with a frontend application.

Project Structure
The project follows a clean, modular structure to ensure maintainability and clarity.

```
job_application_tracker/
├── app/
│   ├── main.py                # Main application entry point
│   ├── database.py              # Handles database connection and sessions
│   ├── models.py                # Defines all SQLModel database tables and Pydantic schemas
│   ├── security.py              # Manages password hashing and JWT token logic
│   ├── middleware/
│   │   └── user_agent.py      # Middleware to check for the User-Agent header
│   └── routers/
│       ├── users.py           # Handles user registration and authentication
│       └── listings.py          # Manages all job listings and applications logic
├── requirements.txt           # Project dependencies
└── README.md                  # This file
```

Setup & Installation
1. Clone the repository
Bash

git clone <your_repo_link>
cd job_application_tracker
2. Create a virtual environment
It is recommended to use a virtual environment to manage project dependencies.

Bash

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
3. Install dependencies
Install all required libraries using the requirements.txt file.

Bash

pip install -r requirements.txt
4. Run the application
Run the application using Uvicorn. The --reload flag enables auto-reloading on code changes.

Bash

uvicorn app.main:app --reload
Upon the first run, the database file (job_tracker.db) will be created automatically, and default admin and user accounts will be seeded for testing purposes.

API Endpoints
The API documentation is available at http://127.0.0.1:8000/docs once the server is running. You can interact with all endpoints directly from this page.

Admin Credentials (for testing)
Username: admin

Password: admin_password

User Credentials (for testing)
Username: testuser

Password: test_password

Endpoints List
Public Endpoints
GET /listings/ - Retrieve all public job listings.

GET /listings/search?position=<query>&company=<query> - Search for listings by position or company.

User Endpoints (Authentication Required)
POST /listings/apply - Apply to a specific job listing.

GET /listings/my-applications - View a list of all your submitted applications.

Admin Endpoints (Authentication Required - Admin Role)
POST /listings/ - Create a new job listing.

PUT /listings/{listing_id} - Update an existing job listing.

DELETE /listings/{listing_id} - Delete a job listing.

GET /listings/all-applications - View all applications submitted by all users.

How to Test
1. Get a Token
Use the POST /users/token endpoint with the appropriate username and password to get an access token.

2. Authorize
Click the "Authorize" button in the Swagger UI and enter your token in the format Bearer <your_token>.

3. Test Endpoints
Admin-Only: Use the admin token to test creating, updating, and deleting listings.

User-Only: Use the user token to test applying to a listing and viewing your applications.

Public: Access these endpoints without any authentication to see them work.