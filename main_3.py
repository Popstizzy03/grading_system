import pandas as pd
import matplotlib.pyplot as plt
import os
import re

RAW_FILE = "students_raw.csv"
RESULT_FILE = "students_results.csv"

# ---------- STEP 1: Ensure starter CSV exists ----------
if not os.path.exists(RAW_FILE):
    with open(RAW_FILE, "w") as f:
        f.write("Name,ID,Assignment1,Lab1,Test1,Exam\n")

# ---------- STEP 2: Load existing CSV ----------
df_existing = pd.read_csv(RAW_FILE)

# Detect current columns
assignment_cols = [col for col in df_existing.columns if col.startswith("Assignment")]
lab_cols = [col for col in df_existing.columns if col.startswith("Lab")]
test_cols = [col for col in df_existing.columns if col.startswith("Test")]

# If none found, start with 1 each
if not assignment_cols:
    assignment_cols = ["Assignment1"]
if not lab_cols:
    lab_cols = ["Lab1"]
if not test_cols:
    test_cols = ["Test1"]

# ---------- STEP 3: New student input ----------
print("\n--- STUDENT INFORMATION ENTRY ---")
name = input("Enter the full name of the student: ")
student_id = input("Enter the student's ID: ")

# Ask how many to record for each category
num_assignments = int(input(f"How many assignments? (current max {len(assignment_cols)}): ") or len(assignment_cols))
num_labs = int(input(f"How many labs? (current max {len(lab_cols)}): ") or len(lab_cols))
num_tests = int(input(f"How many tests? (current max {len(test_cols)}): ") or len(test_cols))

# Expand column lists if user enters more than existing
while len(assignment_cols) < num_assignments:
    assignment_cols.append(f"Assignment{len(assignment_cols)+1}")
while len(lab_cols) < num_labs:
    lab_cols.append(f"Lab{len(lab_cols)+1}")
while len(test_cols) < num_tests:
    test_cols.append(f"Test{len(test_cols)+1}")

# Ensure DataFrame has these columns
for col in assignment_cols + lab_cols + test_cols + ["Exam"]:
    if col not in df_existing.columns:
        df_existing[col] = None

# Gather marks
assignments = [float(input(f"  {col} (out of 10): ")) for col in assignment_cols]
labs = [float(input(f"  {col} (out of 10): ")) for col in lab_cols]
tests = [float(input(f"  {col} (out of 100): ")) for col in test_cols]
exam = float(input("  Final Exam (out of 100): "))

# Add new student row
new_row = [name, student_id] + assignments + labs + tests + [exam]
# Align new_row with df_existing column order
row_dict = dict(zip(["Name", "ID"] + assignment_cols + lab_cols + test_cols + ["Exam"], new_row))
df_existing = pd.concat([df_existing, pd.DataFrame([row_dict])], ignore_index=True)

# Save updated raw CSV
df_existing.to_csv(RAW_FILE, index=False)
print("\nStudent data saved!")

# ---------- STEP 4: Processing ----------
df = df_existing.copy()

df['Avg_Assignments'] = df[assignment_cols].mean(axis=1)
df['Avg_Labs'] = df[lab_cols].mean(axis=1)
df['Avg_Tests'] = df[test_cols].mean(axis=1)

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

# ---------- STEP 7: Visualization (non-blocking) ----------
# Histogram of Final Grades
plt.figure(figsize=(6,4))
plt.hist(df['Final_Grade'], bins=10, color='skyblue', edgecolor='black')
plt.title("Final Grade Distribution")
plt.xlabel("Grade (%)")
plt.ylabel("Number of Students")
plt.savefig("grade_distribution.png")
plt.close()

# Pie chart of Letter Grades
grade_counts = df['Letter_Grade'].value_counts()
plt.figure(figsize=(6,6))
grade_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
plt.title("Letter Grade Distribution")
plt.ylabel("")
plt.savefig("letter_grade_pie.png")
plt.close()

print("\nCharts saved as 'grade_distribution.png' and 'letter_grade_pie.png'")

