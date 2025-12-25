import unittest
import sqlite3
import database  # The module we're testing

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Set up a temporary in-memory database for each test."""
        self.conn = sqlite3.connect(":memory:")
        database.create_tables(self.conn)
        database.populate_courses(self.conn)

    def tearDown(self):
        """Close the database connection after each test."""
        self.conn.close()

    def test_add_and_get_student(self):
        """Test adding a student and then retrieving them by ID."""
        student_id = 2024000001
        name = "John Doe"
        sex = "Male"

        # Add a student
        database.add_student(self.conn, student_id, name, sex)

        # Retrieve the student
        student = database.get_student_by_id(self.conn, student_id)

        # Assertions
        self.assertIsNotNone(student, "Student should be found.")
        self.assertEqual(len(student), 1, "Should find exactly one student.")
        self.assertEqual(student[0][0], student_id, "Student ID should match.")
        self.assertEqual(student[0][1], name, "Student name should match.")
        self.assertEqual(student[0][2], sex, "Student sex should match.")

    def test_get_all_students(self):
        """Test retrieving all students from the database."""
        # Add multiple students
        database.add_student(self.conn, 2024000001, "John Doe", "Male")
        database.add_student(self.conn, 2024000002, "Jane Smith", "Female")

        # Retrieve all students
        students = database.get_all_students(self.conn)

        # Assertions
        self.assertIsNotNone(students, "Should return a list of students, not None.")
        self.assertEqual(len(students), 2, "Should be 2 students in the database.")

    def test_get_nonexistent_student(self):
        """Test that querying for a nonexistent student returns an empty list."""
        student = database.get_student_by_id(self.conn, 9999999999)
        self.assertEqual(len(student), 0, "Should not find any student with a nonexistent ID.")

    def test_add_and_get_grade(self):
        """Test adding a grade and then retrieving it."""
        # Setup: Add a student and get a course ID
        student_id = 2024000001
        database.add_student(self.conn, student_id, "Test Student", "Other")
        course_id = 1  # Assuming MAT2110 is the first course
        assessment = "Quiz"
        score = 85.5

        # Add a grade
        database.add_grade(self.conn, student_id, course_id, assessment, score)

        # Retrieve the grades
        grades = database.get_grades_for_student_course(self.conn, student_id, course_id)

        # Assertions
        self.assertIsNotNone(grades)
        self.assertEqual(len(grades), 1)
        self.assertEqual(grades[0][0], assessment)
        self.assertEqual(grades[0][1], score)


if __name__ == '__main__':
    unittest.main()
