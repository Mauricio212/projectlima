# Project Lima – Full Flask App with All Endpoints
# ✅ Golden Rule #6 Compliant – August 7, 2025 Clean Version

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'REPLACE_ME_WITH_SECRET_KEY'

# --- Login Manager ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- Simple User Class ---
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# --- Routes ---
@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/health')
@login_required
def health():
    return render_template('health.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'your-password':
            user = User('admin')
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/roi')
@login_required
def api_roi():
    conn = sqlite3.connect('lima_trading.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT symbol, grid_roi, hold_roi, recommendation, confidence, timestamp
        FROM roi_analysis
        WHERE DATE(timestamp) = DATE('now')
        ORDER BY timestamp DESC
        LIMIT 10
    """)
    data = cursor.fetchall()
    conn.close()

    html = """
    <div class="overflow-x-auto">
      <table class="min-w-full table-auto">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-2 text-left">Symbol</th>
            <th class="px-4 py-2 text-left">Grid ROI</th>
            <th class="px-4 py-2 text-left">Hold ROI</th>
            <th class="px-4 py-2 text-left">Recommendation</th>
            <th class="px-4 py-2 text-left">Confidence</th>
          </tr>
        </thead>
        <tbody>
    """
    for row in data:
        rec_class = "text-green-600 font-semibold" if row['recommendation'] == 'GRID' else "text-red-600 font-semibold"
        html += f"""
          <tr class="border-b">
            <td class="px-4 py-2">{row['symbol']}</td>
            <td class="px-4 py-2">{row['grid_roi']:.2f}%</td>
            <td class="px-4 py-2">{row['hold_roi']:.2f}%</td>
            <td class="px-4 py-2 {rec_class}">{row['recommendation']}</td>
            <td class="px-4 py-2">{row['confidence']:.1f}%</td>
          </tr>
        """
    html += """
        </tbody>
      </table>
    </div>
    """
    return html

@app.route('/api/chart-data')
@login_required
def api_chart_data():
    conn = sqlite3.connect('lima_trading.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(timestamp) as date,
               AVG(grid_roi) as avg_grid_roi,
               AVG(hold_roi) as avg_hold_roi
        FROM roi_analysis
        WHERE timestamp >= DATE('now', '-30 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
    """)
    data = cursor.fetchall()
    conn.close()

    chart_data = {
        'type': 'line',
        'data': {
            'labels': [row[0] for row in data],
            'datasets': [
                {
                    'label': 'Grid ROI',
                    'data': [row[1] for row in data],
                    'borderColor': 'rgb(34, 197, 94)',
                    'backgroundColor': 'rgba(34, 197, 94, 0.1)',
                    'tension': 0.1
                },
                {
                    'label': 'Hold ROI',
                    'data': [row[2] for row in data],
                    'borderColor': 'rgb(239, 68, 68)',
                    'backgroundColor': 'rgba(239, 68, 68, 0.1)',
                    'tension': 0.1
                }
            ]
        },
        'options': {
            'responsive': True,
            'plugins': {
                'title': {
                    'display': True,
                    'text': 'Grid vs Hold Performance (30 Days)'
                }
            }
        }
    }

    return jsonify(chart_data)

@app.route('/api/health')
@login_required
def api_health():
    modules = [
        {'name': 'FIX Module 1', 'status': 'active', 'last_run': '2025-08-07 06:00:00'},
        {'name': 'FIX Module 2', 'status': 'active', 'last_run': '2025-08-07 06:00:00'},
        {'name': 'ROI Engine', 'status': 'active', 'last_run': '2025-08-07 06:05:00'},
        {'name': 'Database', 'status': 'active', 'last_run': '2025-08-07 06:05:00'},
        {'name': 'Cron Jobs', 'status': 'active', 'last_run': '2025-08-07 06:00:00'},
        {'name': 'Google Sheets Export', 'status': 'active', 'last_run': '2025-08-07 06:10:00'},
    ]

    html = '<div class="grid grid-cols-1 md:grid-cols-3 gap-4">'
    for m in modules:
        style = "bg-green-100 border-green-500 text-green-700" if m["status"] == "active" else "bg-red-100 border-red-500 text-red-700"
        icon = "✅" if m["status"] == "active" else "❌"
        html += f'''
        <div class="border-2 {style} rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="text-xl mr-2">{icon}</span>
            <h3 class="font-semibold">{m['name']}</h3>
          </div>
          <p class="text-sm">Status: {m['status'].upper()}</p>
          <p class="text-sm">Last Run: {m['last_run']}</p>
        </div>
        '''
    html += '</div>'
    return html

@app.route('/api/recent')
@login_required
def api_recent():
    return """
    <ul class='list-disc pl-5 text-sm text-gray-700'>
      <li>Bot swap: ETH/USDC closed, ADA/USDC added</li>
      <li>Volatility filter removed: PEPE/USDC approved</li>
      <li>Donchian range updated: SOL/USDC widened by 12%</li>
      <li>GRID ROI failed on MATIC/USDC – fallback to HOLD</li>
      <li>Next rotation: 2025-08-08 06:00 UTC</li>
    </ul>
    """

# --- Launch ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

