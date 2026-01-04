# task-2-todo-api/database.py
from pymongo import MongoClient
import certifi

# ---------------------------------------------------------
# UPDATED CONNECTION STRING (New Cluster: vmbrk6c)
# ---------------------------------------------------------
MONGO_URI = "mongodb+srv://debmalyapanda2004_db_user:1dehlWc5A0t9bmtU@cluster0.vmbrk6c.mongodb.net/?appName=Cluster0"

try:
    # Connect with SSL fixes enabled (tlsAllowInvalidCertificates=True)
    # This handles both the connection and the Windows SSL issues
    client = MongoClient(
        MONGO_URI, 
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    
    # Create/Connect to the database named 'todo_db'
    db = client.todo_db
    
    users_collection = db["users"]
    tasks_collection = db["tasks"]
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")

except Exception as e:
    print(f"❌ Connection failed: {e}")