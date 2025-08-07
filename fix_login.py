import re

with open('web_app_professional_secured.py', 'r') as f:
    content = f.read()

login_code = """
@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def demo_login_endpoint():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        if email == 'demo@projectlima.com' and password == 'demo123':
            session['user_id'] = 'demo_user'
            session['email'] = email
            return jsonify({'status': 'success', 'redirect': '/dashboard'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Login failed'}), 500
"""

pattern = r"(\n+if __name__ == '__main__':)"
if re.search(pattern, content):
    new_content = re.sub(pattern, login_code + r'\1', content)
    with open('web_app_professional_secured.py', 'w') as f:
        f.write(new_content)
    print("✅ Fixed!")
else:
    print("❌ No main block found")
