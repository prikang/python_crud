import sqlite3
class Employee:
    def __init__(self, id, name, phone_no, email, position):
        self.id = id
        self.name = name
        self.phone_no = phone_no
        self.email = email
        self.position = position

    def add(self):
        pass

    def remove(self):
        pass

    def update(self):
        pass

    def view(self):
        pass

class Student:
    def __init__(self, id, name, age, address, contact, section):
        self.id = id
        self.name = name
        self.age = age
        self.address = address
        self.contact = contact
        self.section = section

class Teacher(Employee):
    def __init__(self, id, name, phone_no, email, position, subject):
        super().__init__(id, name, phone_no, email, position)
        self.subject = subject

    def mark_attendance(self):
        pass

    def key_in_assessment_marks(self):
        pass

    def key_in_term_report(self):
        pass

    def update_own_profile(self):
        pass

class Admin:
    # Creating datbase
    connection_ = sqlite3.connect("kms.db")
    cur = connection_.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_no INTEGER,
                email TEXT NOT NULL,
                position TEXT NOT NULL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                address TEXT,
                contact INTEGER,
                section TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_no INTEGER,
                email TEXT NOT NULL,
                position TEXT NOT NULL,
                subject TEXT NOT NULL)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                date TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                marks INTEGER,
                term_report TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id))''')
        
    connection_.commit()
    students = []

    # add employee
    def add_employee(self):
        name = input("Enter employee name: ")
        phone_no = input("Enter employee phone number: ")
        email = input("Enter employee email: ")
        position = input("Enter employee position: ")
        self.cur.execute("INSERT INTO employees (name, phone_no, email, position) VALUES (?, ?, ?, ?)", (name, phone_no, email, position))
        self.connection_.commit()
        print(f"Employee {name} added successfully.")

    # remove employee
    def remove_employee(self):
        id_to_remove = input("Enter the id of employee to remove: ")
        result = self.cur.execute('SELECT id FROM employees WHERE id=?', (id_to_remove,)).fetchone()
        if result:
            self.cur.execute('DELETE FROM employees WHERE id = ?', (id_to_remove,))
            self.connection_.commit()
            print(f"Employee {id_to_remove} successfully deleted")
        else:
            print(f"Employee {id_to_remove} not found")
    # update employee
    def update_employee_profile(self):
        id_to_update = input("Enter the id of the employee to update: ")

        # Check if the employee ID exists
        result = self.cur.execute('SELECT id FROM employees WHERE id=?', (id_to_update,)).fetchone()
        if result:
            new_position = input("Enter the new position: ")
            self.cur.execute('UPDATE employees SET position = ? WHERE id = ?', (new_position, id_to_update))
            self.connection_.commit()
            print(f"Employee {id_to_update} profile is updated successfully.")
        else:
            print(f"Employee {id_to_update} not found.")

    # view employee details 
    def view_employee_details(self):
        self.cur.execute('SELECT * FROM employees')
        results = self.cur.fetchall()
        for result in results:
            print(f"ID: {result[0]}, Name: {result[1]}, Phone number: {result[2]}, Email: {result[3]}, Position: {result[4]}")
    # earch employee by name
    def search_employee_by_name(self):
        name_to_search = input("Enter employee name to search: ")
        self.cur.execute('SELECT * FROM employees WHERE name =?', (name_to_search,))
        results = self.cur.fetchall()
        for result in results:
            print(f"ID: {result[0]}, Name: {result[1]}, Phone number: {result[2]}, Email: {result[3]}, Position: {result[4]}")

    # upload student
    def upload_students_list(self):
        num_students = int(input("Enter the number of students: "))
        for _ in range(num_students):
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            address = input("Enter student address: ")
            contact = input("Enter student contact: ")
            section = input("Enter student section: ")

            student_data = (name, age, address, contact, section)
            self.students.append(student_data)  # add student to the list
            self.cur.execute("INSERT INTO students (name, age, address, contact, section) VALUES (?, ?, ?, ?, ?)", student_data)

        self.connection_.commit()
        print("Students list uploaded successfully.")
        print(f"Current students list: {self.students}")

    # remove student
    def remove_students_names(self):
        names = input("Enter student names to remove : ")

        self.cur.execute("DELETE FROM students WHERE name=?",(names,)).fetchone()
        self.connection_.commit()

        print("Students removed successfully.")
    
    # update student profile
    def update_students_profiles(self):
        id_to_update = input("Enter student id to update age: ")

        result = self.cur.execute('SELECT id FROM students WHERE id=?', (id_to_update,)).fetchone()
        if result:
            new_age = int(input("Enter new age: "))
            self.cur.execute("UPDATE students SET age=? WHERE id=?", (new_age, id_to_update))
            self.connection_.commit()
            print(f"Student {id_to_update} profile is updated successfully.")
        else:
            print(f"Student {id_to_update} not found.")

    # search student by name
    def search_student_by_id(self):
        student_id_to_search = input("Enter student ID to search: ")
        self.cur.execute('SELECT * FROM students WHERE id = ?', (student_id_to_search,))
        result = self.cur.fetchone()
        if result:
            print(f"ID: {result[0]}, Name: {result[1]}, Age: {result[2]}, Address: {result[3]}, Contact: {result[4]}, Section: {result[5]}")
        else:
            print(f"Student with ID {student_id_to_search} not found.")
    
    # attendance
    def mark_student_attendance(self):
        student_id = input("Enter student ID: ")
        date = input("Enter date (YYYY-MM-DD): ")
        self.cur.execute("INSERT INTO attendance (student_id, date) VALUES (?, ?)", (student_id, date))
        self.connection_.commit()
        print(f"Attendance marked for Student ID {student_id} on {date}")

    # assesment mark and term report
    def key_in_assessment_marks_and_term_report(self):
        student_id = input("Enter student ID: ")
        marks = int(input("Enter assessment marks: "))
        term_report = input("Enter term report text: ")
        self.cur.execute("INSERT INTO assessments (student_id, marks, term_report) VALUES (?, ?, ?)", (student_id, marks, term_report))
        self.connection_.commit()
        print(f"Assessment marks and term report keyed in for Student ID {student_id}")

    # add teacher
    def add_teacher(self):
        name = input("Enter teacher name: ")
        phone_no = input("Enter teacher phone number: ")
        email = input("Enter teacher email: ")
        position = input("Enter teacher position: ")
        subject = input("Enter teacher subject: ")

        self.cur.execute("INSERT INTO teachers (name, phone_no, email, position, subject) VALUES (?, ?, ?, ?, ?)",
                         (name, phone_no, email, position, subject))
        self.connection_.commit()
        print(f"Teacher {name} added successfully.")
        
    # update teacher profile
    def update_teacher_profile(self):
        id_to_update = input("Enter the id of the teacher to update: ")
        new_subject = input("Enter the new subject: ")

        self.cur.execute('UPDATE teachers SET subject = ? WHERE id = ?', (new_subject, id_to_update))
        self.connection_.commit()
        print(f"Teacher {id_to_update} profile is updated successfully.")


while True:
    print("\n1. Add Employee")
    print("2. Remove Employee")
    print("3. Update Employee Profile")
    print("4. View Employee Details")
    print("5. Upload Students List")
    print("6. Remove Students by Names")
    print("7. Update Student Profiles")
    print("8. Mark Student Attendance")
    print("9. Key-in Assessment Marks")
    print("10. Add teacher")
    print("11. Update Own Profile")
    print("12. Search employee")
    print("13. Search student")
    print("14. Exit")

    option = input("\nEnter the option (1-14): ")

    if option == '1':
        Admin().add_employee()
    elif option == '2':
        Admin().remove_employee()
    elif option == '3':
        Admin().update_employee_profile()
    elif option == '4':
        Admin().view_employee_details()
    elif option == '5':
        Admin().upload_students_list()
    elif option == '6':
        Admin().remove_students_names()
    elif option == '7':
        Admin().update_students_profiles()
    elif option == '8':
        Admin().mark_student_attendance()
    elif option == '9':
        Admin().key_in_assessment_marks_and_term_report()
    elif option == '10':
       Admin().add_teacher()
    elif option == '11':
       Admin().update_teacher_profile()
    elif option == '12':
        Admin().search_employee_by_name()
    elif option == '13':
        Admin().search_student_by_id()
    elif option == '14':
        Admin.connection_.close()
        print("Exiting program.")
        break
    else:
        print("Invalid option. Please enter a number between 1 and 14.")

