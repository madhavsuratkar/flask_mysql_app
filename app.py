from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection setup
def get_db_connection():
    db_config = {
        'host': 'localhost',
        'user': 'root',           # Update with your MySQL user
        'password': '',           # Update with your MySQL password
        'database': 'studenttracker'
    }
    return mysql.connector.connect(**db_config)

# Route to add a student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_num = request.form['roll_num']
        maths = request.form['maths']
        science = request.form['science']
        english = request.form['english']
        
        total = int(maths) + int(science) + int(english)
        average = total / 3
        if average >= 90:
            grade = 'A'
        elif average >= 75:
            grade = 'B'
        elif average >= 50:
            grade = 'C'
        else:
            grade = 'D'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO student (name, roll_num, maths, science, english, total, average, grades)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, roll_num, maths, science, english, total, average, grade))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_students'))
    return render_template('add_student.html')

# Route to view all students
@app.route('/view_students')
def view_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('view_students.html', students=students)

# Route to search a student by roll number
@app.route('/search_student', methods=['GET', 'POST'])
def search_student():
    student = None
    if request.method == 'POST':
        roll_num = request.form['roll_num']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE roll_num = %s", (roll_num,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()

    return render_template('search_student.html', student=student)

# Route to delete a student by roll number
@app.route('/delete_student/<int:roll_num>')
def delete_student(roll_num):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE roll_num = %s", (roll_num,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('view_students'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
