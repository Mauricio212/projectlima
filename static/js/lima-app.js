// Project Lima - Real-time Web Application

class LimaApp {
    constructor() {
        this.ws = null;
        this.initWebSocket();
        this.loadInitialData();
        this.startDataRefresh();
    }

    initWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws/live-data`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateUI(data);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket closed, attempting to reconnect...');
            setTimeout(() => this.initWebSocket(), 5000);
        };
    }

    async loadInitialData() {
        try {
            // Load market data
            const marketResponse = await axios.get('/api/v2/market-data');
            this.updateMarketData(marketResponse.data);
            
            // Load market summary
            const summaryResponse = await axios.get('/api/v2/market-summary');
            this.updateMarketSummary(summaryResponse.data);
            
            // Load analysis data
            const analysisResponse = await axios.get('/api/v2/grid-analysis');
            this.updateAnalysisData(analysisResponse.data);
            
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    updateMarketData(response) {
        if (response.status === 'success' && response.data) {
            this.updateTicker(response.data);
            
            // Update last update time
            const lastUpdate = new Date(response.timestamp).toLocaleTimeString();
            document.getElementById('lastUpdate').textContent = lastUpdate;
        }
    }

    updateTicker(cryptoData) {
        const tickerContainer = document.getElementById('tickerContainer');
        
        const tickerHTML = cryptoData.slice(0, 10).map(crypto => `
            <div class="ticker-item">
                <span class="ticker-symbol">${crypto.symbol}</span>
                <span class="ticker-price">$${crypto.price.toFixed(2)}</span>
                <span class="ticker-change ${crypto.change_24h >= 0 ? 'positive' : 'negative'}">
                    ${crypto.change_24h >= 0 ? '+' : ''}${crypto.change_24h.toFixed(2)}%
                </span>
            </div>
        `).join('');
        
        tickerContainer.innerHTML = tickerHTML;
    }

    updateMarketSummary(response) {
        if (response.status === 'success' && response.summary) {
            const summary = response.summary;
            
            // Update market stats
            document.getElementById('totalMarketCap').textContent = 
                `$${(summary.total_market_cap / 1e12).toFixed(1)}T`;
            
            document.getElementById('trendingUp').textContent = summary.trending_up;
            document.getElementById('trendingDown').textContent = summary.trending_down;
            
            document.getElementById('marketSentiment').textContent = summary.market_sentiment;
            
            // Update top performers
            if (summary.top_gainers && summary.top_gainers.length > 0) {
                const topGainer = summary.top_gainers[0];
                document.getElementById('topGainer').innerHTML = `
                    <span class="symbol">${topGainer.symbol}</span>
                    <span class="change">+${topGainer.change_24h.toFixed(2)}%</span>
                `;
            }
            
            if (summary.top_losers && summary.top_losers.length > 0) {
                const topLoser = summary.top_losers[0];
                document.getElementById('topLoser').innerHTML = `
                    <span class="symbol">${topLoser.symbol}</span>
                    <span class="change">${topLoser.change_24h.toFixed(2)}%</span>
                `;
            }
        }
    }

    updateAnalysisData(response) {
        if (response.status === 'success' && response.recommendations) {
            const recommendations = response.recommendations;
            
            // Update GRID ROI
            const gridRec = recommendations.find(r => r.strategy === 'GRID Trading');
            if (gridRec) {
                document.getElementById('gridROI').textContent = gridRec.expected_roi;
            }
            
            // Update HOLD ROI
            const holdRec = recommendations.find(r => r.strategy === 'HOLD Strategy');
            if (holdRec) {
                document.getElementById('holdROI').textContent = holdRec.expected_roi;
            }
        }
    }

    updateUI(data) {
        if (data.type === 'market_update' && data.data) {
            // Update with real-time data
            if (data.data.crypto_prices) {
                this.updateTicker(data.data.crypto_prices);
            }
            
            if (data.data.market_summary) {
                this.updateMarketSummary({status: 'success', summary: data.data.market_summary});
            }
        }
    }

    startDataRefresh() {
        // Refresh data every 60 seconds
        setInterval(() => {
            this.loadInitialData();
        }, 60000);
    }
}

// Global functions
async function runAnalysis() {
    try {
        const response = await axios.get('/api/v2/run-analysis');
        
        if (response.data.status === 'started') {
            alert('✅ GRID vs HOLD analysis started! Results will be available shortly.');
            
            // Refresh analysis data after 30 seconds
            setTimeout(() => {
                window.location.reload();
            }, 30000);
        }
    } catch (error) {
        alert('❌ Error starting analysis: ' + error.message);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.limaApp = new LimaApp();
});
