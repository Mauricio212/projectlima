from flask import Flask, render_template_string, jsonify, session, redirect, url_for
import pandas as pd
import json
from datetime import datetime
import sqlite3

# Complete Dashboard HTML Template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Lima Pro - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
        }
        
        .navbar {
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 255, 157, 0.3);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .navbar-brand {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00ff9d;
        }
        
        .navbar-nav {
            display: flex;
            gap: 2rem;
        }
        
        .nav-link {
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-decoration: none;
            color: #b8b8b8;
            transition: all 0.3s ease;
        }
        
        .nav-link.active {
            background: rgba(0, 255, 157, 0.2);
            color: #00ff9d;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .premium-badge {
            background: linear-gradient(45deg, #00ff9d, #00d4aa);
            color: #000;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .welcome-section {
            margin-bottom: 2rem;
        }
        
        .welcome-title {
            font-size: 2.5rem;
            color: #00ff9d;
            margin-bottom: 0.5rem;
        }
        
        .welcome-subtitle {
            color: #b8b8b8;
            font-size: 1.1rem;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .metric-card {
            background: rgba(26, 26, 46, 0.8);
            border: 1px solid rgba(0, 255, 157, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #00ff9d;
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            color: #b8b8b8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-change {
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        
        .positive { color: #00ff9d; }
        .negative { color: #ff6b6b; }
        
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 2rem;
        }
        
        .recommendations-section {
            background: rgba(26, 26, 46, 0.8);
            border: 1px solid rgba(0, 255, 157, 0.3);
            border-radius: 16px;
            padding: 2rem;
        }
        
        .section-title {
            font-size: 1.5rem;
            color: #00ff9d;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .recommendations-list {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .recommendation-card {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 157, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .recommendation-card:hover {
            border-color: #00ff9d;
            transform: translateY(-2px);
        }
        
        .rec-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .token-symbol {
            font-size: 1.25rem;
            font-weight: bold;
            color: #ffffff;
        }
        
        .confidence-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .confidence-high {
            background: rgba(0, 255, 157, 0.2);
