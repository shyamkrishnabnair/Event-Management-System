import mysql.connector
from flask import Flask, request, jsonify

# Flask application setup
app = Flask(__name__)

# --- MySQL Database Configuration ---
# You MUST replace these with your actual MySQL credentials
DB_CONFIG = {
    'host': '127.0.0.1', # Replace with your host
    'user': 'your_user', # Replace with your MySQL username
    'password': 'your_password', # Replace with your MySQL password
    'database': 'event_management' # The database must be created beforehand
}

# --- Database Connection and Cursors ---
def get_db_connection():
    """
    Establishes a connection to the MySQL database.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database():
    """
    Creates and initializes the MySQL database tables with dummy data.
    This function should be run once to set up the database schema.
    """
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database. Exiting.")
        return
        
    cursor = conn.cursor()

    # Create Colleges table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Colleges (
            college_id INT AUTO_INCREMENT PRIMARY KEY,
            college_name VARCHAR(255) NOT NULL,
            location VARCHAR(255)
        )
    ''')

    # Create Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            college_id INT,
            FOREIGN KEY (college_id) REFERENCES Colleges (college_id) ON DELETE CASCADE
        )
    ''')

    # Create Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            event_id INT AUTO_INCREMENT PRIMARY KEY,
            event_name VARCHAR(255) NOT NULL,
            description TEXT,
            event_type VARCHAR(255),
            event_date DATE NOT NULL,
            college_id INT,
            FOREIGN KEY (college_id) REFERENCES Colleges (college_id) ON DELETE CASCADE
        )
    ''')

    # Create Registrations table (includes attendance and feedback)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Registrations (
            registration_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            event_id INT,
            registration_date DATE NOT NULL,
            attendance_status ENUM('Registered', 'Attended', 'Not Attended') NOT NULL,
            feedback_score INT,
            UNIQUE KEY unique_registration (student_id, event_id),
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE,
            FOREIGN KEY (event_id) REFERENCES Events (event_id) ON DELETE CASCADE
        )
    ''')
    
    # --- Add Dummy Data ---
    print("Inserting dummy data into tables...")
    try:
        # Dummy Colleges
        cursor.execute("INSERT IGNORE INTO Colleges (college_id, college_name, location) VALUES (%s, %s, %s)", (1, 'Tech University', 'Bengaluru'))
        cursor.execute("INSERT IGNORE INTO Colleges (college_id, college_name, location) VALUES (%s, %s, %s)", (2, 'State College', 'Mumbai'))

        # Dummy Students
        cursor.execute("INSERT IGNORE INTO Students (student_id, student_name, email, college_id) VALUES (%s, %s, %s, %s)", (101, 'Alice Johnson', 'alice.j@example.com', 1))
        cursor.execute("INSERT IGNORE INTO Students (student_id, student_name, email, college_id) VALUES (%s, %s, %s, %s)", (102, 'Bob Williams', 'bob.w@example.com', 1))
        cursor.execute("INSERT IGNORE INTO Students (student_id, student_name, email, college_id) VALUES (%s, %s, %s, %s)", (201, 'Charlie Davis', 'charlie.d@example.com', 2))
        
        # Dummy Events
        cursor.execute("INSERT IGNORE INTO Events (event_id, event_name, description, event_type, event_date, college_id) VALUES (%s, %s, %s, %s, %s, %s)", (1, 'Web Dev Workshop', 'Intro to Flask & APIs', 'Workshop', '2025-10-26', 1))
        cursor.execute("INSERT IGNORE INTO Events (event_id, event_name, description, event_type, event_date, college_id) VALUES (%s, %s, %s, %s, %s, %s)", (2, 'AI & ML Talk', 'A talk on the future of AI', 'Tech Talk', '2025-11-15', 1))
        cursor.execute("INSERT IGNORE INTO Events (event_id, event_name, description, event_type, event_date, college_id) VALUES (%s, %s, %s, %s, %s, %s)", (3, 'Annual Fest', 'The biggest cultural event of the year', 'Fest', '2025-12-01', 2))
        
        # Dummy Registrations
        cursor.execute("INSERT IGNORE INTO Registrations (student_id, event_id, registration_date, attendance_status, feedback_score) VALUES (%s, %s, %s, %s, %s)", (101, 1, '2025-10-10', 'Attended', 5))
        cursor.execute("INSERT IGNORE INTO Registrations (student_id, event_id, registration_date, attendance_status, feedback_score) VALUES (%s, %s, %s, %s, %s)", (102, 1, '2025-10-10', 'Attended', 4))
        cursor.execute("INSERT IGNORE INTO Registrations (student_id, event_id, registration_date, attendance_status, feedback_score) VALUES (%s, %s, %s, %s, %s)", (201, 3, '2025-10-15', 'Registered', None))

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting dummy data: {err}")
        conn.rollback()

    cursor.close()
    conn.close()

# --- API Endpoints ---
@app.route('/events', methods=['POST'])
def create_event():
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Events (event_name, description, event_type, event_date, college_id) VALUES (%s, %s, %s, %s, %s)",
            (data['event_name'], data['description'], data['event_type'], data['event_date'], data['college_id'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Event created successfully"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True) # Returns results as dictionaries
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(events), 200

@app.route('/students/register', methods=['POST'])
def register_student():
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Registrations (student_id, event_id, registration_date, attendance_status) VALUES (%s, %s, CURDATE(), 'Registered')",
            (data['student_id'], data['event_id'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Student registered successfully"}), 201
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            return jsonify({"error": "Student is already registered for this event."}), 409
        return jsonify({"error": str(e)}), 500

@app.route('/events/<int:event_id>/attendance', methods=['POST'])
def mark_attendance(event_id):
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Registrations SET attendance_status = 'Attended' WHERE student_id = %s AND event_id = %s",
            (data['student_id'], event_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Registration not found."}), 404
        cursor.close()
        conn.close()
        return jsonify({"message": "Attendance marked successfully"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/events/<int:event_id>/feedback', methods=['POST'])
def collect_feedback(event_id):
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Registrations SET feedback_score = %s WHERE student_id = %s AND event_id = %s",
            (data['score'], data['student_id'], event_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Registration not found."}), 404
        cursor.close()
        conn.close()
        return jsonify({"message": "Feedback submitted successfully"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

# --- Reporting Endpoints ---
@app.route('/reports/registrations', methods=['GET'])
def total_registrations_report():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            E.event_name,
            COUNT(R.registration_id) AS total_registrations
        FROM Events E
        LEFT JOIN Registrations R ON E.event_id = R.event_id
        GROUP BY E.event_name
        ORDER BY total_registrations DESC
    """)
    report = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(report), 200

