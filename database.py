import sqlite3
from sqlite3 import Error

DB_FILE = "student_grades.db"

def create_connection():
    """Create a database connection to the SQLite database specified by DB_FILE."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create tables for students, courses, and grades."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                sex TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                assessment_type TEXT NOT NULL,
                score REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (course_id) REFERENCES courses (id)
            );
        """)
        conn.commit()
    except Error as e:
        print(e)

def populate_courses(conn):
    """Populate the courses table with the predefined list of courses."""
    courses = [
        "MAT2110", "EEE2019", "CEE2219", "ENG2129",
        "ENG2139", "MEC2009", "MEC2309", "ENG2159"
    ]
    try:
        cursor = conn.cursor()
        for course in courses:
            # The IGNORE clause prevents errors if the course already exists
            cursor.execute("INSERT OR IGNORE INTO courses (name) VALUES (?)", (course,))
        conn.commit()
    except Error as e:
        print(e)

def add_student(conn, student_id, name, sex):
    """Add a new student to the students table."""
    sql = ''' INSERT INTO students(id,name,sex)
              VALUES(?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (student_id, name, sex))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def get_student_by_id(conn, student_id):
    """Query students by id."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)

def get_all_students(conn):
    """Query all students."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)

def add_grade(conn, student_id, course_id, assessment_type, score):
    """Add a new grade for a student in a specific course."""
    sql = ''' INSERT INTO grades(student_id, course_id, assessment_type, score)
              VALUES(?,?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (student_id, course_id, assessment_type, score))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None

def get_grades_for_student_course(conn, student_id, course_id):
    """Query all grades for a student in a specific course."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT assessment_type, score FROM grades WHERE student_id=? AND course_id=?", (student_id, course_id))
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)
