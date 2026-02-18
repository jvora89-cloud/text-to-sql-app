import sqlite3

def create_database():
    """Create comprehensive multi-industry business database"""
    conn = sqlite3.connect('business.db')
    cursor = conn.cursor()

    # Create Companies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Companies (
            CompanyID INTEGER PRIMARY KEY,
            CompanyName TEXT NOT NULL,
            Industry TEXT NOT NULL,
            Location TEXT
        )
    ''')

    # Create Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Departments (
            DepartmentID INTEGER PRIMARY KEY,
            DepartmentName TEXT NOT NULL,
            CompanyID INTEGER,
            FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
        )
    ''')

    # Create Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            EmployeeID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Occupation TEXT NOT NULL,
            DepartmentID INTEGER,
            Salary REAL,
            HireDate TEXT,
            FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
        )
    ''')

    # Create Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY,
            CustomerName TEXT NOT NULL,
            Industry TEXT,
            ContactEmail TEXT
        )
    ''')

    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY,
            ProductName TEXT NOT NULL,
            Category TEXT NOT NULL,
            Price REAL,
            CompanyID INTEGER,
            FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
        )
    ''')

    # Create Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Projects (
            ProjectID INTEGER PRIMARY KEY,
            ProjectName TEXT NOT NULL,
            CompanyID INTEGER,
            Budget REAL,
            StartDate TEXT,
            EndDate TEXT,
            Status TEXT,
            FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
        )
    ''')

    # Create Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            TransactionID INTEGER PRIMARY KEY,
            EmployeeID INTEGER,
            CustomerID INTEGER,
            ProductID INTEGER,
            TransactionDate TEXT,
            Amount REAL,
            FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        )
    ''')

    # Insert Companies
    companies = [
        (1, 'TechVision Inc', 'Technology', 'San Francisco'),
        (2, 'HealthPlus Medical', 'Healthcare', 'New York'),
        (3, 'Global Finance Corp', 'Finance', 'Chicago'),
        (4, 'EduLearn Academy', 'Education', 'Boston'),
        (5, 'RetailMax Stores', 'Retail', 'Los Angeles'),
        (6, 'BuildRight Construction', 'Construction', 'Houston'),
        (7, 'GreenEnergy Solutions', 'Energy', 'Austin'),
        (8, 'FoodDelight Restaurants', 'Hospitality', 'Miami')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Companies VALUES (?, ?, ?, ?)', companies)

    # Insert Departments
    departments = [
        (1, 'Engineering', 1), (2, 'Sales', 1), (3, 'Marketing', 1),
        (4, 'Medical Staff', 2), (5, 'Administration', 2),
        (6, 'Investment Banking', 3), (7, 'Risk Management', 3),
        (8, 'Teaching', 4), (9, 'Curriculum Development', 4),
        (10, 'Store Operations', 5), (11, 'Supply Chain', 5),
        (12, 'Project Management', 6), (13, 'Architecture', 6),
        (14, 'Research', 7), (15, 'Operations', 7),
        (16, 'Kitchen', 8), (17, 'Customer Service', 8)
    ]
    cursor.executemany('INSERT OR IGNORE INTO Departments VALUES (?, ?, ?)', departments)

    # Insert Employees with diverse occupations
    employees = [
        (1, 'Alice Johnson', 'Software Engineer', 1, 120000, '2020-01-15'),
        (2, 'Bob Smith', 'Sales Manager', 2, 95000, '2019-06-20'),
        (3, 'Carol White', 'Marketing Director', 3, 110000, '2018-03-10'),
        (4, 'Dr. David Brown', 'Surgeon', 4, 350000, '2015-09-01'),
        (5, 'Emma Davis', 'Nurse', 4, 75000, '2021-02-14'),
        (6, 'Frank Wilson', 'Investment Banker', 6, 180000, '2017-05-05'),
        (7, 'Grace Lee', 'Financial Analyst', 7, 85000, '2020-11-30'),
        (8, 'Henry Garcia', 'High School Teacher', 8, 65000, '2016-08-22'),
        (9, 'Iris Martinez', 'Curriculum Designer', 9, 72000, '2019-01-10'),
        (10, 'Jack Taylor', 'Store Manager', 10, 68000, '2018-07-15'),
        (11, 'Kate Anderson', 'Supply Chain Analyst', 11, 78000, '2020-04-01'),
        (12, 'Leo Thomas', 'Project Manager', 12, 95000, '2017-12-05'),
        (13, 'Maria Rodriguez', 'Architect', 13, 105000, '2019-09-18'),
        (14, 'Nathan Clark', 'Research Scientist', 14, 92000, '2021-03-22'),
        (15, 'Olivia Lewis', 'Operations Manager', 15, 88000, '2018-11-11'),
        (16, 'Paul Walker', 'Executive Chef', 16, 82000, '2017-06-30'),
        (17, 'Quinn Hall', 'Restaurant Manager', 17, 70000, '2019-08-14'),
        (18, 'Rachel Young', 'Data Scientist', 1, 135000, '2021-05-20'),
        (19, 'Sam King', 'DevOps Engineer', 1, 115000, '2020-02-28'),
        (20, 'Tina Wright', 'Account Executive', 2, 87000, '2019-10-12')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Employees VALUES (?, ?, ?, ?, ?, ?)', employees)

    # Insert Customers
    customers = [
        (1, 'Acme Corporation', 'Manufacturing', 'contact@acme.com'),
        (2, 'Global Tech Partners', 'Technology', 'info@globaltech.com'),
        (3, 'Retail Solutions Inc', 'Retail', 'sales@retailsol.com'),
        (4, 'Healthcare Systems', 'Healthcare', 'admin@healthsys.com'),
        (5, 'Education First', 'Education', 'contact@edufirst.com'),
        (6, 'City Construction Co', 'Construction', 'projects@cityconstruct.com'),
        (7, 'Energy Investors Ltd', 'Finance', 'invest@energyinv.com'),
        (8, 'Food Services Group', 'Hospitality', 'orders@foodservices.com')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Customers VALUES (?, ?, ?, ?)', customers)

    # Insert Products
    products = [
        (1, 'Cloud Platform Subscription', 'Software', 5000, 1),
        (2, 'AI Analytics Tool', 'Software', 3500, 1),
        (3, 'Medical Equipment Package', 'Medical', 25000, 2),
        (4, 'Patient Care System', 'Software', 15000, 2),
        (5, 'Investment Portfolio', 'Financial Service', 10000, 3),
        (6, 'Risk Assessment Service', 'Financial Service', 8000, 3),
        (7, 'Online Course Platform', 'Education', 2000, 4),
        (8, 'Learning Management System', 'Software', 4500, 4),
        (9, 'Retail POS System', 'Hardware', 3000, 5),
        (10, 'Inventory Management Software', 'Software', 2500, 5),
        (11, 'Construction Management Software', 'Software', 6000, 6),
        (12, 'Solar Panel Installation', 'Energy', 20000, 7),
        (13, 'Energy Audit Service', 'Service', 3000, 7),
        (14, 'Catering Package', 'Food Service', 5000, 8),
        (15, 'Restaurant POS System', 'Hardware', 2800, 8)
    ]
    cursor.executemany('INSERT OR IGNORE INTO Products VALUES (?, ?, ?, ?, ?)', products)

    # Insert Projects
    projects = [
        (1, 'Cloud Migration', 1, 500000, '2024-01-01', '2024-12-31', 'In Progress'),
        (2, 'Hospital Expansion', 2, 2000000, '2023-06-01', '2025-06-30', 'In Progress'),
        (3, 'Digital Banking Platform', 3, 1500000, '2024-02-01', '2024-11-30', 'In Progress'),
        (4, 'New Curriculum Rollout', 4, 300000, '2024-01-15', '2024-08-15', 'Completed'),
        (5, 'Store Modernization', 5, 800000, '2024-03-01', '2024-09-30', 'In Progress'),
        (6, 'Office Complex Build', 6, 5000000, '2023-09-01', '2025-12-31', 'In Progress'),
        (7, 'Solar Farm Development', 7, 3000000, '2024-01-01', '2025-06-30', 'In Progress'),
        (8, 'Restaurant Chain Expansion', 8, 1200000, '2024-04-01', '2024-12-31', 'In Progress')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Projects VALUES (?, ?, ?, ?, ?, ?, ?)', projects)

    # Insert Transactions
    transactions = [
        (1, 1, 2, 1, '2024-01-15', 5000),
        (2, 2, 2, 2, '2024-01-20', 3500),
        (3, 4, 4, 3, '2024-02-01', 25000),
        (4, 5, 4, 4, '2024-02-15', 15000),
        (5, 6, 7, 5, '2024-03-01', 10000),
        (6, 7, 7, 6, '2024-03-10', 8000),
        (7, 8, 5, 7, '2024-03-15', 2000),
        (8, 9, 5, 8, '2024-04-01', 4500),
        (9, 10, 3, 9, '2024-04-10', 3000),
        (10, 11, 3, 10, '2024-04-20', 2500),
        (11, 12, 6, 11, '2024-05-01', 6000),
        (12, 14, 7, 12, '2024-05-15', 20000),
        (13, 15, 7, 13, '2024-06-01', 3000),
        (14, 16, 8, 14, '2024-06-10', 5000),
        (15, 17, 8, 15, '2024-06-20', 2800),
        (16, 1, 1, 1, '2024-07-01', 5000),
        (17, 2, 2, 2, '2024-07-15', 3500),
        (18, 18, 2, 1, '2024-08-01', 5000),
        (19, 19, 1, 2, '2024-08-10', 3500),
        (20, 20, 3, 9, '2024-09-01', 3000)
    ]
    cursor.executemany('INSERT OR IGNORE INTO Transactions VALUES (?, ?, ?, ?, ?, ?)', transactions)

    conn.commit()
    conn.close()
    print("✓ Comprehensive multi-industry database created successfully!")

if __name__ == "__main__":
    create_database()
