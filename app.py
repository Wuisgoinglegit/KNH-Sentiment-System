from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# custom scripts
from sentiment_engine import SentimentEngine
from department_detection import detect_department 

app = Flask(__name__)

# THE SECRET KEY: Required to securely remember who logged in
app.secret_key = 'knh_secure_super_secret_key_2026' 

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

# CACHE CONTROL: Prevents the browser back button from loading secure pages after logout
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/')
def home():
    # Catches success messages from the redirect
    success = request.args.get('success')
    dept_name = request.args.get('dept')
    return render_template('patient feedback.html', success=success, dept_name=dept_name)

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

        # PRG FIX: Redirects cleanly to the home page to prevent resubmission popups
        return redirect(url_for('home', success='true', dept=department_result))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Catches errors from the redirect to display on a clean page
    error_msg = None
    err_code = request.args.get('error')
    if err_code == 'mismatch':
        error_msg = "Passwords do not match!"
    elif err_code == 'exists':
        error_msg = "This Staff ID already exists!"

    if request.method == 'POST':
        staff_id = request.form.get('staffId')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return redirect(url_for('register', error='mismatch'))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin_users WHERE staff_id = ?', (staff_id,))
        if cursor.fetchone():
            conn.close()
            return redirect(url_for('register', error='exists'))

        hashed_pw = generate_password_hash(password)
        cursor.execute('INSERT INTO admin_users (staff_id, password_hash) VALUES (?, ?)', (staff_id, hashed_pw))
        conn.commit()
        conn.close()
        
        # PRG FIX: Redirects cleanly to login upon success
        return redirect(url_for('login', registered='success'))
        
    return render_template('register.html', error=error_msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    success_msg = None
    if request.args.get('registered') == 'success':
        success_msg = "Account created successfully! Please log in."
        
    error_msg = None
    if request.args.get('error') == 'invalid':
        error_msg = "Invalid Staff ID or Password."

    if request.method == 'POST':
        staff_id = request.form.get('staffId')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM admin_users WHERE staff_id = ?', (staff_id,))
        user_record = cursor.fetchone()
        conn.close()

        if user_record and check_password_hash(user_record[0], password):
            # SECURE LOGIN: Save ID into the session memory
            session['staff_id'] = staff_id
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login', error='invalid'))
            
    return render_template('login.html', error_msg=error_msg, success_msg=success_msg)

# LOGOUT ROUTE: Destroys the session memory
@app.route('/logout')
def logout():
    session.pop('staff_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    # PROTECT ROUTE: If they aren't in the session memory, kick them back to login
    if 'staff_id' not in session:
        return redirect(url_for('login'))

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

    return render_template('dashboard.html', 
                           feedbacks=feedbacks, 
                           total=total, 
                           pos_percent=pos_percent, 
                           pos_count=pos_count, 
                           neu_count=neu_count, 
                           neg_count=neg_count,
                           staff_id=session['staff_id'])

@app.route('/api/dashboard_data')
def api_dashboard_data():
    if 'staff_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

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

@app.route('/analysis/<dept_name>')
def department_analysis(dept_name):
    # PROTECT ROUTE
    if 'staff_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_feedback WHERE dept_category LIKE ? ORDER BY timestamp DESC", ('%' + dept_name + '%',))
    dept_feedbacks = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM patient_feedback WHERE dept_category LIKE ?", ('%' + dept_name + '%',))
    total_dept = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM patient_feedback WHERE dept_category LIKE ? AND sentiment_label = 'Positive'", ('%' + dept_name + '%',))
    pos_dept = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM patient_feedback WHERE dept_category LIKE ? AND sentiment_label = 'Negative'", ('%' + dept_name + '%',))
    neg_dept = cursor.fetchone()[0] or 0
    
    neu_dept = total_dept - (pos_dept + neg_dept)
    conn.close()

    return render_template('analysis.html', 
                           dept=dept_name, 
                           feedbacks=dept_feedbacks, 
                           count=total_dept, 
                           issues=neg_dept,
                           pos_count=pos_dept,
                           neu_count=neu_dept,
                           neg_count=neg_dept,
                           staff_id=session['staff_id'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)