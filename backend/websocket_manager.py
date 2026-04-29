from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        # Dictionary to store connections by site_id
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, site_id: int):
        """Accept a WebSocket connection and add to site's connections"""
        await websocket.accept()
        
        if site_id not in self.active_connections:
            self.active_connections[site_id] = []
        
        self.active_connections[site_id].append(websocket)
        logger.info(f"WebSocket connected for site {site_id}. Total connections: {len(self.active_connections[site_id])}")
    
    def disconnect(self, websocket: WebSocket, site_id: int):
        """Remove a WebSocket connection"""
        if site_id in self.active_connections:
            self.active_connections[site_id].remove(websocket)
            logger.info(f"WebSocket disconnected for site {site_id}. Remaining connections: {len(self.active_connections[site_id])}")
            
            # Clean up empty lists
            if not self.active_connections[site_id]:
                del self.active_connections[site_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        await websocket.send_text(message)
    
    async def broadcast_to_site(self, site_id: int, message: dict):
        """Broadcast a message to all connections for a specific site"""
        if site_id in self.active_connections:
            disconnected = []
            
            for connection in self.active_connections[site_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to connection: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected connections
            for connection in disconnected:
                self.disconnect(connection, site_id)
    
    async def broadcast_pageview(self, site_id: int, data: dict):
        """Broadcast a new pageview to all site connections"""
        message = {
            "type": "pageview",
            "data": data,
            "timestamp": data.get("created_at")
        }
        await self.broadcast_to_site(site_id, message)
    
    async def broadcast_event(self, site_id: int, data: dict):
        """Broadcast a new event to all site connections"""
        message = {
            "type": "event",
            "data": data,
            "timestamp": data.get("created_at")
        }
        await self.broadcast_to_site(site_id, message)
    
    def get_connection_count(self, site_id: int) -> int:
        """Get the number of active connections for a site"""
        return len(self.active_connections.get(site_id, []))


# Global connection manager instance
manager = ConnectionManager()
