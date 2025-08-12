import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean, median, mode, stdev

RAW_FILE = "students_raw.csv"
RESULT_FILE = "students_results.csv"

# --- Step 1: Read data ---
df = pd.read_csv(RAW_FILE)

# --- Step 2: Calculate averages & grades ---
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

# --- Step 3: Save results ---
df.to_csv(RESULT_FILE, index=False)
print(f"Results saved to {RESULT_FILE}")

# --- Step 4: Statistical Summary ---
print("\nSTATISTICS")
print(df.describe())

# --- Step 5: Visualization ---
# Grade distribution
plt.figure(figsize=(6,4))
plt.hist(df['Final_Grade'], bins=10, color='skyblue', edgecolor='black')
plt.title("Final Grade Distribution")
plt.xlabel("Grade (%)")
plt.ylabel("Number of Students")
plt.savefig("grade_distribution.png")
plt.show()

# Letter grade pie chart
grade_counts = df['Letter_Grade'].value_counts()
plt.figure(figsize=(6,6))
grade_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
plt.title("Letter Grade Distribution")
plt.ylabel("")
plt.savefig("letter_grade_pie.png")
plt.show()
