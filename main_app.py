import tkinter as tk
from tkinter import ttk, messagebox
import database

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Management System")
        self.root.geometry("800x600")

        # Initialize database
        self.db_conn = database.create_connection()
        if self.db_conn is None:
            # Handle database connection error
            tk.Label(self.root, text="Error: Could not connect to the database.").pack()
            return

        # Ensure tables and courses are set up
        database.create_tables(self.db_conn)
        database.populate_courses(self.db_conn)

        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for student list and search
        left_frame = ttk.Frame(main_frame, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right frame for forms and details
        right_frame = ttk.Frame(main_frame, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Widgets for the left frame ---
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=5)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        search_button = ttk.Button(search_frame, text="Search", command=self.search_student)
        search_button.pack(side=tk.RIGHT, padx=5)

        # Student list
        columns = ("id", "name", "sex")
        self.student_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        self.student_tree.heading("id", text="Student ID")
        self.student_tree.heading("name", text="Name")
        self.student_tree.heading("sex", text="Sex")
        self.student_tree.pack(fill=tk.BOTH, expand=True)

        # --- Widgets for the right frame (Add Student Form) ---
        add_student_frame = ttk.LabelFrame(right_frame, text="Add New Student")
        add_student_frame.pack(fill=tk.X, pady=10)

        # Form fields
        ttk.Label(add_student_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.id_var = tk.StringVar()
        id_entry = ttk.Entry(add_student_frame, textvariable=self.id_var)
        id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_student_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(add_student_frame, textvariable=self.name_var)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_student_frame, text="Sex:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.sex_var = tk.StringVar()
        sex_entry = ttk.Entry(add_student_frame, textvariable=self.sex_var)
        sex_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        add_button = ttk.Button(add_student_frame, text="Add Student", command=self.add_student)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_student(self):
        """Handle the 'Add Student' button click."""
        # Retrieve data from the form
        student_id_str = self.id_var.get()
        name = self.name_var.get()
        sex = self.sex_var.get()

        # --- Basic Validation ---
        if not student_id_str or not name or not sex:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            student_id = int(student_id_str)
            # Further validation for 10-digit ID can be added here
            if len(student_id_str) != 10:
                messagebox.showerror("Input Error", "Student ID must be a 10-digit number.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Student ID must be a valid number.")
            return

        # Attempt to add the student to the database
        if database.add_student(self.db_conn, student_id, name, sex):
            messagebox.showinfo("Success", f"Student '{name}' added successfully.")
            # Clear the form fields
            self.id_var.set("")
            self.name_var.set("")
            self.sex_var.set("")
            # Refresh the student list
            self.load_students()
        else:
            messagebox.showerror("Database Error", "Failed to add student. The ID may already exist.")

    def load_students(self):
        """Load all students into the Treeview."""
        # Clear existing items
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        # Fetch and insert students
        students = database.get_all_students(self.db_conn)
        for student in students:
            self.student_tree.insert("", tk.END, values=student)

    def search_student(self):
        """Search for a student by ID and update the Treeview."""
        search_id = self.search_var.get()

        # Clear existing items
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        if not search_id:
            # If search is empty, load all students
            self.load_students()
            return

        try:
            student_id = int(search_id)
            student = database.get_student_by_id(self.db_conn, student_id)
            if student:
                self.student_tree.insert("", tk.END, values=student[0])
        except ValueError:
            # Handle cases where the input is not a valid integer
            pass # Or show a message to the user

    def on_closing(self):
        """Handle the window closing event."""
        if self.db_conn:
            self.db_conn.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = StudentApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
