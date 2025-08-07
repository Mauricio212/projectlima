from flask import render_template, session, redirect, url_for
import sqlite3

def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        conn = sqlite3.connect('lima_trading.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def get_user_by_email(email):
    """Get user data by email with error handling"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        conn.close()
        return None

def register_profile_page(app):
    """Register the profile page route with the Flask app"""
    
    @app.route('/settings')
    def profile_page():
        """Display the full-page profile editing form"""
        
        # Session validation
        if 'user_id' not in session or 'user_email' not in session:
            return redirect(url_for('index'))
        
        # Get user data
        user = get_user_by_email(session['user_email'])
        if not user:
            # Clear invalid session and redirect
            session.clear()
            return redirect(url_for('index'))
        
        # Render external template with user data
        try:
            return render_template('pages/profile.html', user=user)
        except Exception as e:
            print(f"Template rendering error: {e}")
            return "Profile page temporarily unavailable. Please try again later.", 500
