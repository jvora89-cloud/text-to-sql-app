import sqlite3

def create_database():
    """Create and populate the business database"""
    conn = sqlite3.connect('business.db')
    cursor = conn.cursor()

    # Create Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Departments (
            DepartmentID INTEGER PRIMARY KEY,
            DepartmentName TEXT NOT NULL
        )
    ''')

    # Create Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            EmployeeID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            DepartmentID INTEGER,
            Salary REAL,
            FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
        )
    ''')

    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY,
            ProductName TEXT NOT NULL,
            Category TEXT NOT NULL
        )
    ''')

    # Create Sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales (
            SaleID INTEGER PRIMARY KEY,
            EmployeeID INTEGER,
            ProductID INTEGER,
            SaleDate TEXT,
            Amount REAL,
            FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        )
    ''')

    # Insert Departments
    departments = [
        (1, 'Sales'),
        (2, 'Marketing'),
        (3, 'Engineering'),
        (4, 'Human Resources'),
        (5, 'Finance')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Departments VALUES (?, ?)', departments)

    # Insert Employees
    employees = [
        (1, 'John Smith', 1, 75000),
        (2, 'Sarah Johnson', 1, 68000),
        (3, 'Michael Brown', 1, 72000),
        (4, 'Emily Davis', 2, 65000),
        (5, 'David Wilson', 2, 70000),
        (6, 'Jennifer Garcia', 3, 95000),
        (7, 'Robert Martinez', 3, 98000),
        (8, 'Lisa Anderson', 3, 92000),
        (9, 'James Taylor', 4, 62000),
        (10, 'Maria Rodriguez', 5, 88000),
        (11, 'William Lee', 5, 85000),
        (12, 'Jessica White', 1, 71000)
    ]
    cursor.executemany('INSERT OR IGNORE INTO Employees VALUES (?, ?, ?, ?)', employees)

    # Insert Products
    products = [
        (1, 'Laptop Pro', 'Electronics'),
        (2, 'Wireless Mouse', 'Electronics'),
        (3, 'Office Chair', 'Furniture'),
        (4, 'Standing Desk', 'Furniture'),
        (5, 'Monitor 27"', 'Electronics'),
        (6, 'Keyboard Mechanical', 'Electronics'),
        (7, 'Desk Lamp', 'Furniture'),
        (8, 'Webcam HD', 'Electronics'),
        (9, 'Notebook Set', 'Stationery'),
        (10, 'Pen Collection', 'Stationery')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Products VALUES (?, ?, ?)', products)

    # Insert Sales
    sales = [
        (1, 1, 1, '2024-01-15', 1299.99),
        (2, 1, 5, '2024-01-20', 399.99),
        (3, 2, 3, '2024-01-25', 299.99),
        (4, 2, 4, '2024-02-01', 599.99),
        (5, 3, 1, '2024-02-05', 1299.99),
        (6, 3, 2, '2024-02-10', 29.99),
        (7, 1, 6, '2024-02-15', 149.99),
        (8, 12, 1, '2024-03-01', 1299.99),
        (9, 12, 5, '2024-03-05', 399.99),
        (10, 2, 7, '2024-03-10', 79.99),
        (11, 1, 8, '2024-03-15', 89.99),
        (12, 3, 9, '2024-04-01', 24.99),
        (13, 1, 10, '2024-04-05', 34.99),
        (14, 2, 1, '2024-10-15', 1299.99),
        (15, 12, 5, '2024-10-20', 399.99),
        (16, 1, 3, '2024-11-01', 299.99),
        (17, 3, 4, '2024-11-15', 599.99),
        (18, 2, 2, '2024-12-01', 29.99),
        (19, 1, 1, '2024-12-10', 1299.99),
        (20, 12, 6, '2024-12-20', 149.99)
    ]
    cursor.executemany('INSERT OR IGNORE INTO Sales VALUES (?, ?, ?, ?, ?)', sales)

    conn.commit()
    conn.close()
    print("✓ Business database created successfully!")

if __name__ == "__main__":
    create_database()
