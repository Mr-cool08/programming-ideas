from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'the random string'

# Remove the database deletion code and modify connection handling
def get_db_connection():
    return sqlite3.connect('idea.db', check_same_thread=False)

conn = get_db_connection()

def create_datase():
    try:
        conn.execute('''DROP TABLE IF EXISTS ideas''')  # This will reset the table
        conn.execute('''CREATE TABLE IF NOT EXISTS ideas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            difficulty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database creation error: {e}")

def migrate_database():
    try:
        # Check if column exists
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(ideas)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in columns:
            # Add the new column with current timestamp as default
            conn.execute('''ALTER TABLE ideas 
                          ADD COLUMN created_at TIMESTAMP 
                          DEFAULT CURRENT_TIMESTAMP''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database migration error: {e}")

def generate_soft_dark_color():
    # Generate soft, dark colors that match the site's theme
    hue = random.randint(0, 360)
    saturation = random.randint(10, 30)
    lightness = random.randint(15, 25)
    return f"hsl({hue}, {saturation}%, {lightness}%)"

@app.route('/')
@app.route('/home')
def index():
    image_urls = ["static/home.png"]
    return render_template('index.html', image_urls=image_urls)


@app.route('/get')
def get_idea():
    cursor = conn.cursor()
    cursor.execute('SELECT title, description, created_at, difficulty FROM ideas ORDER BY created_at DESC')
    ideas = cursor.fetchall()
    # Generate a color for each idea
    colors = [generate_soft_dark_color() for _ in ideas]
    return render_template('get_idea.html', ideas=zip(ideas, colors))

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        try:
            #if "already" in session:
               #return render_template('error.html', message="You have already submitted an idea.")
            name = request.form['name']
            content = request.form['content']
            difficulty = request.form['difficulty']
            conn.execute('''INSERT INTO ideas(title, description, difficulty) VALUES(?, ?, ?)''', (name, content, difficulty))
            conn.commit()
            session["already"] = True
            return redirect(url_for('get_idea'))
        except Exception as e:
            return render_template('error.html', message="An error occurred while submitting your idea. Please try again.")
    return render_template('write.html')

if __name__ == '__main__':
    create_datase()
    migrate_database()
    app.run(debug=True)