from flask import request, session, redirect, url_for
import sqlite3

def get_db_connection():
    """Get database connection (assuming same pattern as main app)"""
    conn = sqlite3.connect('lima_trading.db')
    conn.row_factory = sqlite3.Row
    return conn

def register_update_profile(app):
    @app.route('/update-profile', methods=['POST'])
    def update_profile():
        """Update user profile from form submission"""
        # Session validation
        if 'user_id' not in session:
            return redirect(url_for('index'))
        
        try:
            # Extract and validate form inputs
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            working_capital = float(request.form.get('working_capital'))
            risk_tolerance = request.form.get('risk_tolerance')
            trading_experience = request.form.get('trading_experience')
            
            # Basic validation
            if not all([first_name, last_name, working_capital, risk_tolerance, trading_experience]):
                return "Error: All fields are required", 400
                
            if working_capital < 1000:
                return "Error: Minimum working capital is $1,000", 400
            
            # Update user in database
            conn = get_db_connection()
            conn.execute("""
                UPDATE users 
                SET first_name = ?, last_name = ?, working_capital = ?, 
                    risk_tolerance = ?, trading_experience = ?
                WHERE email = ?
            """, (first_name, last_name, working_capital, risk_tolerance, trading_experience, session['user_email']))
            
            conn.commit()
            conn.close()
            
            # Success redirect
            return redirect('/dashboard?updated=1')
            
        except ValueError:
            return "Error: Invalid working capital amount", 400
        except Exception as e:
            return f"Error updating profile: {str(e)}", 500
