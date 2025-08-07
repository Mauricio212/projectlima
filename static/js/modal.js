function openConfigureModal(pair, amount) {
    console.log("🔧 Opening configure modal for", pair, amount);
    
    const existingModal = document.getElementById('configureModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modalHTML = `
        <div id="configureModal" style="
            display: flex;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            justify-content: center;
            align-items: center;
        ">
            <div style="
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 1px solid rgba(0, 255, 157, 0.3);
                border-radius: 15px;
                padding: 30px;
                max-width: 600px;
                width: 90%;
                text-align: center;
            ">
                <h3 style="color: #00ff9d; margin-bottom: 15px; font-size: 24px;">
                    🤖 Configure ${pair} Grid Bot
                </h3>
                <p style="color: #b8b8b8; margin-bottom: 30px; font-size: 16px;">
                    Investment Amount: $${amount.toLocaleString()}
                </p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
                    <div onclick="showGenericConfig('${pair}', ${amount})" style="
                        background: rgba(0, 255, 157, 0.1);
                        border: 1px solid rgba(0, 255, 157, 0.3);
                        border-radius: 12px;
                        padding: 25px;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    " onmouseover="this.style.transform='translateY(-3px)'; this.style.borderColor='#00ff9d';" 
                       onmouseout="this.style.transform='translateY(0px)'; this.style.borderColor='rgba(0, 255, 157, 0.3)';">
                        <div style="font-size: 40px; margin-bottom: 15px;">⚙️</div>
                        <h4 style="color: #00ff9d; margin-bottom: 10px;">Generic Configuration</h4>
                        <p style="color: #b8b8b8; font-size: 14px;">Universal grid settings for any platform</p>
                    </div>
                    
                    <div onclick="show3CommasConfig('${pair}', ${amount})" style="
                        background: rgba(0, 255, 157, 0.1);
                        border: 1px solid rgba(0, 255, 157, 0.3);
                        border-radius: 12px;
                        padding: 25px;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    " onmouseover="this.style.transform='translateY(-3px)'; this.style.borderColor='#00ff9d';" 
                       onmouseout="this.style.transform='translateY(0px)'; this.style.borderColor='rgba(0, 255, 157, 0.3)';">
                        <div style="font-size: 40px; margin-bottom: 15px;">🔗</div>
                        <h4 style="color: #00ff9d; margin-bottom: 10px;">3Commas Configuration</h4>
                        <p style="color: #b8b8b8; font-size: 14px;">Ready-to-import 3Commas settings</p>
                    </div>
                </div>
                
                <button onclick="closeConfigureModal()" style="
                    background: rgba(255, 107, 107, 0.2);
                    border: 1px solid rgba(255, 107, 107, 0.5);
                    color: #ff6b6b;
                    padding: 12px 24px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 14px;
                ">Cancel</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

function closeConfigureModal() {
    const modal = document.getElementById('configureModal');
    if (modal) {
        modal.remove();
    }
}

function showGenericConfig(pair, amount) {
    closeConfigureModal();
    
    // Create expanded configuration modal
    const configHTML = `
        <div id="configureModal" style="
            display: flex;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            justify-content: center;
            align-items: center;
        ">
            <div style="
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 1px solid rgba(0, 255, 157, 0.3);
                border-radius: 15px;
                padding: 30px;
                max-width: 800px;
                width: 95%;
                max-height: 90vh;
                overflow-y: auto;
            ">
                <h3 style="color: #00ff9d; margin-bottom: 20px; text-align: center; font-size: 24px;">
                    ⚙️ Generic Grid Bot Configuration
                </h3>
                <h4 style="color: #00ff9d; margin-bottom: 15px; text-align: center;">
                    ${pair} - $${amount.toLocaleString()} Investment
                </h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px;">
                    <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px;">
                        <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">🎯 Entry Parameters</h4>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Trading Pair:</span>
                            <span style="color: #00ff9d; font-weight: bold;">${pair}</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Total Investment:</span>
                            <span style="color: #00ff9d; font-weight: bold;">$${amount.toLocaleString()}</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Entry Range:</span>
                            <span style="color: #00ff9d; font-weight: bold;">Current Price ±5%</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Market Type:</span>
                            <span style="color: #00ff9d; font-weight: bold;">Spot Trading</span>
                        </div>
                    </div>
                    
                    <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px;">
                        <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">📊 Grid Settings</h4>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Grid Levels:</span>
                            <span style="color: #00ff9d; font-weight: bold;">10</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Profit Per Grid:</span>
                            <span style="color: #00ff9d; font-weight: bold;">1.5%</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Position Size per Grid:</span>
                            <span style="color: #00ff9d; font-weight: bold;">$${(amount/10).toLocaleString()}</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Grid Type:</span>
                            <span style="color: #00ff9d; font-weight: bold;">Arithmetic</span>
                        </div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px;">
                    <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px;">
                        <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">🛡️ Risk Management</h4>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Stop Loss:</span>
                            <span style="color: #ff6b6b; font-weight: bold;">-15%</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Take Profit:</span>
                            <span style="color: #00ff9d; font-weight: bold;">+25%</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Max Drawdown:</span>
                            <span style="color: #ff6b6b; font-weight: bold;">20%</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Risk Level:</span>
                            <span style="color: #ffa500; font-weight: bold;">Medium</span>
                        </div>
                    </div>
                    
                    <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px;">
                        <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">⏱️ Execution Settings</h4>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Order Type:</span>
                            <span style="color: #00ff9d; font-weight: bold;">Limit Orders</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Time in Force:</span>
                            <span style="color: #00ff9d; font-weight: bold;">GTC (Good Till Cancel)</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Execution Time:</span>
                            <span style="color: #00ff9d; font-weight: bold;">24/7 Automated</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Estimated Duration:</span>
                            <span style="color: #00ff9d; font-weight: bold;">7-14 days</span>
                        </div>
                    </div>
                </div>
                
                <div style="background: rgba(0, 255, 157, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid rgba(0, 255, 157, 0.3);">
                    <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">📋 Setup Instructions</h4>
                    <ol style="color: #b8b8b8; text-align: left; padding-left: 20px; line-height: 1.6;">
                        <li>Copy these parameters to your trading platform</li>
                        <li>Set up ${amount/10} limit orders at 1.5% intervals</li>
                        <li>Configure stop-loss at -15% from entry</li>
                        <li>Set take-profit orders at +1.5% above each grid level</li>
                        <li>Enable 24/7 monitoring and execution</li>
                        <li>Monitor performance and adjust as needed</li>
                    </ol>
                </div>
                
                <div style="text-align: center; margin-top: 25px;">
                    <button onclick="copyGenericConfig('${pair}', ${amount})" style="
                        background: linear-gradient(45deg, #00ff9d, #00d4aa);
                        color: #000;
                        border: none;
                        padding: 15px 30px;
                        border-radius: 8px;
                        font-weight: bold;
                        cursor: pointer;
                        margin-right: 15px;
                        font-size: 16px;
                    ">📋 Copy Configuration</button>
                    
                    <button onclick="closeConfigureModal()" style="
                        background: rgba(255, 107, 107, 0.2);
                        border: 1px solid rgba(255, 107, 107, 0.5);
                        color: #ff6b6b;
                        padding: 15px 30px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 16px;
                    ">Close</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', configHTML);
}

function show3CommasConfig(pair, amount) {
    closeConfigureModal();
    
    const configHTML = `
        <div id="configureModal" style="
            display: flex;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            justify-content: center;
            align-items: center;
        ">
            <div style="
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 1px solid rgba(0, 255, 157, 0.3);
                border-radius: 15px;
                padding: 30px;
                max-width: 800px;
                width: 95%;
                max-height: 90vh;
                overflow-y: auto;
            ">
                <h3 style="color: #00ff9d; margin-bottom: 20px; text-align: center; font-size: 24px;">
                    🔗 3Commas Grid Bot Configuration
                </h3>
                <h4 style="color: #00ff9d; margin-bottom: 15px; text-align: center;">
                    ${pair} - $${amount.toLocaleString()} Investment
                </h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px;">
                    <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px;">
                        <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">🔧 Step 1: Grid Type Selection</h4>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Recommended Type:</span>
                            <span style="color: #00ff9d; font-weight: bold;">STABLE</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Alternative:</span>
                            <span style="color: #ffa500; font-weight: bold;">RISING</span>
                        </div>
                        <p style="color: #b8b8b8; font-size: 14px; margin-top: 10px;">Select STABLE for sideways markets, RISING for bullish trends</p>
                    </div>
                    
                    <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px;">
                        <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">📊 Step 2: Basic Settings</h4>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Exchange:</span>
                            <span style="color: #00ff9d; font-weight: bold;">Your Connected Exchange</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Market:</span>
                            <span style="color: #00ff9d; font-weight: bold;">USDT</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Pair:</span>
                            <span style="color: #00ff9d; font-weight: bold;">${pair}</span>
                        </div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px;">
                    <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px;">
                        <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">📈 Step 3: Grid Parameters</h4>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Grid Type:</span>
                            <span style="color: #00ff9d; font-weight: bold;">Geometric</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Investment:</span>
                            <span style="color: #00ff9d; font-weight: bold;">$${amount.toLocaleString()}</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Levels:</span>
                            <span style="color: #00ff9d; font-weight: bold;">20</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Amount Per Level:</span>
                            <span style="color: #00ff9d; font-weight: bold;">$${(amount/20).toLocaleString()}</span>
                        </div>
                    </div>
                    
                    <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px;">
                        <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">⚙️ Step 4: Advanced Options</h4>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Upper Stop Bot:</span>
                            <span style="color: #ff6b6b; font-weight: bold;">OFF</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Lower Stop Bot:</span>
                            <span style="color: #00ff9d; font-weight: bold;">ON</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Max Active Orders:</span>
                            <span style="color: #00ff9d; font-weight: bold;">20</span>
                        </div>
                        <div style="color: #fff; margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <span>Stop Loss:</span>
                            <span style="color: #ff6b6b; font-weight: bold;">-15%</span>
                        </div>
                    </div>
                </div>
                
                <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px; margin-bottom: 25px;">
                    <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">📝 Step 5: Bot Settings</h4>
                    <div style="color: #fff; margin-bottom: 15px; padding: 15px; background: rgba(0, 255, 157, 0.1); border-radius: 8px;">
                        <strong>Bot Name:</strong> <span style="color: #00ff9d;">Lima ${pair} Grid Bot</span>
                    </div>
                    <textarea readonly style="
                        width: 100%; 
                        height: 150px; 
                        background: rgba(0, 0, 0, 0.5); 
                        border: 1px solid rgba(0, 255, 157, 0.3); 
                        border-radius: 8px; 
                        color: #fff; 
                        padding: 15px; 
                        font-family: 'Courier New', monospace; 
                        font-size: 12px;
                        resize: vertical;
                    ">{
  "name": "Lima ${pair} Grid Bot",
  "pairs": ["${pair}"],
  "base_order_volume": ${amount / 20},
  "safety_order_volume": ${amount / 40},
  "max_safety_orders": 15,
  "safety_order_step_percentage": 2.5,
  "take_profit": 1.5,
  "stop_loss_percentage": 15,
  "strategy": "grid",
  "grid_lines": 20,
  "grid_type": "geometric"
}</textarea>
                </div>
                
                <div style="background: rgba(0, 255, 157, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid rgba(0, 255, 157, 0.3);">
                    <h4 style="color: #00ff9d; margin-bottom: 15px; font-size: 18px;">🔗 Setup Instructions</h4>
                    <ol style="color: #b8b8b8; text-align: left; padding-left: 20px; line-height: 1.6;">
                        <li>Copy the JSON configuration above</li>
                        <li>Log into your 3Commas account</li>
                        <li>Go to "Create Bot" → "Grid Bot"</li>
                        <li>Select your grid type (Stable/Rising)</li>
                        <li>Click "Import from JSON" or "Advanced Settings"</li>
                        <li>Paste the configuration and review settings</li>
                        <li>Connect your exchange and start the bot</li>
                    </ol>
                </div>
                
                <div style="text-align: center; margin-top: 25px;">
                    <button onclick="copy3CommasConfig('${pair}', ${amount})" style="
                        background: linear-gradient(45deg, #00ff9d, #00d4aa);
                        color: #000;
                        border: none;
                        padding: 15px 30px;
                        border-radius: 8px;
                        font-weight: bold;
                        cursor: pointer;
                        margin-right: 15px;
                        font-size: 16px;
                    ">📋 Copy JSON Config</button>
                    
                    <button onclick="window.open('https://3commas.io', '_blank')" style="
                        background: rgba(0, 123, 255, 0.8);
                        color: #fff;
                        border: none;
                        padding: 15px 30px;
                        border-radius: 8px;
                        font-weight: bold;
                        cursor: pointer;
                        margin-right: 15px;
                        font-size: 16px;
                    ">🔗 Open 3Commas</button>
                    
                    <button onclick="closeConfigureModal()" style="
                        background: rgba(255, 107, 107, 0.2);
                        border: 1px solid rgba(255, 107, 107, 0.5);
                        color: #ff6b6b;
                        padding: 15px 30px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 16px;
                    ">Close</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', configHTML);
}

function copyGenericConfig(pair, amount) {
    const config = `Generic Grid Bot Configuration

Pair: ${pair}
Investment: $${amount.toLocaleString()}

📊 Grid Settings:
- Grid Levels: 10
- Profit Per Grid: 1.5%
- Position Size: $${(amount/10).toLocaleString()} per grid
- Stop Loss: -15%
- Take Profit: +25%
- Grid Type: Arithmetic
- Entry Range: Current Price ±5%

🛡️ Risk Management:
- Max Drawdown: 20%
- Risk Level: Medium
- Order Type: Limit Orders
- Time in Force: GTC (Good Till Cancel)

⏱️ Execution:
- Execution Time: 24/7 Automated
- Estimated Duration: 7-14 days

📋 Setup Instructions:
1. Copy these parameters to your trading platform
2. Set up ${amount/10} limit orders at 1.5% intervals
3. Configure stop-loss at -15% from entry
4. Set take-profit orders at +1.5% above each grid level
5. Enable 24/7 monitoring and execution
6. Monitor performance and adjust as needed`;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(config).then(() => {
            alert('✅ Generic configuration copied to clipboard!');
        });
    } else {
        alert('📋 Configuration ready to copy:\n\n' + config);
    }
}

function copy3CommasConfig(pair, amount) {
    const config = `{
  "name": "Lima ${pair} Grid Bot",
  "pairs": ["${pair}"],
  "base_order_volume": ${amount / 20},
  "safety_order_volume": ${amount / 40},
  "max_safety_orders": 15,
  "safety_order_step_percentage": 2.5,
  "take_profit": 1.5,
  "stop_loss_percentage": 15,
  "strategy": "grid",
  "grid_lines": 20,
  "grid_type": "geometric"
}`;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(config).then(() => {
            alert('✅ 3Commas JSON configuration copied to clipboard!');
        });
    } else {
        alert('📋 3Commas Configuration:\n\n' + config);
    }
}
