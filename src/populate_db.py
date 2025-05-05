import csv
import os
import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': os.environ.get('DB_USER', 'jgw0052'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'host': 'sysmysql8.auburn.edu',
    'database': 'jgw0052db', 
    
}

# Establish connection to MySQL
def connect_to_database():
    try:
        conn = mysql.connector.connect(**config)
        print("Database connection successful.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

# Function to drop tables if they exist
def drop_tables(conn, table_names):
    cursor = conn.cursor()
    for table in table_names:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table};")
            print(f"Table {table} dropped successfully.")
        except mysql.connector.Error as err:
            print(f"Error dropping table {table}: {err}")
    conn.commit()
    cursor.close()

# Function to create tables
def create_tables(conn):
    cursor = conn.cursor()
    try:
        # Create db_subject Table
        cursor.execute("""
        CREATE TABLE db_subject (
            SubjectID INT PRIMARY KEY AUTO_INCREMENT,
            CategoryName VARCHAR(100) NOT NULL
        );
        """)

        # Create db_supplier Table
        cursor.execute("""
        CREATE TABLE db_supplier (
            SupplierID INT PRIMARY KEY AUTO_INCREMENT,
            CompanyName VARCHAR(100) NOT NULL,
            ContactLastName VARCHAR(50),
            ContactFirstName VARCHAR(50),
            Phone VARCHAR(20)
        );
        """)

        # Create db_employee Table
        cursor.execute("""
        CREATE TABLE db_employee (
            EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
            LastName VARCHAR(50) NOT NULL,
            FirstName VARCHAR(50) NOT NULL
        );
        """)

        # Create db_customer Table
        cursor.execute("""
        CREATE TABLE db_customer (
            CustomerID INT PRIMARY KEY AUTO_INCREMENT,
            LastName VARCHAR(50) NOT NULL,
            FirstName VARCHAR(50) NOT NULL,
            Phone VARCHAR(20)
        );
        """)

        # Create db_shipper Table
        cursor.execute("""
        CREATE TABLE db_shipper (
            ShipperID INT PRIMARY KEY AUTO_INCREMENT,
            ShipperName VARCHAR(100) NOT NULL
        );
        """)

        # Create db_book Table
        cursor.execute("""
        CREATE TABLE db_book (
            BookID INT PRIMARY KEY AUTO_INCREMENT,
            Title VARCHAR(150) NOT NULL,
            UnitPrice DECIMAL(10, 2) NOT NULL,
            Author VARCHAR(100),
            Quantity INT NOT NULL,
            SupplierID INT,
            SubjectID INT,
            FOREIGN KEY (SupplierID) REFERENCES db_supplier(SupplierID),
            FOREIGN KEY (SubjectID) REFERENCES db_subject(SubjectID)
        );
        """)

        # Create db_order Table
        cursor.execute("""
        CREATE TABLE db_order (
            OrderID INT PRIMARY KEY,  -- Removed AUTO_INCREMENT to allow explicit insertion
            CustomerID INT NOT NULL,
            EmployeeID INT NOT NULL,
            OrderDate DATE NOT NULL,
            ShippedDate DATE DEFAULT NULL,
            ShipperID INT,
            FOREIGN KEY (CustomerID) REFERENCES db_customer(CustomerID),
            FOREIGN KEY (EmployeeID) REFERENCES db_employee(EmployeeID),
            FOREIGN KEY (ShipperID) REFERENCES db_shipper(ShipperID)
        );
        """)

        # Create db_order_detail Table
        cursor.execute("""
        CREATE TABLE db_order_detail (
            OrderDetailID INT PRIMARY KEY AUTO_INCREMENT,
            OrderID INT NOT NULL,
            BookID INT NOT NULL,
            Quantity INT NOT NULL,
            FOREIGN KEY (OrderID) REFERENCES db_order(OrderID),
            FOREIGN KEY (BookID) REFERENCES db_book(BookID)
        );
        """)

        print("All tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
    cursor.close()

# Function to read CSV files and insert data into the database
def insert_data_from_csv(conn, table_name, csv_file_path, columns, auto_increment_columns=[]):
    cursor = conn.cursor()
    columns_to_insert = [col for col in columns if col not in auto_increment_columns]
    placeholders = ", ".join(["%s"] * len(columns_to_insert))
    columns_str = ", ".join(columns_to_insert)
    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            values = tuple(
                None if col not in row or row[col].strip().upper() == 'NULL' or row[col] == ''
                else row[col] for col in columns_to_insert
            )
            try:
                cursor.execute(sql, values)
            except mysql.connector.Error as err:
                print(f"Error inserting data into {table_name}: {err}. Data: {values}")

    conn.commit()
    cursor.close()
    print(f"Data inserted into {table_name} from {csv_file_path}.")

# Main script to drop, recreate tables, and insert data
def main():
        conn = connect_to_database()
        if not conn:
            return

        # List of tables to drop and recreate (child tables first)
        tables = [
            'db_order_detail',
            'db_order',
            'db_book',
            'db_employee',
            'db_customer',
            'db_shipper',
            'db_supplier',
            'db_subject'
        ]

        print("Dropping existing tables...")
        drop_tables(conn, tables)

        print("Creating tables...")
        create_tables(conn)

        # Define your CSV files and their corresponding table information
        csv_files_info = {
            './data/db_subject.csv': ('db_subject', ['SubjectID', 'CategoryName'], ['SubjectID']),
            './data/db_supplier.csv': ('db_supplier', ['SupplierID', 'CompanyName', 'ContactLastName', 'ContactFirstName', 'Phone'], ['SupplierID']),
            './data/db_employee.csv': ('db_employee', ['EmployeeID', 'LastName', 'FirstName'], ['EmployeeID']),
            './data/db_customer.csv': ('db_customer', ['CustomerID', 'LastName', 'FirstName', 'Phone'], ['CustomerID']),
            './data/db_shipper.csv': ('db_shipper', ['ShipperID', 'ShipperName'], ['ShipperID']),
            './data/db_book.csv': ('db_book', ['BookID', 'Title', 'UnitPrice', 'Author', 'Quantity', 'SupplierID', 'SubjectID'], ['BookID']),
            './data/db_order.csv': ('db_order', ['OrderID', 'CustomerID', 'EmployeeID', 'OrderDate', 'ShippedDate', 'ShipperID'], []),  # Include OrderID
            './data/db_order_detail.csv': ('db_order_detail', ['OrderID', 'BookID', 'Quantity'], [])  # Adjusted columns
        }

        # Insert data from CSV files
        for file_path, (table_name, columns, auto_increment_cols) in csv_files_info.items():
            print(f"Inserting data from {file_path} into {table_name}...")
            insert_data_from_csv(conn, table_name, file_path, columns, auto_increment_columns=auto_increment_cols)

        conn.close()
        print("All data inserted successfully.")

if __name__ == "__main__":
    main()