import pandas as pd
import matplotlib.pyplot as plt
import os

RAW_FILE = "students_raw.csv"
RESULT_FILE = "students_results.csv"

# ---------- STEP 1: Ensure starter CSV exists ----------
if not os.path.exists(RAW_FILE):
    with open(RAW_FILE, "w") as f:
        f.write("Name,ID,Assignment1,Assignment2,Lab1,Lab2,Test1,Test2,Exam\n")

# ---------- STEP 2: Append new student ----------
print("\n--- STUDENT INFORMATION ENTRY ---")
name = input("Enter the full name of the student: ")
student_id = input("Enter the student's ID: ")

num_assignments = 2  # fixed for now, can expand later
assignments = [float(input(f"  Assignment {i+1} (out of 10): ")) for i in range(num_assignments)]

num_labs = 2
labs = [float(input(f"  Lab {i+1} (out of 10): ")) for i in range(num_labs)]

num_tests = 2
tests = [float(input(f"  Test {i+1} (out of 100): ")) for i in range(num_tests)]

exam = float(input("  Final Exam (out of 100): "))

# Append to CSV
with open(RAW_FILE, "a") as f:
    row = [name, student_id] + assignments + labs + tests + [exam]
    f.write(",".join(map(str, row)) + "\n")

print("\nStudent data saved!")

# ---------- STEP 3: Read full CSV ----------
df = pd.read_csv(RAW_FILE)

# ---------- STEP 4: Processing ----------
df['Avg_Assignments'] = df[[col for col in df.columns if 'Assignment' in col]].mean(axis=1)
df['Avg_Labs'] = df[[col for col in df.columns if 'Lab' in col]].mean(axis=1)
df['Avg_Tests'] = df[[col for col in df.columns if 'Test' in col]].mean(axis=1)

df['Final_Grade'] = (
    (df['Avg_Assignments'] * 10) * 0.15 +
    (df['Avg_Labs'] * 10) * 0.15 +
    (df['Avg_Tests']) * 0.30 +
    (df['Exam']) * 0.40
)

def letter_grade(score):
    if score >= 80: return 'A'
    elif score >= 70: return 'B'
    elif score >= 60: return 'C'
    elif score >= 50: return 'D'
    return 'F'

df['Letter_Grade'] = df['Final_Grade'].apply(letter_grade)

# ---------- STEP 5: Save results ----------
df.to_csv(RESULT_FILE, index=False)
print(f"Results saved to {RESULT_FILE}")

# ---------- STEP 6: Statistics ----------
print("\n--- CLASS STATISTICS ---")
print(df.describe())

# ---------- STEP 7: Visualization ----------
# Histogram of Final Grades
plt.figure(figsize=(6,4))
plt.hist(df['Final_Grade'], bins=10, color='skyblue', edgecolor='black')
plt.title("Final Grade Distribution")
plt.xlabel("Grade (%)")
plt.ylabel("Number of Students")
plt.savefig("grade_distribution.png")
plt.show()

# Pie chart of Letter Grades
grade_counts = df['Letter_Grade'].value_counts()
plt.figure(figsize=(6,6))
grade_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
plt.title("Letter Grade Distribution")
plt.ylabel("")
plt.savefig("letter_grade_pie.png")
plt.show()

