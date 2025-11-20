from flask import Blueprint, request, jsonify, session
from app.db import get_db
from functools import wraps

bp = Blueprint('complaints', __name__)

def require_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({'error': 'User authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/submit_complaint', methods=['POST'])
@require_user
def submit_complaint():
    data = request.json
    complaint_text = data.get('complaint_text')
    category = data.get('category')

    if not all([complaint_text, category]):
        return jsonify({'error': 'Missing required fields'}), 400

    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO complaints (user_id, complaint_text, category, submitted_at, updated_at)
            VALUES (?, ?, ?, datetime('now'), datetime('now'))
        """, (user_id, complaint_text, category))

        complaint_id = cursor.lastrowid
        db.commit()

        return jsonify({'success': True, 'complaint_id': complaint_id})

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/track_complaint', methods=['GET'])
@require_user
def track_complaint():
    complaint_id = request.args.get('id')
    if not complaint_id:
        return jsonify({'error': 'Complaint ID required'}), 400

    try:
        complaint_id = int(complaint_id)
    except ValueError:
        return jsonify({'error': 'Invalid Complaint ID'}), 400

    db = get_db()
    cursor = db.cursor()

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
        'complaint_id': row['complaint_id'],
        'complaint_text': row['complaint_text'],
        'status': row['status'],
        'submitted_at': row['submitted_at'],
        'category': row['category'],
        'name': row['name'],
        'email': row['email']
    }
    return jsonify(complaint)

@bp.route('/user_complaints', methods=['GET'])
def get_user_complaints():
    if not session.get('user_id'):
        return jsonify({'error': 'User authentication required'}), 401

    db = get_db()
    cursor = db.cursor()

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
            'complaint_id': row['complaint_id'],
            'complaint_text': row['complaint_text'],
            'category': row['category'],
            'status': row['status'],
            'submitted_at': row['submitted_at']
        })
    return jsonify(complaints)

@bp.route('/edit_complaint', methods=['PUT'])
@require_user
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

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT status FROM complaints
            WHERE complaint_id = ? AND user_id = ?
        """, (complaint_id, session['user_id']))

        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Complaint not found'}), 404

        if row['status'] != 'Pending':
            return jsonify({'error': 'Cannot edit complaint that is not pending'}), 400

        cursor.execute("""
            UPDATE complaints
            SET complaint_text = ?, category = ?, updated_at = datetime('now')
            WHERE complaint_id = ? AND user_id = ?
        """, (complaint_text, category, complaint_id, session['user_id']))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Failed to update complaint'}), 500

        db.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