@app.route('/reports/attendance', methods=['GET'])
def attendance_percentage_report():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            E.event_name,
            (SUM(CASE WHEN R.attendance_status = 'Attended' THEN 1 ELSE 0 END) * 100.0 / COUNT(R.registration_id)) AS attendance_percentage
        FROM Events E
        JOIN Registrations R ON E.event_id = R.event_id
        GROUP BY E.event_name
    """)
    report = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(report), 200

@app.route('/reports/feedback', methods=['GET'])
def average_feedback_report():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            E.event_name,
            AVG(R.feedback_score) AS average_score
        FROM Events E
        JOIN Registrations R ON E.event_id = R.event_id
        WHERE R.feedback_score IS NOT NULL
        GROUP BY E.event_name
    """)
    report = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(report), 200

@app.route('/reports/students/top_active', methods=['GET'])
def top_active_students_report():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            S.student_id,
            S.student_name,
            COUNT(R.registration_id) AS events_attended
        FROM Students S
        JOIN Registrations R ON S.student_id = R.student_id
        WHERE R.attendance_status = 'Attended'
        GROUP BY S.student_id, S.student_name
        ORDER BY events_attended DESC
        LIMIT 3
    """)
    report = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(report), 200

@app.route('/reports/events/filter', methods=['GET'])
def filter_events_report():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    event_type = request.args.get('type')

    if not event_type:
        return jsonify({"error": "Missing 'type' query parameter."}), 400

    cursor.execute("""
        SELECT
            E.event_name,
            E.event_type,
            COUNT(R.registration_id) AS total_registrations
        FROM Events E
        LEFT JOIN Registrations R ON E.event_id = R.event_id
        WHERE E.event_type = %s
        GROUP BY E.event_name, E.event_type
        ORDER BY total_registrations DESC
    """, (event_type,))
    report = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(report), 200


if __name__ == '__main__':
    create_database()
    app.run(debug=True, port=5000)
