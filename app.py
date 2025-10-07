# Update app.py with students route

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'student_portal_secret_key_2025'

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_name TEXT NOT NULL,
                  last_name TEXT NOT NULL,
                  email TEXT NOT NULL UNIQUE,
                  phone TEXT NOT NULL,
                  course TEXT NOT NULL,
                  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        
        try:
            conn = sqlite3.connect('students.db')
            c = conn.cursor()
            c.execute("INSERT INTO students (first_name, last_name, email, phone, course) VALUES (?, ?, ?, ?, ?)",
                     (first_name, last_name, email, phone, course))
            conn.commit()
            conn.close()
            flash('Registration successful!', 'success')
            return redirect(url_for('confirmation', 
                                   first_name=first_name, 
                                   last_name=last_name,
                                   email=email,
                                   course=course))
        except sqlite3.IntegrityError:
            flash('Email already registered!', 'error')
    
    return render_template('register.html')

@app.route('/confirmation')
def confirmation():
    first_name = request.args.get('first_name', '')
    last_name = request.args.get('last_name', '')
    email = request.args.get('email', '')
    course = request.args.get('course', '')
    
    return render_template('confirmation.html', 
                          first_name=first_name,
                          last_name=last_name,
                          email=email,
                          course=course)

@app.route('/students')
def students():
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students ORDER BY registration_date DESC")
        students = c.fetchall()
        conn.close()
        
        return render_template('students.html', students=students)
    except Exception as e:
        flash(f'Error loading students: {str(e)}', 'error')
        return render_template('students.html', students=[])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

