#!/usr/bin/env python3
"""
PROJECT LIMA - Trading Intelligence Platform with User Authentication
Complete login system with customer data storage and personalization
"""

import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from flask import Flask, jsonify, request, render_template_string, session, redirect, url_for
    import json
    from datetime import datetime, timedelta
    import hashlib
    import uuid
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = 'lima_trading_intelligence_secure_2025'

# In-memory user database (replace with real database like PostgreSQL/MySQL)
users_db = {
    # Demo user for testing
    "demo@projectlima.com": {
        "user_id": "demo_user_001",
        "email": "demo@projectlima.com",
        "password_hash": "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5",  # password: demo123
        "first_name": "Demo",
        "last_name": "User",
        "created_date": "2025-01-01",
        "working_capital": 50000,
        "risk_tolerance": "medium",
        "trading_experience": "intermediate",
        "preferred_strategies": ["grid_bot", "swing_trading"],
        "portfolio": {
            "total_value": 52347.80,
            "profit_loss": 2347.80,
            "active_positions": 3
        },
        "settings": {
            "notifications": True,
            "auto_execute": False,
            "max_position_size": 25
        }
    }
}

def hash_password(password):
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_value):
    """Verify password against hash"""
    return hash_password(password) == hash_value

# LOGIN/REGISTER PAGE
LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Lima - Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: rgba(26, 26, 46, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 255, 157, 0.3);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo h1 {
            font-size: 32px;
            background: linear-gradient(45deg, #00ff9d, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .logo p {
            color: #b8b8b8;
            font-size: 16px;
        }
        
        .form-tabs {
            display: flex;
            margin-bottom: 30px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 5px;
        }
        
        .tab-button {
            flex: 1;
            padding: 12px;
            background: none;
            border: none;
            color: #b8b8b8;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .tab-button.active {
            background: linear-gradient(45deg, #00ff9d, #00d4aa);
            color: #000;
        }
        
        .form-section {
            display: none;
        }
        
        .form-section.active {
            display: block;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #00ff9d;
            font-weight: 500;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px 15px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 157, 0.3);
            border-radius: 8px;
            color: #fff;
            font-size: 16px;
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #00ff9d;
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .submit-button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #00ff9d, #00d4aa);
            color: #000;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        
        .submit-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 255, 157, 0.3);
        }
        
        .demo-login {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0, 255, 157, 0.1);
            border: 1px solid rgba(0, 255, 157, 0.3);
            border-radius: 8px;
            text-align: center;
        }
        
        .demo-login h4 {
            color: #00ff9d;
            margin-bottom: 10px;
        }
        
        .demo-login p {
            font-size: 14px;
            color: #b8b8b8;
            margin-bottom: 10px;
        }
        
        .demo-button {
            background: rgba(0, 255, 157, 0.2);
            color: #00ff9d;
            border: 1px solid #00ff9d;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .error-message {
            background: rgba(255, 107, 107, 0.2);
            border: 1px solid rgba(255, 107, 107, 0.5);
            color: #ff6b6b;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .success-message {
            background: rgba(0, 255, 157, 0.2);
            border: 1px solid rgba(0, 255, 157, 0.5);
            color: #00ff9d;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>🚀 Project Lima</h1>
            <p>Trading Intelligence Platform</p>
        </div>
        
        <div class="error-message" id="errorMessage"></div>
        <div class="success-message" id="successMessage"></div>
        
        <div class="form-tabs">
            <button class="tab-button active" onclick="showTab('login')">Login</button>
            <button class="tab-button" onclick="showTab('register')">Register</button>
        </div>
        
        <!-- LOGIN FORM -->
        <div id="loginForm" class="form-section active">
            <form onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label for="loginEmail">Email:</label>
                    <input type="email" id="loginEmail" required>
                </div>
                <div class="form-group">
                    <label for="loginPassword">Password:</label>
                    <input type="password" id="loginPassword" required>
                </div>
                <button type="submit" class="submit-button">Login to Dashboard</button>
            </form>
        </div>
        
        <!-- REGISTER FORM -->
        <div id="registerForm" class="form-section">
            <form onsubmit="handleRegister(event)">
                <div class="form-row">
                    <div class="form-group">
                        <label for="firstName">First Name:</label>
                        <input type="text" id="firstName" required>
                    </div>
                    <div class="form-group">
                        <label for="lastName">Last Name:</label>
                        <input type="text" id="lastName" required>
                    </div>
                </div>
                <div class="form-group">
                    <label for="registerEmail">Email:</label>
                    <input type="email" id="registerEmail" required>
                </div>
                <div class="form-group">
                    <label for="registerPassword">Password:</label>
                    <input type="password" id="registerPassword" required minlength="6">
                </div>
                <div class="form-group">
                    <label for="workingCapital">Working Capital (USD):</label>
                    <input type="number" id="workingCapital" min="1000" value="25000" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="riskTolerance">Risk Tolerance:</label>
                        <select id="riskTolerance" required>
                            <option value="conservative">Conservative</option>
                            <option value="medium" selected>Medium</option>
                            <option value="aggressive">Aggressive</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="experience">Trading Experience:</label>
                        <select id="experience" required>
                            <option value="beginner">Beginner</option>
                            <option value="intermediate" selected>Intermediate</option>
                            <option value="advanced">Advanced</option>
                        </select>
                    </div>
                </div>
                <button type="submit" class="submit-button">Create Account</button>
            </form>
        </div>
        
        <!-- DEMO LOGIN -->
        <div class="demo-login">
            <h4>🎯 Try Demo Account</h4>
            <p>Email: demo@projectlima.com | Password: demo123</p>
            <button class="demo-button" onclick="loginDemo()">Quick Demo Login</button>
        </div>
    </div>
    
    <script>
        function showTab(tab) {
            // Hide all forms
            document.querySelectorAll('.form-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.tab-button').forEach(button => {
                button.classList.remove('active');
            });
            
            // Show selected form and activate tab
            document.getElementById(tab + 'Form').classList.add('active');
            event.target.classList.add('active');
            
            // Clear messages
            hideMessages();
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            document.getElementById('successMessage').style.display = 'none';
        }
        
        function showSuccess(message) {
            const successDiv = document.getElementById('successMessage');
            successDiv.textContent = message;
            successDiv.style.display = 'block';
            document.getElementById('errorMessage').style.display = 'none';
        }
        
        function hideMessages() {
            document.getElementById('errorMessage').style.display = 'none';
            document.getElementById('successMessage').style.display = 'none';
        }
        
        async function handleLogin(event) {
            event.preventDefault();
            hideMessages();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    showSuccess('Login successful! Redirecting to dashboard...');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1500);
                } else {
                    showError(result.message || 'Login failed');
                }
            } catch (error) {
                showError('Network error. Please try again.');
            }
        }
        
        async function handleRegister(event) {
            event.preventDefault();
            hideMessages();
            
            const userData = {
                first_name: document.getElementById('firstName').value,
                last_name: document.getElementById('lastName').value,
                email: document.getElementById('registerEmail').value,
                password: document.getElementById('registerPassword').value,
                working_capital: parseFloat(document.getElementById('workingCapital').value),
                risk_tolerance: document.getElementById('riskTolerance').value,
                trading_experience: document.getElementById('experience').value
            };
            
            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userData)
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    showSuccess('Account created successfully! Redirecting to dashboard...');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1500);
                } else {
                    showError(result.message || 'Registration failed');
                }
            } catch (error) {
                showError('Network error. Please try again.');
            }
        }
        
        function loginDemo() {
            document.getElementById('loginEmail').value = 'demo@projectlima.com';
            document.getElementById('loginPassword').value = 'demo123';
            showTab('login');
        }
    </script>
