from datetime import date, datetime, time

# Serializer for EmployeeInformation
def employee_serializer(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "employee_id": employee["employee_id"],
        "first_name": employee["first_name"],
        "last_name": employee["last_name"]
    }

# Serializer for VehicleInformation
def vehicle_serializer(vehicle) -> dict:
    return {
        "id": str(vehicle["_id"]),
        "vehicle_id": vehicle["vehicle_id"],
        "model": vehicle["model"],
        "plate_number": vehicle["plate_number"],
        "year": vehicle["year"],
        "color": vehicle["color"]
    }

# Serializer for VehicleAllocation
def allocation_serializer(allocation) -> dict:

    allocation_date = allocation["allocation_date"]
    
    # Convert date to datetime if it's a date object
    if isinstance(allocation_date, date):
        allocation_date = datetime.combine(allocation_date, time.min)
        
    return {
        "id": str(allocation["_id"]),
        "employee_id": allocation["employee_id"],
        "vehicle_id": allocation["vehicle_id"],
        "allocation_date": allocation["allocation_date"]
    }

# Serializer for VehicleAllocationHistory

def allocation_history_serializer(allocation_history) -> dict:

    allocation_date = allocation_history["allocation_date"]

    if isinstance(allocation_date, date):
        allocation_date = datetime.combine(allocation_date, time.min)

    return {
        "id": str(allocation_history["_id"]),
        "employee_id": allocation_history["employee_id"],
        "vehicle_id": allocation_history["vehicle_id"],
        "status": allocation_history["status"],
        "allocation_date": allocation_history["allocation_date"]
    }

# List serializers for each model
def list_employees(employees) -> list:
    return [employee_serializer(employee) for employee in employees]

def list_vehicles(vehicles) -> list:
    return [vehicle_serializer(vehicle) for vehicle in vehicles]

def list_allocations(allocations) -> list:
    return [allocation_serializer(allocation) for allocation in allocations]

def list_allocation_history(allocation_history) -> list:
    return [allocation_history_serializer(history) for history in allocation_history]