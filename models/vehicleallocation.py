from pydantic import BaseModel
from enum import Enum
from datetime import date


# Employee Model
class EmployeeInformation(BaseModel):
    employee_id: str
    first_name: str
    last_name: str

# Vehicle Model
class VehicleInformation(BaseModel):
    vehicle_id: str
    model: str
    plate_number: str
    year: int
    color: str

# Vehicle Allocation Model
class VehicleAllocation(BaseModel):
    employee_id: str
    vehicle_id: str
    allocation_date: date

class AllocationStatus(str, Enum):
    allocated = "allocated",
    deallocated = "deallocated"
    
class VehicleAllocationHistory(BaseModel):
    employee_id: str
    vehicle_id: str
    status : AllocationStatus
    allocation_date: date
