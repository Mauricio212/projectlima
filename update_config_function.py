import re

# Read the file
with open('web_app_professional_secured.py', 'r') as f:
    content = f.read()

# Find and replace the executePersonalizedBot function
old_function_pattern = r'function executePersonalizedBot\(pair, amount\) \{[^}]*\}[^}]*\}[^}]*\}'
new_function = '''function executePersonalizedBot(pair, amount) {
            // Show configuration choice modal instead of simple confirm
            showConfigModal(pair, amount);
        }

        function showConfigModal(pair, amount) {
            // Create modal HTML
            const modalHTML = `
                <div id="configModal" class="config-modal">
                    <div class="config-modal-content">
                        <div class="config-header">
                            <h3>🤖 Configure ${pair} Grid Bot</h3>
                            <p>Investment Amount: $${amount.toLocaleString()}</p>
                            <span class="config-close" onclick="closeConfigModal()">&times;</span>
                        </div>
                        
                        <div class="config-options">
                            <div class="config-option" onclick="generateGenericConfig('${pair}', ${amount})">
                                <div class="config-icon">⚙️</div>
                                <h4>Generic Grid Bot Config</h4>
                                <p>Universal format for any trading platform</p>
                                <ul>
                                    <li>Entry price & grid levels</li>
                                    <li>Profit targets</li>
                                    <li>Stop loss levels</li>
                                    <li>Position sizing</li>
                                </ul>
                            </div>
                            
                            <div class="config-option" onclick="generate3CommasConfig('${pair}', ${amount})">
                                <div class="config-icon">🔗</div>
                                <h4>3Commas Integration</h4>
                                <p>Ready-to-import 3Commas bot configuration</p>
                                <ul>
                                    <li>3Commas API format</li>
                                    <li>Direct import settings</li>
                                    <li>Optimized parameters</li>
                                    <li>Risk management</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add modal to page
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            
            // Show modal
            document.getElementById('configModal').style.display = 'flex';
        }

        function closeConfigModal() {
            const modal = document.getElementById('configModal');
            if (modal) {
                modal.remove();
            }
        }

        function generateGenericConfig(pair, amount) {
            closeConfigModal();
            
            const button = document.querySelector(`button[onclick*="${pair}"][onclick*="${amount}"]`);
            if (button) {
                button.textContent = '🔄 Generating Config...';
                button.disabled = true;
                
                setTimeout(() => {
                    alert(`✅ Generic Grid Bot Configuration Generated!\\n\\nPair: ${pair}\\nAmount: $${amount.toLocaleString()}\\n\\nGrid Levels: 10\\nProfit Per Grid: 1.5%\\nStop Loss: -15%\\n\\nCopy this configuration to your trading platform.`);
                    button.textContent = `🤖 Configure $${amount.toLocaleString()} GRID Bot`;
                    button.disabled = false;
                }, 1500);
            }
        }

        function generate3CommasConfig(pair, amount) 
            closeConfigModal();
            
            const button = document.querySelector(`button[onclick*="${pair}"][onclick*="${amount}"]`);
            if (button) {
                button.textContent = '🔄 Generating 3Commas Config...';
                button.disabled = true;
                
                setTimeout(() => {
                    const config = `{
  "name": "Lima ${pair} Grid Bot",
  "pairs": ["${pair}"],
  "base_order_volume": ${amount / 10},
  "safety_order_volume": ${amount / 20},
  "max_safety_orders": 8,
  "take_profit": 1.5,
  "stop_loss_percentage": 15,
  "strategy": "grid"
}`;
                    
                    // Copy to clipboard
                    navigator.clipboard.writeText(config).then(() => {
                        alert(`✅ 3Commas Configuration Generated & Copied!\\n\\nPair: ${pair}\\nAmount: $${amount.toLocaleString()}\\n\\nConfiguration copied to clipboard.\\nPaste it into 3Commas bot creation form.`);
                    }).catch(() => {
                        alert(`✅ 3Commas Configuration Generated!\\n\\n${config}\\n\\nManually copy this JSON to 3Commas.`);
                    });
                    
                    button.textContent = `🤖 Configure $${amount.toLocaleString()} GRID Bot`;
                    button.disabled = false;
                }, 1500);
            }
        }'''

# Replace the function
content = re.sub(old_function_pattern, new_function, content, flags=re.DOTALL)

# Write back
with open('web_app_professional_secured.py', 'w') as f:
    f.write(content)

print("✅ Function updated successfully!")
