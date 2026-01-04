# 🔐 Smart ToDo API (Task 2)

## Overview
**Smart ToDo API** is a robust RESTful backend system designed for secure task management. It features **JWT (JSON Web Token) Authentication**, ensuring that users can only access and modify their own tasks.

This project fulfills the **Task 2** requirements of the internship assessment, built using **Python** and **FastAPI** for high performance and automatic documentation.

## 🚀 Features
1.  **User Authentication:** Secure Login endpoint that issues **JWT Bearer Tokens**.
2.  **CRUD Operations:** Full Create, Read, Update, and Delete functionality for tasks.
3.  **Data Privacy:** Strict dependency injection ensures users cannot access tasks belonging to others.
4.  **Automatic Docs:** Interactive Swagger UI documentation generated automatically.

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python)
* **Server:** Uvicorn (ASGI)
* **Security:** Python-Jose (JWT), Passlib (Hashing), OAuth2

## ⚙️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.9+** installed.

### 2. Install Dependencies
Navigate to the project folder and install the required packages:

cd task-2-todo-api
pip install -r requirements.txt
(If you haven't created the requirements.txt file yet, see the section below).3. Run the ServerStart the API server using Uvicorn:Bashuvicorn main:app --reload
The server will start at http://127.0.0.1:8000.🧪 How to Test (Swagger UI)The easiest way to test the API is through the automatic interactive documentation.Open Docs: Go to http://127.0.0.1:8000/docs in your browser.Authorize:Click the Authorize button (top right).Username: adminPassword: secretClick Login (This generates and saves your JWT token).Test Endpoints:POST /tasks: Create a new task (e.g., {"title": "Finish Assessment", "description": "Write READMEs"}).GET /tasks: Execute this to see the list of tasks you just created.DELETE /tasks/{id}: Remove a task by its ID.📡 API Endpoints StructureMethodEndpointDescriptionAuth RequiredPOST/tokenLogin to get Access Token❌ NoGET/tasksRetrieve current user's tasks✅ YesPOST/tasksCreate a new task✅ YesPUT/tasks/{id}Update an existing task✅ YesDELETE/tasks/{id}Delete a task✅ Yes📂 
```text
Project StructurePlaintexttask-2-todo-api/
│
├── main.py          # API Routes and Business Logic
├── auth.py          # JWT Handling and Password Hashing
├── requirements.txt # Project Dependencies
└── README.md        # Documentation
```
Submitted as part of the Internship Technical Assessment 2025.


### ⚠️ Important: create the `requirements.txt` file
If you haven't created the `requirements.txt` file for Task 2 yet, create it inside the `task-2-todo-api` folder and paste this list so the recruiter can actually install the libraries:


fastapi
uvicorn[standard]
python-jose[cryptography]
passlib[bcrypt]

pydantic
