import sqlite3

def create_database():
    """Create database with top companies from Best Companies lists"""
    conn = sqlite3.connect('business.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Companies (
        CompanyID INTEGER PRIMARY KEY, CompanyName TEXT NOT NULL, Industry TEXT NOT NULL, Location TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Departments (
        DepartmentID INTEGER PRIMARY KEY, DepartmentName TEXT NOT NULL, CompanyID INTEGER,
        FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employees (
        EmployeeID INTEGER PRIMARY KEY, Name TEXT NOT NULL, Occupation TEXT NOT NULL,
        DepartmentID INTEGER, Salary REAL, HireDate TEXT,
        FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY, CustomerName TEXT NOT NULL, Industry TEXT, ContactEmail TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
        ProductID INTEGER PRIMARY KEY, ProductName TEXT NOT NULL, Category TEXT NOT NULL,
        Price REAL, CompanyID INTEGER, FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Projects (
        ProjectID INTEGER PRIMARY KEY, ProjectName TEXT NOT NULL, CompanyID INTEGER,
        Budget REAL, StartDate TEXT, EndDate TEXT, Status TEXT,
        FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY, EmployeeID INTEGER, CustomerID INTEGER,
        ProductID INTEGER, TransactionDate TEXT, Amount REAL,
        FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID))''')

    # Top Companies - Best Companies to Own 2026
    companies = [
        # Technology Giants
        (1, 'Apple Inc', 'Technology', 'Cupertino, CA'),
        (2, 'Microsoft Corporation', 'Technology', 'Redmond, WA'),
        (3, 'NVIDIA Corporation', 'Technology', 'Santa Clara, CA'),
        (4, 'Alphabet Inc (Google)', 'Technology', 'Mountain View, CA'),
        (5, 'Meta Platforms', 'Technology', 'Menlo Park, CA'),
        (6, 'Amazon.com Inc', 'E-commerce/Technology', 'Seattle, WA'),
        (7, 'Netflix Inc', 'Technology/Entertainment', 'Los Gatos, CA'),
        (8, 'Adobe Inc', 'Software', 'San Jose, CA'),
        (9, 'Salesforce Inc', 'Cloud Software', 'San Francisco, CA'),
        (10, 'Oracle Corporation', 'Software/Cloud', 'Austin, TX'),
        
        # Financial Services
        (11, 'JPMorgan Chase', 'Banking', 'New York, NY'),
        (12, 'Bank of America', 'Banking', 'Charlotte, NC'),
        (13, 'Visa Inc', 'Financial Services', 'San Francisco, CA'),
        (14, 'Mastercard Inc', 'Financial Services', 'Purchase, NY'),
        (15, 'Goldman Sachs', 'Investment Banking', 'New York, NY'),
        (16, 'Morgan Stanley', 'Investment Banking', 'New York, NY'),
        (17, 'American Express', 'Financial Services', 'New York, NY'),
        (18, 'PayPal Holdings', 'Fintech', 'San Jose, CA'),
        (19, 'Berkshire Hathaway', 'Conglomerate', 'Omaha, NE'),
        (20, 'Charles Schwab', 'Financial Services', 'Westlake, TX'),
        
        # Healthcare
        (21, 'UnitedHealth Group', 'Healthcare', 'Minnetonka, MN'),
        (22, 'Johnson & Johnson', 'Pharmaceuticals', 'New Brunswick, NJ'),
        (23, 'Pfizer Inc', 'Pharmaceuticals', 'New York, NY'),
        (24, 'AbbVie Inc', 'Pharmaceuticals', 'North Chicago, IL'),
        (25, 'Moderna Inc', 'Biotechnology', 'Cambridge, MA'),
        (26, 'CVS Health', 'Healthcare', 'Woonsocket, RI'),
        
        # Retail
        (27, 'Walmart Inc', 'Retail', 'Bentonville, AR'),
        (28, 'Costco Wholesale', 'Retail', 'Issaquah, WA'),
        (29, 'Target Corporation', 'Retail', 'Minneapolis, MN'),
        (30, 'Home Depot', 'Retail', 'Atlanta, GA'),
        (31, 'Lowes Companies', 'Retail', 'Mooresville, NC'),
        
        # Consumer Brands
        (32, 'Procter & Gamble', 'Consumer Goods', 'Cincinnati, OH'),
        (33, 'Coca-Cola Company', 'Beverages', 'Atlanta, GA'),
        (34, 'PepsiCo Inc', 'Food & Beverage', 'Purchase, NY'),
        (35, 'Nike Inc', 'Apparel', 'Beaverton, OR'),
        (36, 'Starbucks Corporation', 'Restaurants', 'Seattle, WA'),
        (37, 'McDonald Corporation', 'Restaurants', 'Chicago, IL'),
        
        # Automotive & Energy
        (38, 'Tesla Inc', 'Automotive/Energy', 'Austin, TX'),
        (39, 'Ford Motor Company', 'Automotive', 'Dearborn, MI'),
        (40, 'General Motors', 'Automotive', 'Detroit, MI'),
        (41, 'ExxonMobil', 'Energy', 'Irving, TX'),
        (42, 'Chevron Corporation', 'Energy', 'San Ramon, CA'),
        
        # Telecom & Media
        (43, 'Verizon Communications', 'Telecommunications', 'New York, NY'),
        (44, 'AT&T Inc', 'Telecommunications', 'Dallas, TX'),
        (45, 'Comcast Corporation', 'Media/Telecom', 'Philadelphia, PA'),
        (46, 'Walt Disney Company', 'Entertainment', 'Burbank, CA'),
        
        # Industrial & Aerospace
        (47, 'Boeing Company', 'Aerospace', 'Arlington, VA'),
        (48, 'Lockheed Martin', 'Aerospace/Defense', 'Bethesda, MD'),
        (49, 'Caterpillar Inc', 'Industrial', 'Deerfield, IL'),
        (50, 'Deere & Company', 'Agricultural Equipment', 'Moline, IL')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Companies VALUES (?, ?, ?, ?)', companies)

    # Sample Departments
    departments = [
        (1, 'Engineering', 1), (2, 'Product', 1), (3, 'Retail', 1),
        (4, 'Cloud Services', 2), (5, 'Azure', 2), (6, 'Sales', 2),
        (7, 'AI Research', 3), (8, 'GPU Engineering', 3),
        (9, 'Search', 4), (10, 'YouTube', 4), (11, 'Cloud', 4),
        (12, 'Reality Labs', 5), (13, 'Instagram', 5),
        (14, 'AWS', 6), (15, 'Prime', 6), (16, 'Logistics', 6),
        (17, 'Content', 7), (18, 'Streaming Tech', 7),
        (19, 'Creative Cloud', 8), (20, 'Marketing', 8),
        (21, 'CRM Platform', 9), (22, 'Sales Operations', 9),
        (23, 'Investment Banking', 11), (24, 'Trading', 11),
        (25, 'Network Infrastructure', 13), (26, 'Fraud Prevention', 13),
        (27, 'Drug Development', 22), (28, 'Clinical Trials', 22),
        (29, 'Store Operations', 27), (30, 'Supply Chain', 27)
    ]
    cursor.executemany('INSERT OR IGNORE INTO Departments VALUES (?, ?, ?)', departments)

    # Sample Employees (CEOs and key personnel)
    employees = [
        (1, 'Tim Cook', 'CEO', 1, 3000000, '2011-08-24'),
        (2, 'Jeff Williams', 'COO', 1, 1500000, '1998-01-01'),
        (3, 'Satya Nadella', 'CEO', 4, 2500000, '2014-02-04'),
        (4, 'Amy Hood', 'CFO', 4, 1200000, '2013-05-01'),
        (5, 'Jensen Huang', 'CEO', 7, 2600000, '1993-04-05'),
        (6, 'Sundar Pichai', 'CEO', 9, 2800000, '2004-04-01'),
        (7, 'Mark Zuckerberg', 'CEO', 12, 1, '2004-02-01'),
        (8, 'Andy Jassy', 'CEO', 14, 2100000, '1997-01-01'),
        (9, 'Reed Hastings', 'Co-CEO', 17, 1800000, '1997-08-29'),
        (10, 'Shantanu Narayen', 'CEO', 19, 1700000, '2007-12-01'),
        (11, 'Marc Benioff', 'CEO', 21, 1900000, '1999-03-01'),
        (12, 'Jamie Dimon', 'CEO', 23, 3500000, '2005-12-31'),
        (13, 'Brian Moynihan', 'CEO', 24, 2700000, '2010-01-01'),
        (14, 'Warren Buffett', 'CEO', 19, 100000, '1970-05-10'),
        (15, 'Andrew Witty', 'CEO', 21, 2400000, '2021-02-01'),
        (16, 'Albert Bourla', 'CEO', 23, 2200000, '2019-01-01'),
        (17, 'Doug McMillon', 'CEO', 29, 2200000, '2014-02-01'),
        (18, 'Ron Vachris', 'CEO', 28, 1500000, '2024-01-01'),
        (19, 'Elon Musk', 'CEO', 38, 5000000, '2008-10-01'),
        (20, 'Mary Barra', 'CEO', 40, 2800000, '2014-01-15'),
        (21, 'Hans Vestberg', 'CEO', 43, 1900000, '2018-08-01'),
        (22, 'David Solomon', 'CEO', 15, 3100000, '2018-10-01'),
        (23, 'Howard Schultz', 'Chairman', 36, 1200000, '1987-06-01'),
        (24, 'Bob Iger', 'CEO', 46, 2700000, '2005-10-01'),
        (25, 'David Calhoun', 'CEO', 47, 2600000, '2020-01-13')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Employees VALUES (?, ?, ?, ?, ?, ?)', employees)

    # Sample Customers
    customers = [
        (1, 'Fortune 500 Enterprise', 'Technology', 'enterprise@fortune.com'),
        (2, 'Global Retail Chain', 'Retail', 'procurement@retail.com'),
        (3, 'Healthcare Networks Inc', 'Healthcare', 'it@healthcare.com'),
        (4, 'Financial Group LLC', 'Finance', 'ops@fingroup.com'),
        (5, 'Manufacturing Corp', 'Manufacturing', 'supply@mfg.com')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Customers VALUES (?, ?, ?, ?)', customers)

    # Sample Products
    products = [
        (1, 'iPhone 15 Pro', 'Consumer Electronics', 1199, 1),
        (2, 'MacBook Pro M3', 'Computing', 2499, 1),
        (3, 'Microsoft 365 Enterprise', 'Software', 22, 2),
        (4, 'Azure AI Services', 'Cloud/AI', 10000, 2),
        (5, 'NVIDIA H100 GPU', 'Hardware', 30000, 3),
        (6, 'Google Cloud Platform', 'Cloud Services', 8000, 4),
        (7, 'AWS Enterprise Suite', 'Cloud Services', 15000, 6),
        (8, 'Salesforce Platform', 'CRM Software', 5000, 9)
    ]
    cursor.executemany('INSERT OR IGNORE INTO Products VALUES (?, ?, ?, ?, ?)', products)

    # Sample Projects
    projects = [
        (1, 'Vision Pro Expansion', 1, 10000000, '2024-01-01', '2025-12-31', 'In Progress'),
        (2, 'AI Copilot Integration', 2, 25000000, '2023-11-01', '2025-06-30', 'In Progress'),
        (3, 'AI Chip Development', 3, 50000000, '2023-01-01', '2025-12-31', 'In Progress'),
        (4, 'Gemini Ultra Launch', 4, 30000000, '2023-12-01', '2024-12-31', 'In Progress'),
        (5, 'EV Battery Innovation', 38, 3000000000, '2023-01-01', '2026-12-31', 'In Progress')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Projects VALUES (?, ?, ?, ?, ?, ?, ?)', projects)

    # Sample Transactions
    transactions = [
        (1, 2, 1, 1, '2024-01-15', 1199000),
        (2, 4, 1, 3, '2024-02-01', 220000),
        (3, 5, 1, 5, '2024-03-01', 300000),
        (4, 6, 2, 6, '2024-04-01', 800000),
        (5, 8, 1, 7, '2024-05-01', 1500000)
    ]
    cursor.executemany('INSERT OR IGNORE INTO Transactions VALUES (?, ?, ?, ?, ?, ?)', transactions)

    conn.commit()
    conn.close()
    print("✓ Database with 50 top companies created!")

if __name__ == "__main__":
    create_database()
