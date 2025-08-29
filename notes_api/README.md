Notes API
An API to manage personal notes with user authentication, a database, and file backup.

Project Structure
The project follows a clean, modular structure to ensure maintainability and clarity.

```
notes_api/
├── app/
│   ├── main.py
│   ├── database.py
|   |-- security.py
│   ├── models.py
│   ├── middleware/
│   │   ├── __init__.py  <-- New empty file
│   │   └── request_counter.py
│   └── routers/
│       ├── __init__.py <-- empty file
|       |-- users.py  
│       └── notes.py
├── requirements.txt
└── README.md
```


🚀 Features
User Authentication: Securely register and log in users using JSON Web Tokens (JWT).

Note Management:

Create, retrieve, update, and delete (CRUD) notes.

All notes are tied to a specific authenticated user.

Database Integration: Stores user and note data in an SQLite database using SQLModel.

Request Counter Middleware: A custom middleware that counts and logs the total number of requests received by the API.

File Backup: An endpoint to back up all notes to a local JSON file.

CORS Configuration: Securely handles cross-origin requests, allowing a frontend application to interact with the API.

🛠️ Installation
Prerequisites
Python 3.8+

pip (Python package installer)

Steps
Clone the Repository (if applicable)

Bash

git clone <your-repo-url>
cd notes_api
Create a Virtual Environment
It's recommended to work in a virtual environment to manage project dependencies.

Bash

python -m venv venv
Activate the Virtual Environment

On Windows:

Bash

.\venv\Scripts\activate
On macOS and Linux:

Bash

source venv/bin/activate
Install Dependencies
Install all required packages using pip.

Bash

pip install fastapi "uvicorn[standard]" sqlmodel passlib[bcrypt] python-jose[cryptography] colorama
🚀 Running the API
Start the Server
Run the application using Uvicorn. The app.main:app part points to the app object inside the main.py file within the app directory.

Bash

uvicorn app.main:app --reload
The --reload flag will automatically restart the server whenever you make changes to the code.

Access the API Documentation
Once the server is running, open your web browser and navigate to the following URL to see the interactive documentation.

http://127.0.0.1:8000/docs

This page allows you to test all API endpoints directly from your browser.

🔑 API Endpoints
User Endpoints (/users)
POST /users/register: Registers a new user.

POST /users/token: Logs in a user and returns a JWT access token.

Notes Endpoints (/notes)
POST /notes/: Creates a new note (requires authentication).

GET /notes/: Retrieves all notes for the authenticated user (requires authentication).

GET /notes/{note_id}: Retrieves a specific note by ID (requires authentication).

DELETE /notes/{note_id}: Deletes a specific note by ID (requires authentication).

POST /notes/backup: Backs up all notes to a notes_backup.json file.

📝 Usage Example
Register a User:
Go to /docs, expand the users section, and use the POST /users/register endpoint with a username and password.

Get an Access Token:
Use the POST /users/token endpoint with the same username and password to get a JWT access token. Copy the token.

Create a Note:

Click the Authorize button at the top right of the /docs page.

Paste your JWT token into the Value field (preceded by Bearer, e.g., Bearer eyJhbGci...).

Now you can use the POST /notes/ endpoint to create a note.

Access Other Protected Endpoints:
With the authorization token set, you can now try the GET, PUT, and DELETE endpoints for notes.