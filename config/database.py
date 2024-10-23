from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://user:user@cluster0.jnngd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Select the database
db = client.vehicle_allocation

# Define collections
employee_collection = db["employees"]
vehicle_collection = db["vehicles"]
vehicle_allocation_collection = db["vehicle_allocations"]
vehicle_allocation_history_collection = db["vehicle_allocation_history"]

# Create unique indexes to ensure uniqueness of IDs
employee_collection.create_index("employee_id", unique=True)
vehicle_collection.create_index("vehicle_id", unique=True)
vehicle_collection.create_index("plate_number", unique=True)
