import sqlite3
import json
from models import Customer
CUSTOMERS = [
    {
      "id": 1,
      "name": "Hannah Hall",
      "address": "7002 Chestnut Ct",
      "email": "hannah@hannah.com"
    },
    {
      "id": 2,
      "name": "Jake Froeb",
      "address": "Wayne Manor",
      "email": "jake.herman.froeb@gmail.com"
    },
    {
      "id": 3,
      "name": "Luke Froeb",
      "address": "Big booby bungalo",
      "email": "luke@luke.com"
    },
    {
      "email": "herm@herm.com",
      "name": "herm her",
      "address": "asd 123 st",
      "id": 4
    }
]

def get_customers_by_email(email):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)
def get_all_customers():
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email,
            a.password
        FROM customer a
        """)
        customers = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'],
                            row['email'], row['password'])
            customers.append(customer.__dict__)
    return json.dumps(customers)
    
def get_single_customer(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email,
            a.password
        FROM customer a
        WHERE a.id = ?
        """, ( id, ))
        data = db_cursor.fetchone()
        customer = Customer(data['id'], data['name'], data['address'],
                            data['email'], data['password'])
        return json.dumps(customer.__dict__)

def create_customer(customer):
    customer["id"] = CUSTOMERS[-1]["id"] + 1
    CUSTOMERS.append(customer)
    return customer

def delete_customer(id):
    customer_index = -1
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            customer_index = index
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)
def update_customer(id, new_customer):
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            CUSTOMERS[index] = new_customer
            break