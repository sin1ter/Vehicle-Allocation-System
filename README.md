
# Project Title

A brief description of what this project does and who it's for


# Welcome to Vehicle Allocation Management API 👋

![Version](https://img.shields.io/badge/version-v1-blue.svg?cacheSeconds=2592000)


## Features

- **Vehicle Management:**
  - Create, update, and delete vehicle records.
  - Ensure unique vehicle IDs and plate numbers using MongoDB indexes.
  - Retrieve detailed information about each vehicle.
  
- **Employee Management:**
  - Add, update, and remove employee records.
  - Ensure unique employee IDs through MongoDB indexes.
  - Retrieve detailed information about each employee.
  
- **Vehicle Allocation:**
  - Allocate vehicles to employees for specific dates.
  - Allow vehicle allocations only for today's date or future dates, preventing allocations for past dates.
  - Ensure that each vehicle can only be allocated to one employee at a time.
  - Ensure that an employee can only have one active vehicle allocation.
  - Update vehicle allocations before the allocated date. Updates are restricted on or after the allocation date.
  
- **Allocation History:**
  - Track vehicle allocation history, storing past allocations for reporting purposes.
  - Generate reports based on allocation history with customizable filters for better data insights.
## Run Locally

Clone the project

```bash
  git clone https://github.com/sin1ter/vehicle-allocation-api.git
```

Go to the project directory

```bash
  cd Vehicle-Allocation-System
```

# For Windows
```bash 
   python -m venv env

   env\Scripts\activate
```

 # For macOS/Linux
 ```bash
   python3 -m venv env
   
   source env/bin/activate
   ```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload
```
# Access the API documentation:
  Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to view the interactive API documentation.


## API Reference


#### Employee Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **POST** | `/api/employees` | To create a new employee record |
| **GET** | `/api/employees` | To retrieve all employees |
| **GET** | `/api/employees/:employeeId` | To retrieve details of a single employee |
| **PUT** | `/api/employees/:employeeId` | To update the details of a single employee |
| **DELETE** | `/api/employees/:employeeId` | To delete a single employee |

#### Vehicle Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **POST** | `/api/vehicles` | To create a new vehicle record |
| **GET** | `/api/vehicles` | To retrieve all vehicles |
| **GET** | `/api/vehicles/:vehicleId` | To retrieve details of a single vehicle |
| **PUT** | `/api/vehicles/:vehicleId` | To update the details of a single vehicle |
| **DELETE** | `/api/vehicles/:vehicleId` | To delete a single vehicle |


#### Vehicle Allocation Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **POST** | `/api/allocate-vehicle` | To allocate a vehicle to an employee |
| **GET** | `/api/allocations` | To retrieve all vehicle allocations |
| **GET** | `/api/allocations/:allocationId` | To retrieve details of a specific vehicle allocation |
| **PUT** | `/api/allocations/:allocationId` | To update an existing vehicle allocation before the allocated date |
| **DELETE** | `/api/allocations/:allocationId` | To delete a vehicle allocation before the allocated date |

#### Vehicle Allocation History Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **GET** | `/api/allocation-history` | To retrieve all allocation history |


## Author

👤 **Symon**

- Github: [@sin1ter](https://github.com/sin1ter)
