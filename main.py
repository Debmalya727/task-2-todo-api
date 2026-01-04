# task-2-todo-api/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse  # <--- Added this import
from datetime import datetime
from bson import ObjectId

# Import our own modules
from database import users_collection, tasks_collection
from models import UserCreate, TaskModel, TaskUpdate
from auth import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

app = FastAPI(title="Smart ToDo API")

# This tells FastAPI that the URL "/token" is where users go to login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- HELPER FUNCTION: Get Current User ---
# This protects routes. It checks if the user has a valid token.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = users_collection.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return user

# --- AUTH ROUTES ---

@app.post("/signup", status_code=201)
async def signup(user: UserCreate):
    # 1. Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Hash the password
    hashed_password = get_password_hash(user.password)
    
    # 3. Save to MongoDB
    new_user = {
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    users_collection.insert_one(new_user)
    return {"message": "User created successfully"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Find user
    user = users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # 2. Create JWT Token
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- TASK ROUTES (CRUD) ---

@app.post("/tasks", status_code=201)
async def create_task(task: TaskModel, current_user: dict = Depends(get_current_user)):
    new_task = task.dict()
    new_task["owner_email"] = current_user["email"] # Link task to the logged-in user
    new_task["created_at"] = datetime.utcnow()
    
    result = tasks_collection.insert_one(new_task)
    return {"id": str(result.inserted_id), "message": "Task created"}

@app.get("/tasks")
async def get_my_tasks(current_user: dict = Depends(get_current_user)):
    # Only fetch tasks belonging to the currently logged-in user
    tasks_cursor = tasks_collection.find({"owner_email": current_user["email"]})
    
    tasks = []
    for task in tasks_cursor:
        task["id"] = str(task["_id"]) # Convert ObjectId to string
        del task["_id"] # Remove the raw ObjectId object
        tasks.append(task)
    return tasks

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user)):
    # Create a filter to ensure user only updates THEIR OWN task
    query = {"_id": ObjectId(task_id), "owner_email": current_user["email"]}
    
    # Remove None values so we don't overwrite data with empty fields
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    result = tasks_collection.update_one(query, {"$set": update_data})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    
    return {"message": "Task updated successfully"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    query = {"_id": ObjectId(task_id), "owner_email": current_user["email"]}
    result = tasks_collection.delete_one(query)
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
        
    return {"message": "Task deleted successfully"}

# --- ROOT REDIRECT ---
# This ensures http://127.0.0.1:8000 automatically goes to the docs
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")