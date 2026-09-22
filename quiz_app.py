import sqlite3
import pandas as pd
from datetime import datetime

class question:
    def __init__(self, question_text, choices, correct_answer):
        self.question = question_text
        self.choices = choices
        self.correct_answer = correct_answer

    def check_answer(self, user_answer):
        return user_answer.strip().lower() == self.correct_answer.strip().lower()

# Database setup
conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    choice_1 TEXT, choice_2 TEXT, choice_3 TEXT, choice_4 TEXT,
    correct_answer TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    score REAL
)
''')
conn.commit()

# Insert starter questions if the database is empty
cursor.execute("SELECT COUNT(*) FROM question")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO question (question, choice_1, choice_2, choice_3, choice_4, correct_answer) VALUES (?, ?, ?, ?, ?, ?)",
                   ("What is the capital of France?", "Paris", "London", "Berlin", "Madrid", "Paris"))
    cursor.execute("INSERT INTO question (question, choice_1, choice_2, choice_3, choice_4, correct_answer) VALUES (?, ?, ?, ?, ?, ?)",
                   ("Which language is used for this app?", "Java", "Python", "C++", "HTML", "Python"))
    conn.commit()

def play_quiz():
    cursor.execute("SELECT * FROM question")
    rows = cursor.fetchall()
    
    score = 0
    total = len(rows)
    
    print("\n🏁 STARTING THE QUIZ!")
    for row in rows:
        # Load data into your OOP class object
        q = question(row[1], [row[2], row[3], row[4], row[5]], row[6])
        
        print(f"\n📝 {q.question}")
        print(f" [A] {q.choices[0]}  [B] {q.choices[1]}  [C] {q.choices[2]}  [D] {q.choices[3]}")
        
        user_choice = input("Your Answer (Type the full word match): ").strip()
        
        if q.check_answer(user_choice):
            print("✨ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect. The right answer was: {q.correct_answer}")
            
    percentage = (score / total) * 100
    print(f"\n🎯 Quiz Finished! Your Score: {score}/{total} ({percentage}%)")
    
    # Save the score history
    date_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO quiz_attempts (date, score) VALUES (?, ?)", (date_str, percentage))
    conn.commit()

def view_history():
    df = pd.read_sql_query("SELECT * FROM quiz_attempts", conn)
    if df.empty:
        print("📭 No scores logged yet. Play a game first!")
        return
    print("\n" + "="*10 + " HISTORICAL STATISTICS " + "="*10)
    print(df)
    print("Average score across attempts:", df["score"].mean())
    print("Best score recorded:", df["score"].max())

# --- THE INTERACTIVE MENU LOOP ---
while True:
    print("\n=== INTERACTIVE QUIZ MENU ===")
    print("1. Take the Quiz")
    print("2. View History and Performance Metrics")
    print("3. Exit")
    
    choice = input("\nChoose an option (1-3): ").strip()
    
    if choice == "1":
        play_quiz()
    elif choice == "2":
        view_history()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("❌ Invalid option.")
    for row in rows:
        print(f"ID: {row[0]} - Date: {row[1]} - Category: {row[2]} - Rs.{row[3]}")

def total_spent():
    cursor.execute("SELECT SUM(amount) FROM expense")
    total = cursor.fetchone()[0]
    if total is None:
        total = 0
    print(f"\n💰 Total spent so far: Rs.{total}")

def filter_by_category(category):
    category = category.title()
    cursor.execute("SELECT * FROM expense WHERE category = ?", (category,))
    rows = cursor.fetchall()
    print(f"\n---- EXPENSES FOR {category} ----")
    for row in rows:
        print(f"ID: {row[0]} - Date: {row[1]} - Rs.{row[3]}")

def show_chart():
    df = pd.read_sql_query("SELECT * FROM expense", conn)
    if df.empty:
        print("⚠️ No data to make a chart yet!")
        return
    
    df["category"] = df["category"].str.title()
    print("\n Spending grouped by category:")
    print(df.groupby("category")["amount"].sum())
    
    # Pop up the simple bar chart
    df.groupby("category")["amount"].sum().plot(kind="bar")
    plt.title("My Spending")
    plt.tight_layout()
    plt.show()

# --- THE INTERACTIVE MENU LOOP ---
while True:
    print("\n=== EXPENSE TRACKER MENU ===")
    print("1. Add a New Expense")
    print("2. View All Expenses")
    print("3. View Total Spent")
    print("4. Filter Expenses by Category")
    print("5. Delete an Expense by ID")
    print("6. Show Analytics Chart")
    print("7. Exit")
    
    choice = input("\nChoose an option (1-7): ").strip()
    
    if choice == "1":
        cat = input("Enter category (e.g. Food, Transport): ").strip()
        amt = float(input("Enter amount (Rs.): "))
        add_expense(cat, amt)
    elif choice == "2":
        view_expense()
    elif choice == "3":
        total_spent()
    elif choice == "4":
        cat = input("Enter category to search: ").strip()
        filter_by_category(cat)
    elif choice == "5":
        exp_id = int(input("Enter the Expense ID to delete: "))
        delete_expense(exp_id)
    elif choice == "6":
        show_chart()
    elif choice == "7":
        print("Goodbye!")
        break
    else:
        print("❌ Invalid option. Please choose 1 to 7.")
conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS question (
id INTEGER PRIMARY KEY AUTOINCREMENT,
question TEXT,
choice_1 TEXT,
choice_2 TEXT,
choice_3 TEXT,
choice_4 TEXT,
correct_answer TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_attempts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT,
score REAL
)
''')

conn.commit()


# --- Functions ---

def add_question_db(question, choice_1, choice_2, choice_3, choice_4, correct_answer):
    cursor.execute(
        "INSERT INTO question (question, choice_1, choice_2, choice_3, choice_4, correct_answer) VALUES (?, ?, ?, ?, ?, ?)",
        (question, choice_1, choice_2, choice_3, choice_4, correct_answer)
    )
    conn.commit()


def delete_question(id):
    cursor.execute("DELETE FROM question WHERE id = ?", (id,))
    conn.commit()


def save_attempt(score):
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO quiz_attempts (date, score) VALUES (?, ?)", (date, score))
    conn.commit()


# --- Demonstration ---

add_question_db("What is the capital of France?", "Paris", "London", "Berlin", "Madrid", "Paris")

cursor.execute("SELECT * FROM question")
rows = cursor.fetchall()

questions_list = []
for row in rows:
    q = question(row[1], [row[2], row[3], row[4], row[5]], row[6])
    questions_list.append(q)

print(questions_list[0])
print(questions_list[0].check_answer("Paris"))

save_attempt(80)

df = pd.read_sql_query("SELECT * FROM quiz_attempts", conn)
print(df)
print("Average score:", df["score"].mean())
print("Best score:", df["score"].max())
