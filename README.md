FastAPI Portfolio: A Series of Backend Projects

This repository contains a collection of five independent backend projects built using FastAPI. Each project is a self-contained application designed to demonstrate proficiency in building robust, secure, and well-structured APIs. The projects showcase a progression of skills, from fundamental API design to advanced features like database integration, authentication, and custom middleware.

```
📁 Repository Structure
The repository is organized with each task residing in its own folder. Each folder is a complete FastAPI project with a clean, modular structure.

```

Task_1_Student_Management_System/

Task_2_E-Commerce_API/

Task_3_Job_Application_Tracker/

Task_4_Notes_API/

Task_5_Contact_Manager_API/

```

Each project folder contains the following:

app/: The main application package.

main.py: The entry point of the application.

models.py: Defines SQLModel database schemas.

routers/: Contains modular API endpoints.

database.py: Handles database connection logic.

requirements.txt: Lists all project dependencies.

README.md: Provides specific instructions and details for that task.

```
✨ Key Concepts and Technologies
Across these projects, a variety of key backend development concepts and tools have been implemented:

FastAPI: The primary framework for building all APIs, leveraging its speed and asynchronous capabilities.

SQLModel: A powerful library for ORM (Object-Relational Mapping), combining the simplicity of Pydantic with the power of SQLAlchemy to define database models and schemas.

Dependency Injection: Extensively used for managing database sessions and handling security dependencies like user authentication.

JWT Authentication: Implemented a robust, token-based authentication system using python-jose for secure user access to protected routes.

Password Hashing: Utilized passlib with the bcrypt algorithm to securely store user passwords in the database.

Middleware: Custom middleware functions were developed to perform tasks such as:

Logging requests.

Counting total requests.

Adding custom headers (e.g., response time).

Rejecting requests based on headers.

CORS (Cross-Origin Resource Sharing): Configured the API to securely interact with frontend applications.

Modular Architecture: Projects are structured with routers to keep the codebase organized and scalable.

Database Management: Used SQLite as a lightweight database, with models and tables automatically created on application startup.

```
📝 Project Summaries
Task 1: Student Management System
A basic CRUD API to manage student records. This project introduced core concepts like SQLModel, database dependency injection, and basic file-based authentication.

Task 2: E-Commerce API
An API for a simplified e-commerce platform with public and admin-only endpoints. This task demonstrated a modular project structure, implemented JWT authentication, and added middleware for performance logging.

Task 3: Job Application Tracker
A secure application tracker where users can manage their job applications. Key features included user-specific data access, endpoint filtering via query parameters, and defensive middleware to handle missing headers.

Task 4: Notes API
A personal notes management system featuring CRUD operations. This project explored database and file storage, implemented a request-counting middleware, and configured CORS for multiple origins.

Task 5: Contact Manager API
A complete, end-to-end contact management system. This final project integrated all previously learned concepts, including JWT authentication, a relational database, and custom middleware to log client IP addresses. It serves as a comprehensive example of a production-ready FastAPI application.

```

How to Run
To run any of the projects, navigate to its respective directory, install the dependencies from the requirements.txt file, and run the uvicorn command as specified in that project's README.md