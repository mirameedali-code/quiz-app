import sqlite3
import pandas as pd
from datetime import datetime

# --- Classes ---

class question:
    def __init__(self, question, choices, correct_answer):
        self.question = question
        self.choices = choices
        self.correct_answer = correct_answer

    def __str__(self):
        return self.question

    def check_answer(self, user_answer):
        if user_answer == self.correct_answer:
            return True
        else:
            return False


class quiz:
    def __init__(self):
        self.questions = []

    def add_question(self, new_question):
        self.questions.append(new_question)

    def display_questions(self):
        for q in self.questions:
            print(q)


# --- Database setup ---

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
