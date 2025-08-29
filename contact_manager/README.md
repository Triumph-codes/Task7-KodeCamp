Contact Manager API
A secure and robust API for managing personal contacts, built with FastAPI, SQLModel, and modern security practices.
```
contact_manager/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── security.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── ip_logger.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       └── contacts.py
├── requirements.txt
└── README.md
```


🚀 Features
User Authentication: Secure user registration and login using JWT (JSON Web Tokens). All contact management operations are restricted to authenticated users.

Contact Management: Full CRUD (Create, Read, Update, Delete) functionality for contacts.

Data Persistence: Uses SQLModel with an SQLite database to reliably store user and contact information.

Security: Implements password hashing with bcrypt and token-based authentication with python-jose.

Custom Middleware: Includes a custom middleware that logs the IP address of every incoming request.

CORS Enabled: Configured to handle Cross-Origin Resource Sharing, allowing a separate frontend application to interact with the API.

Interactive Documentation: Automatically generated API documentation at /docs using FastAPI's integrated Swagger UI.

🛠️ Installation
Prerequisites
Python 3.8+

pip (Python package installer)

Steps
Clone the Repository

Bash

git clone <your-repo-url>
cd contact_manager
Create and Activate a Virtual Environment

Bash

python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
Install Dependencies
Install all required packages from requirements.txt. If you don't have one, you can install them manually:

Bash

pip install fastapi "uvicorn[standard]" sqlmodel passlib[bcrypt] python-jose[cryptography] colorama
🚀 Running the API
Start the Server
Run the application using Uvicorn. The --reload flag is great for development as it restarts the server on code changes.

Bash

uvicorn app.main:app --reload
Upon the first run, the lifespan function will automatically create the contacts.db file and the necessary database tables.

Access the API Documentation
Open your web browser and navigate to the following URL to view and interact with the API endpoints:

http://127.0.0.1:8000/docs

🔑 API Endpoints
User Endpoints (/users)
POST /users/register: Registers a new user.

POST /users/token: Logs in a user and returns a JWT access token. This token must be used for all subsequent protected endpoints.

Contacts Endpoints (/contacts)
POST /contacts/: Creates a new contact for the logged-in user.

GET /contacts/: Retrieves a list of all contacts belonging to the authenticated user.

PUT /contacts/{contact_id}: Updates an existing contact by ID.

DELETE /contacts/{contact_id}: Deletes a contact by ID.

General Endpoints
GET /: A simple welcome message to confirm the API is running.

📝 Usage Example
Register a User:

Open the /docs page.

Expand the users section and click on POST /users/register.

Click "Try it out", enter a username and password, then click "Execute".

Log In and Get a Token:

Expand POST /users/token.

Click "Try it out", enter the same username and password, and click "Execute".

Copy the access_token from the response.

Authorize Your Requests:

Click the Authorize button at the top of the docs page.

In the pop-up window, enter your token in the format Bearer YOUR_ACCESS_TOKEN (e.g., Bearer eyJhbGci...).

Click "Authorize" and close the window. The lock icons next to the protected endpoints should now appear "locked".

Manage Contacts:

You can now use any of the contacts endpoints to perform CRUD operations on your contacts.

For example, use POST /contacts/ to create a new contact for your user.