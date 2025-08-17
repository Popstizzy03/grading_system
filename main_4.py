import pandas as pd
import matplotlib.pyplot as plt
import os

RAW_FILE = "students_raw.csv"
RESULT_FILE = "students_results.csv"

# ---------- STEP 1: Ensure starter CSV exists ----------
if not os.path.exists(RAW_FILE):
    with open(RAW_FILE, "w") as f:
        f.write("Name,ID,Assignment1,Lab1,Test1,Exam\n")

# ---------- HELPER FUNCTIONS ----------
def get_valid_mark(prompt, max_mark):
    """Prompt until a valid mark <= max_mark is entered."""
    while True:
        try:
            mark = float(input(prompt))
            if 0 <= mark <= max_mark:
                return mark
            else:
                print(f"Error: mark must be between 0 and {max_mark}. You entered {mark}. Try again.")
        except ValueError:
            print("Error: please enter a number.")

def letter_grade(score):
    if score >= 80: return 'A'
    elif score >= 70: return 'B'
    elif score >= 60: return 'C'
    elif score >= 50: return 'D'
    return 'F'

def process_and_save(df):
    """Processes grades, saves results, and exports graphs."""
    assignment_cols = [col for col in df.columns if col.startswith("Assignment")]
    lab_cols = [col for col in df.columns if col.startswith("Lab")]
    test_cols = [col for col in df.columns if col.startswith("Test")]

    df['Avg_Assignments'] = df[assignment_cols].mean(axis=1)
    df['Avg_Labs'] = df[lab_cols].mean(axis=1)
    df['Avg_Tests'] = df[test_cols].mean(axis=1)

    df['Final_Grade'] = (
        (df['Avg_Assignments'] * 10) * 0.15 +
        (df['Avg_Labs'] * 10) * 0.15 +
        (df['Avg_Tests']) * 0.30 +
        (df['Exam']) * 0.40
    )

    df['Letter_Grade'] = df['Final_Grade'].apply(letter_grade)

    # Save results CSV
    df.to_csv(RESULT_FILE, index=False)
    print(f"\nResults saved to {RESULT_FILE}")

    # Stats
    print("\n--- CLASS STATISTICS ---")
    print(df.describe())

    # Graphs
    plt.figure(figsize=(6,4))
    plt.hist(df['Final_Grade'], bins=10, color='skyblue', edgecolor='black')
    plt.title("Final Grade Distribution")
    plt.xlabel("Grade (%)")
    plt.ylabel("Number of Students")
    plt.savefig("grade_distribution.png")
    plt.close()

    grade_counts = df['Letter_Grade'].value_counts()
    plt.figure(figsize=(6,6))
    grade_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
    plt.title("Letter Grade Distribution")
    plt.ylabel("")
    plt.savefig("letter_grade_pie.png")
    plt.close()

# ---------- MAIN LOOP ----------
while True:
    df_existing = pd.read_csv(RAW_FILE)

    # Detect columns
    assignment_cols = [col for col in df_existing.columns if col.startswith("Assignment")]
    lab_cols = [col for col in df_existing.columns if col.startswith("Lab")]
    test_cols = [col for col in df_existing.columns if col.startswith("Test")]

    if not assignment_cols:
        assignment_cols = ["Assignment1"]
    if not lab_cols:
        lab_cols = ["Lab1"]
    if not test_cols:
        test_cols = ["Test1"]

    print("\n--- STUDENT INFORMATION ENTRY ---")
    name = input("Enter the full name of the student: ")
    student_id = input("Enter the student's ID: ")

    # Check if student exists (by ID or name)
    student_mask = (df_existing["ID"] == student_id) | (df_existing["Name"].str.lower() == name.lower())
    student_exists = df_existing[student_mask].shape[0] > 0

    # Ask how many assessments to enter
    num_assignments = int(input(f"How many assignments? (current max {len(assignment_cols)}): ") or len(assignment_cols))
    num_labs = int(input(f"How many labs? (current max {len(lab_cols)}): ") or len(lab_cols))
    num_tests = int(input(f"How many tests? (current max {len(test_cols)}): ") or len(test_cols))

    # Expand columns if needed
    while len(assignment_cols) < num_assignments:
        assignment_cols.append(f"Assignment{len(assignment_cols)+1}")
    while len(lab_cols) < num_labs:
        lab_cols.append(f"Lab{len(lab_cols)+1}")
    while len(test_cols) < num_tests:
        test_cols.append(f"Test{len(test_cols)+1}")

    # Ensure CSV has all needed columns
    for col in assignment_cols + lab_cols + test_cols + ["Exam"]:
        if col not in df_existing.columns:
            df_existing[col] = None

    # Input marks with validation
    assignments = [get_valid_mark(f"  {col} (out of 10): ", 10) for col in assignment_cols]
    labs = [get_valid_mark(f"  {col} (out of 10): ", 10) for col in lab_cols]
    tests = [get_valid_mark(f"  {col} (out of 100): ", 100) for col in test_cols]
    exam = get_valid_mark("  Final Exam (out of 100): ", 100)

    # Add or update
    if student_exists:
        print(f"Updating existing record for {name}...")
        df_existing.loc[student_mask, ["Name", "ID"] + assignment_cols + lab_cols + test_cols + ["Exam"]] = \
            [name, student_id] + assignments + labs + tests + [exam]
    else:
        new_row = dict(zip(["Name", "ID"] + assignment_cols + lab_cols + test_cols + ["Exam"],
                           [name, student_id] + assignments + labs + tests + [exam]))
        df_existing = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)

    # Save updated CSV
    df_existing.to_csv(RAW_FILE, index=False)
    print("Student data saved!\n")

    # Continue?
    cont = input("Do you want to enter another student? (y/n): ").strip().lower()
    if cont != 'y':
        # Final processing before exit
        process_and_save(df_existing)
        print("\nCharts saved as 'grade_distribution.png' and 'letter_grade_pie.png'")
        break

