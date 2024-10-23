from fastapi import APIRouter, HTTPException
from datetime import datetime, date, time, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from bson import ObjectId

from pymongo.errors import DuplicateKeyError

from models.vehicleallocation import EmployeeInformation, VehicleInformation, VehicleAllocation, VehicleAllocationHistory, AllocationStatus
from config.database import (
    employee_collection, vehicle_collection, 
    vehicle_allocation_collection, vehicle_allocation_history_collection
    )
from schema.schemas import (
    list_employees, list_vehicles, 
    list_allocations, list_allocation_history
    )

router = APIRouter()

######### Employee Endpoints #######
# List employees
@router.get("/api/employees", tags=["Employees"], summary="Get All Employees",)
async def get_employees():
    """
    Retrieve a list of all employees in the system.
    
    - **Returns**: A list of employee records. If no employees are found, a message indicating this will be returned.
    """
    try:
        employees = list_employees(employee_collection.find())
        if not employees:
            return {"message": "No employees found."}
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a specific employee by ID
@router.get("/api/employees/{id}", tags=["Employees"], summary="Get Employee by ID")
async def get_employee(id:str):
    """
    Retrieve an employee's information by their unique ID.
    
    - **id**: The ID of the employee to retrieve.
    - **Returns**: The employee details as a JSON object.
    - **Raises**:
        - 404: If the employee is not found.
    """

    # Find the employee using the given ID
    employee = employee_collection.find_one({"_id": ObjectId(id)})
    # Check if exists
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Convert MongoDB document to a JSON-serializable format
    employee["_id"] = str(employee["_id"])
    return employee

# Create a new employee
@router.post("/api/employees", tags=["Employees"], summary="Create an Employee")
async def create_employee(employee:EmployeeInformation):
    """
    Create a new employee record.
    
    - **Request Body**: Employee details including `employee_id`, `first_name`, `last_name`.
    - **Returns**: A success message upon successful creation.
    - **Raises**:
        - 400: If an employee with the given ID already exists.
    """
    try:
        employee_collection.insert_one(dict(employee))
        return {"message" : "Employee added succesfully"}
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="Employee with given ID already exists."
        )

# Update an employee's details
@router.put("/api/employee/{id}", tags=["Employees"], summary="Update Employee Information")
async def update_employee(id:str, employee:EmployeeInformation):
    """
    Update an existing employee's information by their ID.
    
    - **id**: The ID of the employee to update.
    - **Request Body**: Updated employee details.
    - **Returns**: A success message upon successful update.
    - **Raises**:
        - 404: If the employee is not found.
    """
    result = employee_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(employee)}
    )
    if not result: 
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message" : "Employee updated succesfully"}

# Delete an employee by ID
@router.delete("/api/employee/{id}", tags=["Employees"], summary="Delete Employee Information")
async def delete_employee(id: str):
    """
    Delete an employee record by their unique ID.
    
    - **id**: The ID of the employee to delete.
    - **Returns**: A success message upon successful deletion.
    - **Raises**:
        - 404: If the employee is not found.
    """
    try:
        result = employee_collection.find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        employee_collection.delete_one({"_id": ObjectId(id)})

        return {"message": "Employee deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


######### Vehicle Endpoints #######

# List of Vehicles
@router.get("/api/vehicles", tags=["Vehicles"], summary="Get All Vehicles")
async def get_vehicles():
    """
    Retrieve a list of all vehicles in the system.

    - **Returns**: A list of vehicle records. If no vehicles are found, a message indicating this will be returned.
    """
    try:
        vehicles = list_vehicles(vehicle_collection.find())
        if not vehicles:
            return {"message": "No vehicles found."}
        return vehicles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a specific vehicle by ID
@router.get("/api/vehicle/{id}", tags=["Vehicles"], summary="Get Vehicle by ID")
async def get_vehicle(id:str):
    """
    Retrieve a vehicle by its unique ID.

    - **Parameters**:
        - **id**: The ID of the vehicle to retrieve.
        
    - **Returns**: The vehicle record if found; otherwise, a 404 error.
    """
    try:
        # Find the vehicle using the given ID
        vehicle = vehicle_collection.find_one({"_id": ObjectId(id)})
        # Check if exists
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # Convert MongoDB document to a JSON-serializable format
        vehicle["_id"] = str(vehicle["_id"])
        return vehicle
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create a new vehicle
@router.post("/api/vehicle", tags=["Vehicles"], summary="Create a Vehicle")
async def post_vehicle(vehicle: VehicleInformation):
    """
    Add a new vehicle to the system.

    - **Parameters**:
        - **vehicle**: The vehicle information to add.

    - **Returns**: A success message upon successful addition of the vehicle.
    """
    try:
        vehicle_collection.insert_one(dict(vehicle))
        return {"message" : "Vehicle added succesfully"}
    
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="Vehicle already exists."
        )

