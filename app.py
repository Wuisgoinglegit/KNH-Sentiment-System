from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash # Required for secure passwords

# custom scripts
from sentiment_engine import SentimentEngine
from department_detection import detect_department 

app = Flask(__name__)
engine = SentimentEngine()

# Database Setup
DB_NAME = "knh_feedback.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Patient feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_text TEXT NOT NULL,
            sentiment_label VARCHAR(10),
            dept_category VARCHAR(100),
            timestamp DATETIME
        )
    ''')
    
    # Admin users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# URL Routes 

# 1. Patient Portal Home
@app.route('/')
def home():
    return render_template('patient feedback.html')

# 2. Patient Feedback Submission
@app.route('/submit', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        patient_text = request.form.get('feedback_text')
        department_selections = request.form.getlist('department_selection')

        if not department_selections or "General" in department_selections:
            department_result = detect_department(patient_text)
        else:
            department_result = ", ".join(department_selections)

        sentiment_result = engine.predict(patient_text)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patient_feedback (raw_text, sentiment_label, dept_category, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (patient_text, sentiment_result, department_result, current_time))
        conn.commit()
        conn.close()

        return render_template('patient feedback.html', success=True, dept_name=department_result)

# 3. Staff Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        staff_id = request.form.get('staffId')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match!")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Check if Staff ID is already taken
        cursor.execute('SELECT * FROM admin_users WHERE staff_id = ?', (staff_id,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error="This Staff ID already exists!")

        # Encrypt the password and save to the database
        hashed_pw = generate_password_hash(password)
        cursor.execute('INSERT INTO admin_users (staff_id, password_hash) VALUES (?, ?)', (staff_id, hashed_pw))
        conn.commit()
        conn.close()

        # Send them to the login page with a success message
        return render_template('login.html', success_msg="Account created successfully! Please log in.")

    return render_template('register.html')

# 4. Staff Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        staff_id = request.form.get('staffId')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM admin_users WHERE staff_id = ?', (staff_id,))
        user_record = cursor.fetchone()
        conn.close()

        # Verify the user exists AND the password matches the hash
        if user_record and check_password_hash(user_record[0], password):
            # Temporary success screen until we build the dashboard
            return f"""
            <div style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h2 style="color: #00102E;">Login Successful!</h2>
                <p>Welcome, Staff ID: <strong>{staff_id}</strong>.</p>
                <p style="color: #666;">(The Admin Dashboard will go here once we build it.)</p>
                <br>
                <a href="/login" style="color: #87CEEC; text-decoration: none; font-weight: bold;">Log Out</a>
            </div>
            """
        else:
            return render_template('login.html', error_msg="Invalid Staff ID or Password.")

    return render_template('login.html')

if __name__ == '__main__':
    # host='0.0.0.0' allows mobile network testing
    app.run(host='0.0.0.0', port=5000, debug=True)