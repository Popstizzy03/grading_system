import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

RAW_FILE = "students_raw.csv"
RESULT_FILE = "students_results.csv"

# ---------- STARTUP ----------
if not os.path.exists(RAW_FILE):
    with open(RAW_FILE, "w") as f:
        f.write("Name,ID,Assignment1,Lab1,Test1,Exam,Date\n")

def get_valid_mark(prompt, max_mark, default=None):
    """Prompt until valid mark is entered or keep default."""
    while True:
        try:
            entry = input(prompt).strip()
            if entry == "" and default is not None:
                return default
            mark = float(entry)
            if 0 <= mark <= max_mark:
                return mark
            print(f"Error: must be between 0 and {max_mark}, you entered {mark}")
        except ValueError:
            print("Error: please enter a number or leave blank to keep existing")

def letter_grade(score):
    if score >= 80: return 'A'
    elif score >= 70: return 'B'
    elif score >= 60: return 'C'
    elif score >= 50: return 'D'
    return 'F'

def process_and_save(df):
    assignment_cols = [c for c in df.columns if c.startswith("Assignment")]
    lab_cols = [c for c in df.columns if c.startswith("Lab")]
    test_cols = [c for c in df.columns if c.startswith("Test")]

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

    df.to_csv(RESULT_FILE, index=False)
    print(f"\nResults saved to {RESULT_FILE}")

    # Stats
    print("\n--- CLASS STATISTICS ---")
    print(df.describe())

    # Leaderboard
    print("\n--- TOP 5 STUDENTS ---")
    leaderboard = df.sort_values(by="Final_Grade", ascending=False).head(5)
    for i, row in leaderboard.iterrows():
        print(f"{i+1}. {row['Name']} - {row['Final_Grade']:.2f}% ({row['Letter_Grade']})")

    # Grade distribution
    plt.figure(figsize=(6,4))
    plt.hist(df['Final_Grade'], bins=10, color='skyblue', edgecolor='black')
    plt.title("Final Grade Distribution")
    plt.xlabel("Grade (%)")
    plt.ylabel("Number of Students")
    plt.savefig("grade_distribution.png")
    plt.close()

    # Letter grade pie chart
    grade_counts = df['Letter_Grade'].value_counts()
    plt.figure(figsize=(6,6))
    grade_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
    plt.title("Letter Grade Distribution")
    plt.ylabel("")
    plt.savefig("letter_grade_pie.png")
    plt.close()

    # Line graph - grade trends by date
    if 'Date' in df.columns:
        plt.figure(figsize=(8,5))
        for name, group in df.groupby("Name"):
            group_sorted = group.sort_values(by="Date")
            plt.plot(group_sorted['Date'], group_sorted['Final_Grade'], marker='o', label=name)
        plt.title("Student Grade Trends")
        plt.xlabel("Date")
        plt.ylabel("Final Grade (%)")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("grade_trends.png")
        plt.close()

# ---------- MAIN LOOP ----------
while True:
    df_existing = pd.read_csv(RAW_FILE)

    assignment_cols = [c for c in df_existing.columns if c.startswith("Assignment")]
    lab_cols = [c for c in df_existing.columns if c.startswith("Lab")]
    test_cols = [c for c in df_existing.columns if c.startswith("Test")]

    print("\n--- STUDENT INFORMATION ENTRY ---")
    name = input("Enter student name: ")
    student_id = input("Enter student ID: ")

    mask = (df_existing["ID"] == student_id) | (df_existing["Name"].str.lower() == name.lower())
    exists = mask.any()

    if exists:
        print(f"Updating record for {name}")
        idx = df_existing.index[mask][0]
    else:
        # Make sure all expected columns exist
        for col in assignment_cols + lab_cols + test_cols + ["Exam", "Date"]:
            if col not in df_existing.columns:
                df_existing[col] = None
        idx = len(df_existing)
        df_existing.loc[idx, "Name"] = name
        df_existing.loc[idx, "ID"] = student_id

    # Assignments
    for col in assignment_cols:
        current = df_existing.at[idx, col] if exists else None
        df_existing.at[idx, col] = get_valid_mark(f"{col} (out of 10): ", 10, current)

    # Labs
    for col in lab_cols:
        current = df_existing.at[idx, col] if exists else None
        df_existing.at[idx, col] = get_valid_mark(f"{col} (out of 10): ", 10, current)

    # Tests
    for col in test_cols:
        current = df_existing.at[idx, col] if exists else None
        df_existing.at[idx, col] = get_valid_mark(f"{col} (out of 100): ", 100, current)

    # Exam
    current_exam = df_existing.at[idx, "Exam"] if exists else None
    df_existing.at[idx, "Exam"] = get_valid_mark("Final Exam (out of 100): ", 100, current_exam)

    # Date stamp
    df_existing.at[idx, "Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save
    df_existing.to_csv(RAW_FILE, index=False)
    print("Student data saved!\n")

    cont = input("Enter another student? (y/n): ").strip().lower()
    if cont != 'y':
        process_and_save(df_existing)
        print("\nCharts saved as 'grade_distribution.png', 'letter_grade_pie.png', 'grade_trends.png'")
        break

