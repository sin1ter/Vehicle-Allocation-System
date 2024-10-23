from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import Optional

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
class AllocationStatus(str, Enum):
    allocated = "allocated",
    deallocated = "deallocated"

class VehicleAllocation(BaseModel):
    employee_id: str
    vehicle_id: str
    status: Optional[AllocationStatus] = AllocationStatus.allocated
    allocation_date: date
    
class VehicleAllocationHistory(BaseModel):
    employee_id: str
    vehicle_id: str
    status : AllocationStatus
    allocation_date: date
