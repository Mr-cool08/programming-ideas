from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'the random string'
conn = sqlite3.connect('idea.db', check_same_thread=False)
def create_datase():
    conn.execute('''CREATE TABLE IF NOT EXISTS ideas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT
    );''')
    conn.commit()

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
    cursor.execute('SELECT title, description FROM ideas')
    ideas = cursor.fetchall()
    # Generate a color for each idea
    colors = [generate_soft_dark_color() for _ in ideas]
    return render_template('get_idea.html', ideas=zip(ideas, colors))

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        if "already" in session:
            return render_template('error.html', message="You have already written an idea")
        else:
            name = request.form['name']
            content = request.form['content']
            conn.execute('''INSERT INTO ideas(title, description) VALUES(?, ?)''', (name, content))
            conn.commit()
            session["already"] = True
            return render_template('write.html')
    elif request.method == 'GET':
        
        return render_template('write.html')
if __name__ == '__main__':
    create_datase()
    app.run(debug=True)