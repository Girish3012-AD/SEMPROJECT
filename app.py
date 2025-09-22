from flask import Flask, request, jsonify, session, send_from_directory, redirect
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production
app.static_folder = '.'  # Serve static files from current directory
CORS(app)

# Database path
DB_PATH = 'complaint_box.db'

def get_db_connection():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row  # For dictionary-like rows
        return connection
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def init_db():
    """Initialize the database by creating tables if they don't exist."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    
    # Create admins table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    
    # Create complaints table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            complaint_text TEXT NOT NULL,
            category TEXT,
            status TEXT DEFAULT 'Pending',
            submitted_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Add password_hash to users if it doesn't exist (for existing DBs)
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'password_hash' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    
    # Create default admin if none exists
    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        default_username = 'admin'
        default_password = 'admin123'  # Change this in production
        hashed_password = generate_password_hash(default_password)
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", 
                       (default_username, hashed_password))
        print(f"Default admin created: username={default_username}, password={default_password}")
    
    conn.commit()
    cursor.close()
    conn.close()
    return True

# Initialize DB on startup
with app.app_context():
    init_db()

def require_admin(f):
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return jsonify({'error': 'Admin access required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_user(f):
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({'error': 'User authentication required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function
@app.before_request
def log_request():
    print(f"Request: {request.method} {request.url}")

@app.route('/')
def index():
    print(f"Serving index.html from directory: {os.getcwd()}")
    if not os.path.exists('index.html'):
        print("ERROR: index.html not found")
        return "File not found", 404
    return send_from_directory('.', 'index.html')

@app.route('/submit.html')
def submit():
    return send_from_directory('.', 'submit.html')

@app.route('/track.html')
def track():
    return send_from_directory('.', 'track.html')

@app.route('/admin_login.html')
def admin_login_page():
    print("Serving admin_login.html")
    return send_from_directory('.', 'admin_login.html')

@app.route('/admin_dashboard.html')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin_login.html')
    return send_from_directory('.', 'admin_dashboard.html')

@app.route('/<path:filename>')
def static_files(filename):
    print(f"Serving {filename} from directory: {os.getcwd()}")
    if not os.path.exists(filename):
        print(f"ERROR: {filename} not found")
        return "File not found", 404
    return send_from_directory('.', filename)

@require_user
@app.route('/api/submit_complaint', methods=['POST'])
def submit_complaint():
    data = request.json
    complaint_text = data.get('complaint_text')
    category = data.get('category')

    if not all([complaint_text, category]):
        return jsonify({'error': 'Missing required fields'}), 400

    user_id = session['user_id']

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()

    try:
        # Insert complaint
        cursor.execute("""
            INSERT INTO complaints (user_id, complaint_text, category, submitted_at, updated_at)
            VALUES (?, ?, ?, datetime('now'), datetime('now'))
        """, (user_id, complaint_text, category))

        complaint_id = cursor.lastrowid
        conn.commit()

        return jsonify({'success': True, 'complaint_id': complaint_id})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@require_user
@app.route('/api/track_complaint', methods=['GET'])
def track_complaint():
    complaint_id = request.args.get('id')
    if not complaint_id:
        return jsonify({'error': 'Complaint ID required'}), 400

    try:
        complaint_id = int(complaint_id)
    except ValueError:
        return jsonify({'error': 'Invalid Complaint ID'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT c.complaint_id, c.complaint_text, c.status, c.submitted_at, c.category,
                   u.name, u.email
            FROM complaints c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.complaint_id = ? AND c.user_id = ?
        """, (complaint_id, session['user_id']))

        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Complaint not found'}), 404

        complaint = {
            'complaint_id': row[0],
            'complaint_text': row[1],
            'status': row[2],
            'submitted_at': row[3],
            'category': row[4],
            'name': row[5],
            'email': row[6]
        }
        return jsonify(complaint)

    finally:
        cursor.close()
        conn.close()