# Update an existing vehicle's information
@router.put("/api/vehicle-update/{id}", tags=["Vehicles"], summary="Update Vehicle Information")
async def put_vehicle(id: str, vehicle:VehicleInformation):
    """
    Update an existing vehicle's information.

    - **Parameters**:
        - **id**: The ID of the vehicle to update.
        - **vehicle**: The new vehicle information.

    - **Returns**: A success message upon successful update of the vehicle.
    """
    
    result = vehicle_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(vehicle)}
    )
    if not result:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"message" : "Vehicle updated succesfully"}

# Delete a vehicle by ID
@router.delete("/api/vehicle-delete/{id}", tags=["Vehicles"], summary="Delete Vehicle Information")
async def delete_vehicle(id:str):
    """
    Delete a vehicle from the system by its ID.

    - **Parameters**:
        - **id**: The ID of the vehicle to delete.

    - **Returns**: A success message upon successful deletion of the vehicle.
    """
    try:
        result = vehicle_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return {"message": "Vehicle deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


######### Vehicle Allocation Endpoints #######

# Vehicle Allocations
@router.get("/api/allocations", tags=["Vehicle Allocations"])
async def get_allocations():
    """
    Retrieve a list of all vehicle allocations.

    This endpoint returns all vehicle allocation records in the system. If no allocations are found, 
    a message indicating the absence of records is returned.

    - **Returns**:
        - 200 OK: A list of all vehicle allocations.
        - 200 OK: A message indicating that no vehicle allocations were found if the list is empty.
    
    - **Response Example**:
        - **If allocations exist**:
            [
                {
                    "_id": "64b5c4e4f5e37f2a6c56a92e",
                    "employee_id": "employee123",
                    "vehicle_id": "vehicle456",
                    "allocation_date": "2024-10-22T00:00:00",
                },
                ...
            ]
        - **If no allocations exist**:
            {
                "message": "No vehicle allocations found."
            }
    """
    try:
        allocations = list_allocations(vehicle_allocation_collection.find())
        if not allocations:
            return {"message": "No vehicle allocations found."}
        return allocations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a specific allocation by ID
@router.post("/api/allocate_vehicle", tags=["Vehicle Allocations"])
async def allocate_vehicle(allocation: VehicleAllocation):
    """
    Allocate a vehicle to an employee.

    This endpoint allocates a vehicle to an employee, provided the vehicle is not already allocated 
    and the employee does not already have another vehicle allocated. It also ensures that the 
    allocation date is today or a future date.

    - **Request Body**:
        - **allocation** (VehicleAllocation): An object containing the allocation details.
            - **employee_id**: The ID of the employee receiving the vehicle.
            - **vehicle_id**: The ID of the vehicle to be allocated.
            - **allocation_date**: The date of the allocation. Must be today or a future date.

    - **Returns**:
        - **200 OK**: A message indicating successful vehicle allocation.
            - **Example**: `{"message": "Vehicle allocation successful"}`
        - **400 Bad Request**: If the vehicle is already allocated or the employee has another vehicle.
            - **Example**: `{"detail": "This vehicle is already allocated to the specified employee."}`
            - **Example**: `{"detail": "This employee is already allocated to another vehicle."}`
        - **404 Not Found**: If the allocation date is before today.
            - **Example**: `{"detail": "Choose a correct date."}`
        - **500 Internal Server Error**: If an unexpected error occurs.
            - **Example**: `{"detail": "Error message detailing the issue"}`

    - **Request Example**:
        ```json
        {
            "employee_id": "employee123",
            "vehicle_id": "vehicle456",
            "allocation_date": "2024-10-23"
        }
        ```

    - **Response Example**:
        ```json
        {
            "message": "Vehicle allocation successful"
        }
        ```

    - **Validation Checks**:
        - Ensures that a vehicle can only be allocated to one employee at a time.
        - Ensures that an employee can only have one vehicle allocated to them at a time.
        - Verifies that the allocation date is not set to a past date.
    """
    try:
        # Check if the vehicle is already allocated to this employee
        existing_vehicle_allocation = vehicle_allocation_collection.find_one({
            "vehicle_id": allocation.vehicle_id
        })
        
        if existing_vehicle_allocation:
            raise HTTPException(
                status_code=400,
                detail="This vehicle is already allocated to the specified employee."
            )
        
        # Check if the employee already has a vehicle allocated
        existing_employee_allocation = vehicle_allocation_collection.find_one({
            "employee_id": allocation.employee_id
        })

        if existing_employee_allocation:
            raise HTTPException(
                status_code=400,
                detail="This employee is already allocated to another vehicle."
            )
        
        # Convert allocation_date to datetime if it's a date object
        if isinstance(allocation.allocation_date, date):
            allocation.allocation_date = datetime.combine(allocation.allocation_date, time.min)

        today_start = datetime.combine(date.today(), time.min)

        if allocation.allocation_date < today_start:
            raise HTTPException(
                status_code=404,
                detail="Choose a correct date."
            )
        
        # Insert the allocation
        allocation_data = {
            "employee_id" : allocation.employee_id,
            "vehicle_id" : allocation.vehicle_id,
            "status" : AllocationStatus.allocated.value,
            "allocation_date" : allocation.allocation_date,
        }
        vehicle_allocation_collection.insert_one(allocation_data)
        
        # Create a history record for this allocation
        history_entry = VehicleAllocationHistory(
            employee_id=allocation.employee_id,
            vehicle_id=allocation.vehicle_id,
            status=AllocationStatus.allocated,
            allocation_date=allocation.allocation_date,
        )

        # Convert history_entry to a dictionary and ensure datetime conversion for MongoDB
        history_entry_data = dict(history_entry)
        if isinstance(history_entry_data["allocation_date"], date):
            history_entry_data["allocation_date"] = datetime.combine(history_entry_data["allocation_date"], time.min)
        
        # # Save the history record to the history collection
        vehicle_allocation_history_collection.insert_one(history_entry_data)
        
        return {"message": "Vehicle allocation successful"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# Update an existing allocation by ID
@router.put("/api/update-allocate-vehicle/{id}", tags=["Vehicle Allocations"])
async def update_allocate_vehicle(id: str, allocation: VehicleAllocation):
    """
    Update an existing vehicle allocation.

    This endpoint allows updating an existing vehicle allocation, provided that the 
    allocation date has not yet been reached. Updates are not allowed on or after the 
    allocation date to ensure that only future allocations can be modified.

    - **Path Parameter**:
        - **id** (str): The ID of the allocation record to update.

    - **Request Body**:
        - **allocation** (VehicleAllocation): An object containing the updated allocation details.

    - **Returns**:
        - **200 OK**: A message indicating successful update of the vehicle allocation.
        - **404 Not Found**: If the allocation is not found or if the allocation date has passed.
    """
    try:
        # Retrieve the existing allocation to check the date
        existing_allocation = vehicle_allocation_collection.find_one({"_id": ObjectId(id)})
        if not existing_allocation:
            raise HTTPException(status_code=404, detail="Vehicle allocation not found")
        
        # Extract and convert the allocation date for comparison
        allocation_date = existing_allocation["allocation_date"]
        if isinstance(allocation_date, datetime):
            allocation_date = allocation_date.date()  # Convert to date for comparison

        # Ensure the update is only allowed if today is before the allocation date
        if date.today() >= allocation_date:
            raise HTTPException(
                status_code=404,
                detail="Cannot update vehicle allocation on or after the allocation date."
            )

        # Convert allocation_date to datetime if it's a date object for storage
        if isinstance(allocation.allocation_date, date):
            allocation.allocation_date = datetime.combine(allocation.allocation_date, time.min)
        
        # Update the allocation
        allocation_data = dict(allocation)
        vehicle_allocation_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": allocation_data}
        )
        
        return {"message": "Vehicle allocation updated successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# Delete an existing allocation by ID
@router.delete("/api/delete-allocate-vehicle/{id}", tags=["Vehicle Allocations"])
async def delete_allocate_vehicle(id:str, allocation: VehicleAllocation):
    """
    Delete a vehicle allocation record.

    This endpoint allows the deletion of a vehicle allocation, provided that the 
    allocation date has not yet been reached. Deletion is not permitted on or after 
    the allocation date to prevent removing past or active allocations.

    - **Path Parameter**:
        - **id** (str): The ID of the vehicle allocation record to delete.

    - **Returns**:
        - **200 OK**: A message indicating successful deletion of the vehicle allocation.
            - **Example**: `{"message": "Vehicle allocation deleted successfully"}`
        - **404 Not Found**: If the allocation is not found or if the allocation date has passed.
            - **Example**: `{"detail": "Vehicle allocation not found"}`
            - **Example**: `{"detail": "Cannot delete vehicle allocation on or after the allocation date."}`
        - **500 Internal Server Error**: If an unexpected error occurs.
            - **Example**: `{"detail": "Error message detailing the issue"}`

    - **Request Example**:
        - **URL**: `/delete-allocate-vehicle/64e7a1b9c3f2a5d0845f23c1`
        - **Method**: `DELETE`
        
    - **Response Example**:
        ```json
        {
            "message": "Vehicle allocation deleted successfully"
        }
        ```

    - **Validation Checks**:
        - Ensures that the allocation exists in the database using the provided `id`.
        - Converts the allocation date to a `datetime` object for comparison.
        - Verifies that the current date and time is before the allocation date to allow deletion.
    """
    try:
        existing_allocation = vehicle_allocation_collection.find_one(
                            {"_id": ObjectId(id)}
                            )
        if not existing_allocation:
            raise HTTPException(status_code=404, detail="Vehicle allocation not found")
        
        # Convert allocation date to a datetime object for comparision
        allocation_date = existing_allocation["allocation_date"]
        if isinstance(allocation_date, date):
            allocation_date = datetime.combine(allocation_date, datetime.min.time())

        if datetime.now() >= allocation_date:
            raise HTTPException(
                status_code=404,
                detail="Cannot delete vehicle allocation on or after the allocation date."
            )

        # Perform the deletion
        result = vehicle_allocation_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Vehicle allocation not found")
        
        return {"message": "Vehicle allocation deleted successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    

""" 
This block of code checks either a vehicle allocation passed over 1 month
if it is passed then it will delete it
"""
scheduler = BackgroundScheduler()

def expired_allocation():
    """
    Deletes allocations that have are over one manth duration.
    """
    two_minutes_ago = datetime.combine(date.today(), time.min) - timedelta(days=30)
    result = vehicle_allocation_collection.delete_many({
        "allocation_date": {"$lt": two_minutes_ago}
    })
    print(f"Expired allocations cleaned up: {result.deleted_count} records deleted")

scheduler.add_job(expired_allocation, 'interval', days=30)
scheduler.start()



######### Vehicle Allocation History Endpoints #######

# Retreve the history of a specific vehicle allocation
@router.get("/api/allocation-history/", tags=["Allocations History"])
async def get_allocation_history():
    """
    Retrieve all vehicle allocations with status 'allocated'.

    This endpoint returns a list of all vehicle allocations where the status is 'allocated'.

    - **Returns**:
        - **200 OK**: A list of allocations.
        - **404 Not Found**: If no allocations with 'allocated' status are found.
    """
    # Fetch allocations where the status is 'allocated'
    allocated_allocations = vehicle_allocation_collection.find({"status": "allocated"})
    
    # Serialize the allocations into a list
    try:
        result = list_allocations(allocated_allocations)
        
        # Check if the result is empty and return an appropriate message
        if not result:
            raise HTTPException(status_code=404, detail="No vehicle allocations.")
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Retrieve the history of a specific vehicle allocation from previous
@router.get("/api/old-allocation-history/", tags=["Allocations History"])
async def get_old_allocation_history():
    """
    Retrieve the history of all vehicle allocations.

    This endpoint fetches the complete history of vehicle allocations, including details 
    like allocation status, employee and vehicle IDs, and the date of allocation.

    - **Returns**: A list of all vehicle allocation history records.
        - **Example**:
            ```json
            [
                {
                    "employee_id": "64e7a1b9c3f2a5d0845f23c1",
                    "vehicle_id": "64e7a1b9c3f2a5d0845f23c2",
                    "status": "allocated",
                    "allocation_date": "2024-10-22T00:00:00"
                },
                {
                    "employee_id": "64e7a1b9c3f2a5d0845f23c3",
                    "vehicle_id": "64e7a1b9c3f2a5d0845f23c4",
                    "status": "returned",
                    "allocation_date": "2024-10-21T00:00:00"
                }
            ]
            ```

    - **Response Codes**:
        - **200 OK**: Returns a list of allocation history records.
        - **500 Internal Server Error**: If an unexpected error occurs.
            - **Example**: `{"detail": "Error message detailing the issue"}`

    - **Request Example**:
        - **URL**: `/allocation-history/`
        - **Method**: `GET`
        
    - **Response Example**:
        ```json
        [
            {
                "employee_id": "64e7a1b9c3f2a5d0845f23c1",
                "vehicle_id": "64e7a1b9c3f2a5d0845f23c2",
                "status": "allocated",
                "allocation_date": "2024-10-22T00:00:00"
            },
            {
                "employee_id": "64e7a1b9c3f2a5d0845f23c3",
                "vehicle_id": "64e7a1b9c3f2a5d0845f23c4",
                "status": "returned",
                "allocation_date": "2024-10-21T00:00:00"
            }
        ]
        ```

    - **Functionality**:
        - Fetches all records from the `vehicle_allocation_history_collection`.
        - Uses `list_allocation_history()` to format the records into a JSON-serializable list.
    """
    try:
        result = list_allocation_history(vehicle_allocation_history_collection.find())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    