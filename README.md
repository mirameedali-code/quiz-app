# Quiz App

A command-line quiz application built with Python, SQLite, and pandas — combining OOP design with persistent storage and score tracking.

## Features
- Store quiz questions (with 4 choices and a correct answer) in a database
- Check submitted answers against the correct answer
- Save quiz attempt scores with the date
- View average and best scores across all attempts

## Technologies Used
- Python (OOP)
- SQLite (via `sqlite3`)
- pandas

## How to Run
1. Open the notebook in Google Colab or any Python environment
2. Run all cells
3. The demonstration section shows adding a question, checking an answer, saving a score, and viewing stats

## 🎯 Live Quiz & Scoring Output

Here is what a standard user session looks like during an evaluation round:

```text
Question 1: What is the capital of France?
  [A] Berlin
  [B] Madrid
  [C] Paris
  [D] Rome

👉 Your Answer: C
✨ Result: Correct!

======================================
        HISTORICAL STATISTICS         
======================================
 🏆 Personal Best:  80.0%
 📈 Average Score:  80.0%
--------------------------------------
*Score successfully synchronized to SQLite database.*
======================================
```
