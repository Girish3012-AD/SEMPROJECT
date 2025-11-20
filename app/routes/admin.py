from flask import Blueprint, request, jsonify, session
from app.db import get_db
from functools import wraps

bp = Blueprint('admin', __name__)

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return jsonify({'error': 'Admin access required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['POST'])
def admin_login():
    # This is handled in auth.py but kept here if specific admin login logic is needed separate from main login
    # For now, we'll just redirect to the main auth login or handle it there.
    # However, the original app had a specific admin login endpoint.
    # Let's replicate the logic from auth.py for admin specific endpoint if needed, 
    # or just rely on the unified login.
    # The original app had /api/admin/login.
    
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    db = get_db()
    cursor = db.cursor()
    
    from werkzeug.security import check_password_hash
    
    cursor.execute("SELECT admin_id, password_hash FROM admins WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and check_password_hash(result['password_hash'], password):
        session['admin'] = True
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@bp.route('/complaints', methods=['GET'])
@require_admin
def get_admin_complaints():
    db = get_db()
    cursor = db.cursor()
    
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
            'complaint_id': row['complaint_id'],
            'complaint_text': row['complaint_text'],
            'category': row['category'],
            'status': row['status'],
            'submitted_at': row['submitted_at'],
            'name': row['name'],
            'email': row['email']
        })
    return jsonify(complaints)

@bp.route('/complaints/update_status', methods=['PUT'])
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

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT status FROM complaints WHERE complaint_id = ?", (complaint_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({'error': 'Complaint not found'}), 404

        current_status = row['status']

        if current_status != 'Pending' and status == 'Pending':
             return jsonify({'error': 'Cannot set status back to Pending'}), 400

        cursor.execute("""
            UPDATE complaints
            SET status = ?, updated_at = datetime('now')
            WHERE complaint_id = ?
        """, (status, complaint_id))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Failed to update complaint'}), 500

        db.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/stats', methods=['GET'])
@require_admin
def get_admin_stats():
    db = get_db()
    cursor = db.cursor()
    
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
    status_counts = {row['status']: row['count'] for row in status_rows}
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
    by_category = {row['category']: row['count'] for row in category_rows}
    
    # Monthly complaints
    cursor.execute("""
        SELECT strftime('%Y-%m', submitted_at) as month, COUNT(*) as count
        FROM complaints
        WHERE submitted_at >= date('now', '-6 months')
        GROUP BY month
        ORDER BY month DESC
    """)
    monthly_rows = cursor.fetchall()
    monthly = [{"month": row['month'], "count": row['count']} for row in monthly_rows]
    
    return jsonify({
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'by_category': by_category,
        'monthly': monthly
    })
