from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(title="Project Lima API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class AnalysisRequest(BaseModel):
    ticker: Optional[str] = None
    message: Optional[str] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except:
            self.disconnect(websocket)

manager = ConnectionManager()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    try:
        with open("static/index.html") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>Project Lima Backend Running! Please create static/index.html</h1>")

@app.get("/health")
async def health_check():
    return {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "tiers": {
            "tier1_infrastructure": {"status": "online"},
            "tier2_data_ingestion": {"status": "online"},
            "tier3_config_generator": {"status": "online"},
            "tier4_decision_engine": {"status": "online"},
            "tier5_interaction": {"status": "online"}
        }
    }

@app.post("/analyze")
async def analyze_ticker(request: AnalysisRequest):
    ticker = request.ticker
    message = request.message
    
    if not ticker and not message:
        raise HTTPException(status_code=400, detail="Either ticker or message must be provided")
    
    # Simulate analysis
    await asyncio.sleep(2)
    
    return {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "analysis": {
            "components": {
                "technical": {"recommendation": "BUY"},
                "sentiment": {"recommendation": "BULLISH"},
                "rumor": {"recommendation": "NEUTRAL"},
                "factors": {"recommendation": "NEUTRAL"}
            },
            "final_recommendation": "BUY",
            "confidence_score": 0.85,
            "trading_strategy": "GRID_TRADING"
        },
        "recommendation": "BUY",
        "confidence_score": 0.85,
        "trading_strategy": "GRID_TRADING"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "analyze":
                ticker = message.get("ticker")
                
                # Send analysis updates
                components = ["Technical Analysis", "Sentiment Analysis", "Rumor Analysis", "Other Factors"]
                
                for component in components:
                    await manager.send_personal_message({
                        "type": "analysis_update",
                        "content": {
                            "component": component,
                            "status": "Processing..."
                        }
                    }, websocket)
                    await asyncio.sleep(1)
                    
                    await manager.send_personal_message({
                        "type": "analysis_update",
                        "content": {
                            "component": component,
                            "status": "Complete - BUY"
                        }
                    }, websocket)
                
                # Send final result
                await manager.send_personal_message({
                    "type": "final_result",
                    "content": {
                        "ticker": ticker,
                        "analysis": {
                            "components": {
                                "technical": {"recommendation": "BUY"},
                                "sentiment": {"recommendation": "BULLISH"},
                                "rumor": {"recommendation": "NEUTRAL"},
                                "factors": {"recommendation": "NEUTRAL"}
                            },
                            "final_recommendation": "BUY",
                            "confidence_score": 0.85,
                            "trading_strategy": "GRID_TRADING"
                        }
                    }
                }, websocket)
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