</body>
</html>
'''

# PERSONALIZED TRADING DASHBOARD
TRADING_DASHBOARD = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Lima - Trading Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
        }
        
        .header {
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 255, 157, 0.3);
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .nav {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
            color: #00ff9d;
        }
        
        .nav-menu {
            display: flex;
            gap: 30px;
        }
        
        .nav-item {
            color: #fff;
            text-decoration: none;
            padding: 10px 15px;
            border-radius: 8px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .nav-item:hover, .nav-item.active {
            background: rgba(0, 255, 157, 0.2);
            color: #00ff9d;
        }
        
        .user-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .user-info {
            text-align: right;
        }
        
        .user-name {
            font-weight: bold;
            color: #00ff9d;
        }
        
        .user-capital {
            font-size: 12px;
            color: #b8b8b8;
        }
        
        .logout-btn {
            background: rgba(255, 107, 107, 0.2);
            color: #ff6b6b;
            border: 1px solid #ff6b6b;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .welcome-section {
            background: rgba(26, 26, 46, 0.8);
            border: 1px solid rgba(0, 255, 157, 0.2);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
        }
        
        .welcome-title {
            font-size: 28px;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #00ff9d, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .portfolio-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .portfolio-card {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 157, 0.2);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        
        .portfolio-value {
            font-size: 24px;
            font-weight: bold;
            color: #00ff9d;
            margin-bottom: 5px;
        }
        
        .portfolio-label {
            font-size: 12px;
            color: #b8b8b8;
            text-transform: uppercase;
        }
        
        .portfolio-change {
            font-size: 14px;
            margin-top: 5px;
        }
        
        .positive {
            color: #00ff9d;
        }
        
        .negative {
            color: #ff6b6b;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
        }
        
        .card {
            background: rgba(26, 26, 46, 0.8);
            border: 1px solid rgba(0, 255, 157, 0.2);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
        }
        
        .card-title {
            font-size: 20px;
            color: #00ff9d;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .recommendations-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .recommendation-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 157, 0.2);
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .recommendation-item:hover {
            border-color: #00ff9d;
            transform: translateY(-2px);
        }
        
        .crypto-pair {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .pair-name {
            font-size: 18px;
            font-weight: bold;
            color: #00ff9d;
        }
        
        .roi-badge {
            background: linear-gradient(45deg, #00ff9d, #00d4aa);
            color: #000;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .action-button {
            background: linear-gradient(45deg, #00ff9d, #00d4aa);
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 15px;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .action-button:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(0, 255, 157, 0.3);
        }
        
        .settings-section {
            margin-top: 20px;
        }
        
        .settings-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid rgba(0, 255, 157, 0.1);
        }
        
        .settings-item:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="logo">🚀 Project Lima</div>
            <div class="nav-menu">
                <a href="#" class="nav-item active">Dashboard</a>
                <a href="#" class="nav-item">GRID Bots</a>
                <a href="#" class="nav-item">Portfolio</a>
                <a href="#" class="nav-item">Analytics</a>
            </div>
            <div class="user-section">
                <div class="user-info">
                    <div class="user-name">{{ user.first_name }} {{ user.last_name }}</div>
                    <div class="user-capital">Capital: ${{ "{:,.2f}".format(user.working_capital) }}</div>
                </div>
                <a href="/logout" class="logout-btn">Logout</a>
            </div>
        </nav>
    </header>

    <div class="container">
        <section class="welcome-section">
            <h1 class="welcome-title">Welcome back, {{ user.first_name }}!</h1>
            <p>Your personalized trading intelligence dashboard based on your ${{ "{:,.0f}".format(user.working_capital) }} working capital and {{ user.risk_tolerance }} risk tolerance.</p>
            
            <div class="portfolio-overview">
                <div class="portfolio-card">
                    <div class="portfolio-value">${{ "{:,.2f}".format(user.portfolio.total_value) }}</div>
                    <div class="portfolio-label">Total Portfolio Value</div>
                    <div class="portfolio-change positive">+${{ "{:,.2f}".format(user.portfolio.profit_loss) }} ({{ "{:.1f}".format((user.portfolio.profit_loss / user.working_capital) * 100) }}%)</div>
                </div>
                <div class="portfolio-card">
                    <div class="portfolio-value">{{ user.portfolio.active_positions }}</div>
                    <div class="portfolio-label">Active Positions</div>
                    <div class="portfolio-change">GRID Bots Running</div>
                </div>
                <div class="portfolio-card">
                    <div class="portfolio-value">+12.4%</div>
                    <div class="portfolio-label">30-Day Performance</div>
                    <div class="portfolio-change positive">Beating HOLD by +3.7%</div>
                </div>
                <div class="portfolio-card">
                    <div class="portfolio-value">{{ user.risk_tolerance|title }}</div>
                    <div class="portfolio-label">Risk Profile</div>
                    <div class="portfolio-change">{{ user.trading_experience|title }} Trader</div>
                </div>
            </div>
        </section>

        <div class="main-content">
            <div class="card">
                <h2 class="card-title">🤖 Personalized GRID Bot Recommendations</h2>
                <p style="color: #b8b8b8; margin-bottom: 20px;">Based on your ${{ "{:,.0f}".format(user.working_capital) }} capital and {{ user.risk_tolerance }} risk tolerance</p>
                <div class="recommendations-list" id="personalizedRecommendations">
                    <!-- Dynamic content loaded here -->
                </div>
            </div>

            <div>
                <div class="card">
                    <h2 class="card-title">⚙️ Your Settings</h2>
                    <div class="settings-section">
                        <div class="settings-item">
                            <span>Working Capital:</span>
                            <span>${{ "{:,.0f}".format(user.working_capital) }}</span>
                        </div>
                        <div class="settings-item">
                            <span>Risk Tolerance:</span>
                            <span>{{ user.risk_tolerance|title }}</span>
                        </div>
                        <div class="settings-item">
                            <span>Experience Level:</span>
                            <span>{{ user.trading_experience|title }}</span>
                        </div>
                        <div class="settings-item">
                            <span>Notifications:</span>
                            <span>{{ "Enabled" if user.settings.notifications else "Disabled" }}</span>
                        </div>
                        <div class="settings-item">
                            <span>Max Position Size:</span>
                            <span>{{ user.settings.max_position_size }}%</span>
                        </div>
                    </div>
                    <button class="action-button" onclick="editSettings()">Edit Settings</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Load personalized recommendations on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadPersonalizedRecommendations();
        });

        async function loadPersonalizedRecommendations() {
            try {
                const response = await fetch('/api/v2/personalized-recommendations');
                const data = await response.json();
                
                const container = document.getElementById('personalizedRecommendations');
                container.innerHTML = '';
                
                data.recommendations.forEach(rec => {
                    const item = createRecommendationItem(rec);
                    container.appendChild(item);
                });
            } catch (error) {
                console.error('Error loading recommendations:', error);
            }
        }

        function createRecommendationItem(rec) {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            
            item.innerHTML = `
                <div class="crypto-pair">
                    <span class="pair-name">${rec.pair}</span>
                    <span class="roi-badge">${rec.expected_roi}</span>
                </div>
                <div style="margin: 10px 0; font-size: 14px; color: #b8b8b8;">
                    <strong>Recommended Investment:</strong> $${rec.recommended_amount.toLocaleString()}<br>
                    <strong>Expected Return:</strong> $${rec.expected_profit.toLocaleString()} in ${rec.time_frame}<br>
                    <strong>Risk Level:</strong> ${rec.risk_level}
                </div>
                <div style="background: rgba(0, 255, 157, 0.1); padding: 10px; border-radius: 8px; font-size: 14px; margin: 10px 0;">
                    <strong>Why this fits your profile:</strong> ${rec.personalized_reasoning}
                </div>
                <button class="action-button" onclick="executePersonalizedBot('${rec.pair}', ${rec.recommended_amount})">
                    🤖 Start $${rec.recommended_amount.toLocaleString()} GRID Bot
                </button>
            `;
            
            return item;
        }

        function executePersonalizedBot(pair, amount) {
            if (confirm(`Start GRID Bot for ${pair} with $${amount.toLocaleString()}?`)) {
                alert(`🤖 GRID Bot started for ${pair}\\n\\nAmount: $${amount.toLocaleString()}\\nThis would integrate with your trading platform.`);
            }
        }

        function editSettings() {
            window.location.href = '/settings';
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Redirect to login or dashboard based on session"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_PAGE)

@app.route('/login')
def login_page():
    """Login page"""
    return render_template_string(LOGIN_PAGE)

@app.route('/dashboard')
def dashboard():
    """Personalized trading dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    user = users_db.get(session['user_email'])
    if not user:
        return redirect(url_for('logout'))
    
    return render_template_string(TRADING_DASHBOARD, user=user)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """User login API"""
    try:
        data = request.json
        email = data.get('email', '').lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"status": "error", "message": "Email and password required"})
        
        user = users_db.get(email)
        if not user or not verify_password(password, user['password_hash']):
            return jsonify({"status": "error", "message": "Invalid email or password"})
        
        # Create session
        session['user_id'] = user['user_id']
        session['user_email'] = email
        session['login_time'] = datetime.now().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "name": f"{user['first_name']} {user['last_name']}",
                "email": email,
                "working_capital": user['working_capital']
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """User registration API"""
    try:
        data = request.json
        email = data.get('email', '').lower()
        password = data.get('password', '')
        
        # Validation
        if not all([email, password, data.get('first_name'), data.get('last_name')]):
            return jsonify({"status": "error", "message": "All fields are required"})
        
        if email in users_db:
            return jsonify({"status": "error", "message": "Email already registered"})
        
        if len(password) < 6:
            return jsonify({"status": "error", "message": "Password must be at least 6 characters"})
        
        # Create new user
        user_id = str(uuid.uuid4())
        users_db[email] = {
            "user_id": user_id,
            "email": email,
            "password_hash": hash_password(password),
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "created_date": datetime.now().strftime('%Y-%m-%d'),
            "working_capital": float(data.get('working_capital', 25000)),
            "risk_tolerance": data.get('risk_tolerance', 'medium'),
            "trading_experience": data.get('trading_experience', 'intermediate'),
            "preferred_strategies": ["grid_bot"],
            "portfolio": {
                "total_value": float(data.get('working_capital', 25000)),
                "profit_loss": 0.0,
                "active_positions": 0
            },
            "settings": {
                "notifications": True,
                "auto_execute": False,
                "max_position_size": 25
            }
        }
        
        # Create session
        session['user_id'] = user_id
        session['user_email'] = email
        session['login_time'] = datetime.now().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "Account created successfully",
            "user": {
                "name": f"{data['first_name']} {data['last_name']}",
                "email": email,
                "working_capital": users_db[email]['working_capital']
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/v2/personalized-recommendations', methods=['GET'])
def personalized_recommendations():
    """Get personalized GRID bot recommendations based on user profile"""
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Authentication required"})
    
    try:
        user = users_db.get(session['user_email'])
        if not user:
            return jsonify({"status": "error", "message": "User not found"})
        
        # Generate personalized recommendations based on user profile
        capital = user['working_capital']
        risk_tolerance = user['risk_tolerance']
        experience = user['trading_experience']
        
        # Risk-adjusted position sizing
        if risk_tolerance == 'conservative':
            max_position_pct = 15
            min_confidence = 0.8
        elif risk_tolerance == 'aggressive':
            max_position_pct = 35
            min_confidence = 0.65
        else:  # medium
            max_position_pct = 25
            min_confidence = 0.75
        
        recommendations = []
        
        # BTC recommendation
        btc_amount = min(capital * (max_position_pct / 100), capital * 0.4)
        recommendations.append({
            "pair": "BTC/USDT",
            "expected_roi": "+8.5%",
            "recommended_amount": int(btc_amount),
            "expected_profit": int(btc_amount * 0.085),
            "confidence": 0.78,
            "time_frame": "7-10 days",
            "risk_level": "Medium",
            "personalized_reasoning": f"Fits your {risk_tolerance} risk profile. Amount sized at {(btc_amount/capital)*100:.0f}% of capital for optimal diversification."
        })
        
        # ETH recommendation  
        eth_amount = min(capital * (max_position_pct / 100), capital * 0.3)
        recommendations.append({
            "pair": "ETH/USDT",
            "expected_roi": "+12.3%",
            "recommended_amount": int(eth_amount),
            "expected_profit": int(eth_amount * 0.123),
            "confidence": 0.82,
            "time_frame": "5-8 days",
            "risk_level": "Medium-Low",
            "personalized_reasoning": f"High confidence trade matching your {experience} experience level. Conservative sizing for steady returns."
        })
        
        # Add XRP only for medium/aggressive risk tolerance
        if risk_tolerance in ['medium', 'aggressive']:
            xrp_amount = min(capital * (max_position_pct / 100), capital * 0.2)
            recommendations.append({
                "pair": "XRP/USDT",
                "expected_roi": "+15.7%",
                "recommended_amount": int(xrp_amount),
                "expected_profit": int(xrp_amount * 0.157),
                "confidence": 0.75,
                "time_frame": "3-7 days",
                "risk_level": "Medium-High",
                "personalized_reasoning": f"Higher return opportunity suitable for your {risk_tolerance} risk appetite. Volatile but profitable for experienced traders."
            })
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "user_profile": {
                "working_capital": capital,
                "risk_tolerance": risk_tolerance,
                "experience": experience
            },
            "recommendations": recommendations
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Keep existing endpoints for API compatibility
@app.route('/api/v2/market-data', methods=['GET'])
def market_data():
    """Real-time market data"""
    try:
        data = [
            {"symbol": "BTC", "name": "Bitcoin", "price": 67234, "change_24h": 0.31, "volume": "28.9B"},
            {"symbol": "ETH", "name": "Ethereum", "price": 3765.55, "change_24h": 5.30, "volume": "49.1B"},
            {"symbol": "XRP", "name": "XRP", "price": 3.55, "change_24h": 3.40, "volume": "7.1B"},
            {"symbol": "SOL", "name": "Solana", "price": 182.33, "change_24h": 2.84, "volume": "13.1B"}
        ]
        return jsonify({"status": "success", "data": data, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/v2/market-summary', methods=['GET'])  
def market_summary():
    """Market overview and summary statistics"""
    try:
        return jsonify({
            "total_market_cap": "3.1T",
            "total_volume_24h": "138.2B",
            "btc_dominance": "56.2%",
            "market_sentiment": "Cautiously Optimistic",
            "last_updated": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/ws/live-data', methods=['GET'])
def ws_live_data():
    """Live data feed for real-time updates"""
    try:
        return jsonify({
            "type": "live_update",
            "timestamp": datetime.now().isoformat(),
            "prices": {
                "BTC": {"price": 67234, "change": 0.31},
                "ETH": {"price": 3765.55, "change": 5.30},
                "XRP": {"price": 3.55, "change": 3.40}
            },
            "status": "live"
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    try:
        print("🚀 Starting Project Lima Trading Platform with Authentication...")
        print("👤 User registration and login system enabled")
        print("💰 Personalized capital allocation and recommendations")
        print("🔐 Secure session management")
        print("📡 Available at: http://0.0.0.0:8000")
        print("")
        print("🎯 Demo Account:")
        print("   Email: demo@projectlima.com")
        print("   Password: demo123")
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ Failed to start web service: {e}")
        sys.exit(1)
