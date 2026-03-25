from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# custom scripts
from sentiment_engine import SentimentEngine
from department_detection import detect_department 

app = Flask(__name__)
engine = SentimentEngine()

DB_NAME = "knh_feedback.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_text TEXT NOT NULL,
            sentiment_label VARCHAR(10),
            dept_category VARCHAR(100),
            timestamp DATETIME
        )
    ''')
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

@app.route('/')
def home():
    return render_template('patient feedback.html')

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        staff_id = request.form.get('staffId')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match!")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin_users WHERE staff_id = ?', (staff_id,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error="This Staff ID already exists!")

        hashed_pw = generate_password_hash(password)
        cursor.execute('INSERT INTO admin_users (staff_id, password_hash) VALUES (?, ?)', (staff_id, hashed_pw))
        conn.commit()
        conn.close()
        return render_template('login.html', success_msg="Account created successfully! Please log in.")
    return render_template('register.html')

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

        if user_record and check_password_hash(user_record[0], password):
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error_msg="Invalid Staff ID or Password.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patient_feedback ORDER BY timestamp DESC LIMIT 20')
    feedbacks = cursor.fetchall()
    cursor.execute('SELECT COUNT(*) FROM patient_feedback')
    total = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM patient_feedback WHERE sentiment_label = "Positive"')
    pos_count = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM patient_feedback WHERE sentiment_label = "Negative"')
    neg_count = cursor.fetchone()[0] or 0
    neu_count = total - (pos_count + neg_count)
    conn.close()
    pos_percent = round((pos_count / total * 100), 1) if total > 0 else 0

    return render_template('dashboard.html', feedbacks=feedbacks, total=total, pos_percent=pos_percent, pos_count=pos_count, neu_count=neu_count, neg_count=neg_count)     

@app.route('/api/dashboard_data')
def api_dashboard_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM patient_feedback')
    total = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM patient_feedback WHERE sentiment_label = "Positive"')
    pos_count = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM patient_feedback WHERE sentiment_label = "Negative"')
    neg_count = cursor.fetchone()[0] or 0
    neu_count = total - (pos_count + neg_count)
    pos_percent = round((pos_count / total * 100), 1) if total > 0 else 0

    cursor.execute('SELECT timestamp, dept_category, raw_text, sentiment_label FROM patient_feedback ORDER BY timestamp DESC LIMIT 20')
    recent_feedbacks = cursor.fetchall()
    conn.close()

    return jsonify({
        'total': total,
        'pos_percent': pos_percent,
        'pos_count': pos_count,
        'neg_count': neg_count,
        'neu_count': neu_count,
        'feedbacks': recent_feedbacks
    })

# UPDATED DEPARTMENT ROUTE (Now sends chart data)
@app.route('/analysis/<dept_name>')
def department_analysis(dept_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_feedback WHERE dept_category LIKE ? ORDER BY timestamp DESC", ('%' + dept_name + '%',))
    dept_feedbacks = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM patient_feedback WHERE dept_category LIKE ?", ('%' + dept_name + '%',))
    total_dept = cursor.fetchone()[0] or 0
    
    # Get Positive count for this specific department
    cursor.execute("SELECT COUNT(*) FROM patient_feedback WHERE dept_category LIKE ? AND sentiment_label = 'Positive'", ('%' + dept_name + '%',))
    pos_dept = cursor.fetchone()[0] or 0

    # Get Negative count for this specific department
    cursor.execute("SELECT COUNT(*) FROM patient_feedback WHERE dept_category LIKE ? AND sentiment_label = 'Negative'", ('%' + dept_name + '%',))
    neg_dept = cursor.fetchone()[0] or 0
    
    # Calculate Neutral
    neu_dept = total_dept - (pos_dept + neg_dept)
    conn.close()

    return render_template('analysis.html', 
                           dept=dept_name, 
                           feedbacks=dept_feedbacks, 
                           count=total_dept, 
                           issues=neg_dept,
                           pos_count=pos_dept,
                           neu_count=neu_dept,
                           neg_count=neg_dept)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)