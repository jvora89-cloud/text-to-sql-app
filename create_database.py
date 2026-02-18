import sqlite3

def create_database():
    """Create and populate the student grades database"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            score INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')

    # Sample student data
    students_data = [
        ('Alice Johnson', 'Mathematics', 95, 'A'),
        ('Alice Johnson', 'Physics', 88, 'B'),
        ('Alice Johnson', 'Chemistry', 92, 'A'),
        ('Bob Smith', 'Mathematics', 78, 'C'),
        ('Bob Smith', 'Physics', 85, 'B'),
        ('Bob Smith', 'Chemistry', 80, 'B'),
        ('Carol White', 'Mathematics', 92, 'A'),
        ('Carol White', 'Physics', 95, 'A'),
        ('Carol White', 'Chemistry', 89, 'B'),
        ('David Brown', 'Mathematics', 65, 'D'),
        ('David Brown', 'Physics', 70, 'C'),
        ('David Brown', 'Chemistry', 68, 'D'),
        ('Emma Davis', 'Mathematics', 88, 'B'),
        ('Emma Davis', 'Physics', 91, 'A'),
        ('Emma Davis', 'Chemistry', 87, 'B'),
    ]

    # Insert data
    cursor.executemany('''
        INSERT INTO students (name, subject, score, grade)
        VALUES (?, ?, ?, ?)
    ''', students_data)

    conn.commit()
    conn.close()
    print("✓ Database created successfully with sample student data!")

if __name__ == "__main__":
    create_database()
