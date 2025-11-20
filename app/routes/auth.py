from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['POST'])
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
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT user_id FROM users WHERE email = ? OR (username = ? AND username IS NOT NULL)", (email, username))
        existing = cursor.fetchone()
        if existing:
            return jsonify({'error': 'Email or username already exists'}), 400
        
        cursor.execute("""
            INSERT INTO users (name, email, username, password_hash)
            VALUES (?, ?, ?, ?)
        """, (name, email, username, hashed_password))
        
        db.commit()
        return jsonify({'success': True, 'message': 'User created successfully'})
    
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('identifier')
    password = data.get('password')
    
    if not identifier or not password:
        return jsonify({'error': 'Identifier and password required'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    # Check users
    cursor.execute("SELECT user_id, password_hash, name FROM users WHERE username = ? OR email = ?", (identifier, identifier))
    user_result = cursor.fetchone()
    
    if user_result and check_password_hash(user_result['password_hash'], password):
        session['user_id'] = user_result['user_id']
        session['user_name'] = user_result['name']
        session.pop('admin', None)
        return jsonify({'success': True, 'type': 'user'})
    
    # Check admins
    cursor.execute("SELECT admin_id, password_hash FROM admins WHERE username = ?", (identifier,))
    admin_result = cursor.fetchone()
    
    if admin_result and check_password_hash(admin_result['password_hash'], password):
        session['admin'] = True
        session.pop('user_id', None)
        session.pop('user_name', None)
        return jsonify({'success': True, 'type': 'admin'})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})
