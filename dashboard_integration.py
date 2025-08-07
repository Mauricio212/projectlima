# Add this to your web application to populate the GRID Bot Recommendations

@app.route('/api/dashboard/recommendations')
@limiter.limit("30 per minute")
def dashboard_recommendations():
    try:
        import pandas as pd
        import json
        from datetime import datetime
        
        # Get latest pipeline results
        selected_tokens = pd.read_csv('grid_hold_output/step_3_3_selected_tokens.csv')
        roi_data = pd.read_csv('grid_hold_output/step_3_2_token_roi.csv')
        
        recommendations = []
        for _, token in selected_tokens.iterrows():
            # Find matching ROI data
            roi_info = roi_data[roi_data['symbol'] == token['symbol']].iloc[0]
            
            recommendations.append({
                'symbol': token['symbol'],
                'current_price': float(token.get('price', 0)),
                'grid_roi': float(roi_info['grid_roi']),
                'hold_roi': float(roi_info['hold_roi']),
                'roi_advantage': float(roi_info['grid_roi'] - roi_info['hold_roi']),
                'recommended_allocation': f"${min(12500, 50000 * 0.25):,.0f}",  # 25% max position
                'confidence': 'High' if roi_info['grid_roi'] > roi_info['hold_roi'] + 5 else 'Medium',
                'setup_time': '2-3 minutes',
                'risk_level': 'Medium'
            })
        
        return jsonify({
            'status': 'success',
            'recommendations': recommendations,
            'last_updated': datetime.now().isoformat(),
            'total_recommendations': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user info
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template_string(DASHBOARD_HTML, user=user)