@app.route('/api/user_complaints', methods=['GET'])
def get_user_complaints():
    if not session.get('user_id'):
        return jsonify({'error': 'User authentication required'}), 401

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT complaint_id, complaint_text, category, status, submitted_at
            FROM complaints
            WHERE user_id = ?
            ORDER BY submitted_at DESC
        """, (session['user_id'],))

        rows = cursor.fetchall()
        complaints = []
        for row in rows:
            complaints.append({
                'complaint_id': row[0],
                'complaint_text': row[1],
                'category': row[2],
                'status': row[3],
                'submitted_at': row[4]
            })
        return jsonify(complaints)

    finally:
        cursor.close()
        conn.close()

@require_user
@app.route('/api/edit_complaint', methods=['PUT'])
def edit_complaint():
    data = request.json
    complaint_id = data.get('complaint_id')
    complaint_text = data.get('complaint_text')
    category = data.get('category')

    if not all([complaint_id, complaint_text, category]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        complaint_id = int(complaint_id)
    except ValueError:
        return jsonify({'error': 'Invalid Complaint ID'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()

    try:
        # Check if complaint exists, belongs to user, and status is Pending
        cursor.execute("""
            SELECT status FROM complaints
            WHERE complaint_id = ? AND user_id = ?
        """, (complaint_id, session['user_id']))

        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Complaint not found'}), 404

        if row[0] != 'Pending':
            return jsonify({'error': 'Cannot edit complaint that is not pending'}), 400

        # Update complaint
        cursor.execute("""
            UPDATE complaints
            SET complaint_text = ?, category = ?, updated_at = datetime('now')
            WHERE complaint_id = ? AND user_id = ?
        """, (complaint_text, category, complaint_id, session['user_id']))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Failed to update complaint'}), 500

        conn.commit()
        return jsonify({'success': True})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    print(f"Admin login attempt: username={username}")

    if not username or not password:
        print("Missing username or password")
        return jsonify({'error': 'Username and password required'}), 400

    conn = get_db_connection()
    if conn is None:
        print("Database connection failed")
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password_hash FROM admins WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            print(f"Found admin user, checking password")
            if check_password_hash(result[0], password):
                session['admin'] = True
                print("Admin login successful")
                return jsonify({'success': True})
            else:
                print("Password check failed")
                return jsonify({'error': 'Invalid credentials'}), 401
        else:
            print(f"No admin user found with username: {username}")
            return jsonify({'error': 'Invalid credentials'}), 401

    finally:
        cursor.close()
        conn.close()

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    
    if not all([name, email, password]):
        return jsonify({'error': 'Name, email, and password are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    hashed_password = generate_password_hash(password)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    
    try:
        # Check for existing email or username
        cursor.execute("SELECT user_id FROM users WHERE email = ? OR (username = ? AND username IS NOT NULL)", (email, username))
        existing = cursor.fetchone()
        if existing:
            return jsonify({'error': 'Email or username already exists'}), 400
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (name, email, username, password_hash)
            VALUES (?, ?, ?, ?)
        """, (name, email, username, hashed_password))
        
        conn.commit()
        return jsonify({'success': True, 'message': 'User created successfully'})
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('identifier')  # username or email
    password = data.get('password')
    
    if not identifier or not password:
        return jsonify({'error': 'Identifier and password required'}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    
    try:
        # First check users table
        cursor.execute("""
            SELECT user_id, password_hash, name FROM users WHERE username = ? OR email = ?
        """, (identifier, identifier))
        user_result = cursor.fetchone()
        
        if user_result and check_password_hash(user_result[1], password):
            session['user_id'] = user_result[0]
            session['user_name'] = user_result[2]
            session.pop('admin', None)  # Clear admin session if any
            return jsonify({'success': True, 'type': 'user'})
        
        # Then check admins table
        cursor.execute("SELECT admin_id, password_hash FROM admins WHERE username = ?", (identifier,))
        admin_result = cursor.fetchone()
        
        if admin_result and check_password_hash(admin_result[1], password):
            session['admin'] = True
            session.pop('user_id', None)  # Clear user session if any
            session.pop('user_name', None)
            return jsonify({'success': True, 'type': 'admin'})
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/admin/complaints', methods=['GET'])
@require_admin
def get_admin_complaints():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT c.complaint_id, c.complaint_text, c.category, c.status, c.submitted_at,
                   u.name, u.email
            FROM complaints c
            JOIN users u ON c.user_id = u.user_id
            ORDER BY c.submitted_at DESC
        """)
        
        rows = cursor.fetchall()
        complaints = []
        for row in rows:
            complaints.append({
                'complaint_id': row[0],
                'complaint_text': row[1],
                'category': row[2],
                'status': row[3],
                'submitted_at': row[4],
                'name': row[5],
                'email': row[6]
            })
        return jsonify(complaints)
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/complaints/update_status', methods=['PUT'])
@require_admin
def update_complaint_status():
    data = request.json
    complaint_id = data.get('complaint_id')
    status = data.get('status')
    
    if not complaint_id or status not in ['Pending', 'In Progress', 'Resolved']:
        return jsonify({'error': 'Invalid complaint_id or status'}), 400
    
    try:
        complaint_id = int(complaint_id)
    except ValueError:
        return jsonify({'error': 'Invalid Complaint ID'}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE complaints 
            SET status = ?, updated_at = datetime('now')
            WHERE complaint_id = ?
        """, (status, complaint_id))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Complaint not found'}), 404
        
        conn.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/stats', methods=['GET'])
@require_admin
def get_admin_stats():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    
    try:
        # Total complaints
        cursor.execute("SELECT COUNT(*) FROM complaints")
        total = cursor.fetchone()[0]
        
        # Counts by status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM complaints 
            GROUP BY status
        """)
        status_rows = cursor.fetchall()
        status_counts = {row[0]: row[1] for row in status_rows}
        pending = status_counts.get('Pending', 0)
        in_progress = status_counts.get('In Progress', 0)
        resolved = status_counts.get('Resolved', 0)
        
        # By category
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM complaints 
            GROUP BY category
        """)
        category_rows = cursor.fetchall()
        by_category = {row[0]: row[1] for row in category_rows}
        
        # Monthly complaints (last 6 months) - SQLite date handling
        cursor.execute("""
            SELECT strftime('%Y-%m', submitted_at) as month, COUNT(*) as count
            FROM complaints
            WHERE submitted_at >= date('now', '-6 months')
            GROUP BY month
            ORDER BY month DESC
        """)
        monthly_rows = cursor.fetchall()
        monthly = [{"month": row[0], "count": row[1]} for row in monthly_rows]
        
        return jsonify({
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'resolved': resolved,
            'by_category': by_category,
            'monthly': monthly
        })
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)