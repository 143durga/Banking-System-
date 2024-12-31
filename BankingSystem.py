import mysql.connector

# Establish MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="Durga@2002",  # Replace with your MySQL password
        database="BankingSystem"
    )

# Create and modify Account table
def create_and_modify_account_table():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Create Account table
        create_table_query = """
        CREATE TABLE Account (
            account_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
            account_type ENUM('Saving', 'Checking') NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        print("Account table created successfully.")

        # Add account_number column
        add_column_query = "ALTER TABLE Account ADD COLUMN account_number VARCHAR(20) NOT NULL;"
        cursor.execute(add_column_query)
        print("Column 'account_number' added successfully.")

        # Modify account_type column
        modify_column_query = "ALTER TABLE Account MODIFY account_type ENUM('Saving', 'Checking', 'Savings') NOT NULL;"
        cursor.execute(modify_column_query)
        print("Column 'account_type' modified successfully.")

        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# CREATE: Add a new customer
def create_customer(name, email, contact_number, address):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the email already exists in the database
    cursor.execute("SELECT * FROM customer WHERE email = %s", (email,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        print(f"Customer with email '{email}' already exists.")
    else:
        query = "INSERT INTO customer (name, email, contact_number, address) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, contact_number, address))
        connection.commit()
        print(f"Customer '{name}' added successfully.")

    cursor.close()
    connection.close()

# CREATE: Add a new account
def create_account(customer_id, account_number, account_type):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "INSERT INTO Account (customer_id, account_number, account_type) VALUES (%s, %s, %s)"
    cursor.execute(query, (customer_id, account_number, account_type))
    connection.commit()

    print(f"Account '{account_number}' created successfully.")

    cursor.close()
    connection.close()

# READ: Fetch customer details by email
def get_customer_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM customer WHERE email = %s"
    cursor.execute(query, (email,))
    customer = cursor.fetchone()

    if customer:
        print(f"Customer Found: {customer}")
    else:
        print("Customer not found.")

    cursor.close()
    connection.close()

# UPDATE: Update customer details
def update_customer(email, name=None, contact_number=None, address=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    update_query = "UPDATE customer SET "
    update_values = []

    if name:
        update_query += "name = %s, "
        update_values.append(name)
    if contact_number:
        update_query += "contact_number = %s, "
        update_values.append(contact_number)
    if address:
        update_query += "address = %s, "
        update_values.append(address)

    # Remove trailing comma and space
    update_query = update_query.rstrip(", ")

    update_query += " WHERE email = %s"
    update_values.append(email)

    cursor.execute(update_query, tuple(update_values))
    connection.commit()

    print(f"Customer with email '{email}' updated successfully.")

    cursor.close()
    connection.close()

# DELETE: Delete customer by email
def delete_customer(email):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete the customer record and associated accounts and transactions
    query = "DELETE FROM customer WHERE email = %s"
    cursor.execute(query, (email,))
    connection.commit()

    print(f"Customer with email '{email}' deleted successfully.")

    cursor.close()
    connection.close()

# Initialize and modify the Account table
create_and_modify_account_table()

# Example Usage:

# CREATE: Add new customers
create_customer("Alice Smith", "alice@example.com", "9876543210", "456 Street, City")
create_customer("Bob Johnson", "bob@example.com", "1234567890", "789 Avenue, City")

# CREATE: Add new account for Alice
create_account(1, "AC00123456", "Savings")

# READ: Fetch customer details by email
get_customer_by_email("alice@example.com")

# UPDATE: Update Alice's contact number
update_customer("alice@example.com", contact_number="9876543222")

# DELETE: Delete customer by email
delete_customer("bob@example.com")
