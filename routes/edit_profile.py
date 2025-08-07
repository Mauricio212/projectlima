from flask import render_template_string, session, redirect, url_for
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('lima_trading.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return dict(user) if user else None

def register_edit_profile(app):
    @app.route('/profile')
    def profile():
        if 'user_id' not in session:
            return redirect(url_for('index'))
        
        user = get_user_by_email(session['user_email'])
        if not user:
            return redirect(url_for('logout'))
        
        return "Profile page working! User: " + user['first_name']
