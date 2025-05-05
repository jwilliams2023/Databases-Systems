-- Drop child tables first
DROP TABLE IF EXISTS db_order_detail;
DROP TABLE IF EXISTS db_order;
DROP TABLE IF EXISTS db_book;

-- Then drop parent tables
DROP TABLE IF EXISTS db_employee;
DROP TABLE IF EXISTS db_customer;
DROP TABLE IF EXISTS db_shipper;
DROP TABLE IF EXISTS db_supplier;
DROP TABLE IF EXISTS db_subject;

-- Create db_subject Table
CREATE TABLE db_subject (
    SubjectID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(100) NOT NULL
);

-- Create db_supplier Table
CREATE TABLE db_supplier (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    CompanyName VARCHAR(100) NOT NULL,
    ContactLastName VARCHAR(50),
    ContactFirstName VARCHAR(50),
    Phone VARCHAR(20)
);

-- Create db_employee Table
CREATE TABLE db_employee (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    LastName VARCHAR(50) NOT NULL,
    FirstName VARCHAR(50) NOT NULL
);

-- Create db_book Table
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

-- Create db_customer Table
CREATE TABLE db_customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    LastName VARCHAR(50) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    Phone VARCHAR(20)
);

-- Create db_shipper Table
CREATE TABLE db_shipper (
    ShipperID INT PRIMARY KEY AUTO_INCREMENT,
    ShipperName VARCHAR(100) NOT NULL
);

-- Create db_order Table
CREATE TABLE db_order (
    OrderID INT PRIMARY KEY,  -- Removed AUTO_INCREMENT
    CustomerID INT NOT NULL,
    EmployeeID INT NOT NULL,
    OrderDate DATE NOT NULL,
    ShippedDate DATE DEFAULT NULL,
    ShipperID INT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES db_customer(CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES db_employee(EmployeeID),
    FOREIGN KEY (ShipperID) REFERENCES db_shipper(ShipperID)
);

-- Create db_order_detail Table
CREATE TABLE db_order_detail (
    OrderDetailID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT NOT NULL,
    BookID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES db_order(OrderID),
    FOREIGN KEY (BookID) REFERENCES db_book(BookID)
);