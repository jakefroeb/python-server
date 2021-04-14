import sqlite3
import json
from models import Employee, Location
EMPLOYEES = [
    {
      "name": "Jeremy Bakker",
      "locationId": 2,
      "id": 1
    },
    {
      "id": 2,
      "name": "Jerry Garcia",
      "locationId": 2
    },
    {
      "id": 3,
      "name": "Kyle Trask",
      "locationId": 3
    },
    {
      "id": 4,
      "name": "Steve-O",
      "locationId": 1
    },
    {
      "name": "duger",
      "locationId": 1,
      "id": 5
    }
]
def get_employees_by_location(location_id):
  with sqlite3.connect("./kennel.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    db_cursor.execute("""
    SELECT
      a.id,
      a.name,
      a.address,
      a.location_id
    FROM employee a
    WHERE a.location_id = ?
    """,(location_id, ))
    employees = []
    dataset = db_cursor.fetchall()
    for row in dataset:
      employee = Employee(row['id'], row['name'], row['address'],
                            row['location_id'])
      employees.append(employee.__dict__)
  return json.dumps(employees)
def get_all_employees():
  with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id,
            l.name location_name,
            l.address location_address
        FROM employee a
        JOIN location l
        ON l.id = a.location_id
        """)
        employees = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'],
                            row['location_id'])
            location = Location(row['location_id'], row['location_name'], row['location_address'])
            employee.location = location.__dict__
            employees.append(employee.__dict__)
  return json.dumps(employees)
    
def get_single_employee(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id
        FROM employee a
        WHERE a.id = ?
        """, ( id, ))
        data = db_cursor.fetchone()
        employee = Employee(data['id'], data['name'], data['address'],
                            data['location_id'])
        return json.dumps(employee.__dict__)

def create_employee(employee):
    employee["id"] = EMPLOYEES[-1]["id"] + 1
    EMPLOYEES.append(employee)
    return employee
def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)
def update_employee(id, new_employee):
    # Iterate the employeeS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Update the value.
            EMPLOYEES[index] = new_employee
            break