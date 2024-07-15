import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('student_grades.db')
c = conn.cursor()

# Create table
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            subject TEXT,
            grade INTEGER,
            year INTEGER
        )
    ''')
    conn.commit()

# Insert a new student record
def create_student(name, subject, grade, year):
    c.execute('''
        INSERT INTO students (name, subject, grade, year)
        VALUES (?, ?, ?, ?)
    ''', (name, subject, grade, year))
    conn.commit()

# Read all student records
def read_students():
    c.execute('SELECT * FROM students')
    return c.fetchall()

# Update a student record
def update_student(student_id, name=None, subject=None, grade=None, year=None):
    query = 'UPDATE students SET '
    updates = []
    params = []
    
    if name:
        updates.append('name = ?')
        params.append(name)
    if subject:
        updates.append('subject = ?')
        params.append(subject)
    if grade:
        updates.append('grade = ?')
        params.append(grade)
    if year:
        updates.append('year = ?')
        params.append(year)
    
    query += ', '.join(updates)
    query += ' WHERE id = ?'
    params.append(student_id)
    
    c.execute(query, params)
    conn.commit()

# Delete a student record
def delete_student(student_id):
    c.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()

# Main menu
def main_menu():
    print("Student Grades Management System")
    print("1. Create Student")
    print("2. Read Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        name = input("Enter student name: ")
        subject = input("Enter subject: ")
        grade = int(input("Enter grade: "))
        year = int(input("Enter year: "))
        create_student(name, subject, grade, year)
        print("Student created successfully!")
    elif choice == '2':
        students = read_students()
        for student in students:
            print(student)
    elif choice == '3':
        student_id = int(input("Enter student ID to update: "))
        name = input("Enter new name (leave blank to keep current): ")
        subject = input("Enter new subject (leave blank to keep current): ")
        grade = input("Enter new grade (leave blank to keep current): ")
        year = input("Enter new year (leave blank to keep current): ")
        
        name = name if name else None
        subject = subject if subject else None
        grade = int(grade) if grade else None
        year = int(year) if year else None
        
        update_student(student_id, name, subject, grade, year)
        print("Student updated successfully!")
    elif choice == '4':
        student_id = int(input("Enter student ID to delete: "))
        delete_student(student_id)
        print("Student deleted successfully!")
    elif choice == '5':
        conn.close()
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice, please try again.")
    
    main_menu()

# Initialize database and start main menu
create_table()

# Insert dummy data
dummy_data = [
    ("Alice", "Math", 85, 2023),
    ("Bob", "Science", 90, 2023),
    ("Charlie", "English", 78, 2023),
    ("David", "History", 88, 2023),
    ("Eve", "Math", 92, 2023)
]

for data in dummy_data:
    create_student(*data)

main_menu()
