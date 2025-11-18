import asyncio
from typing import Any, Dict
from .base_agent import BaseAgent
import uuid

class BookingAgent(BaseAgent):
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        option_id = context.get("option_id")
        pax = context.get("pax", {})
        # Simulate tentative reservation call
        await asyncio.sleep(0.3)
        tentative_id = f"tent-{uuid.uuid4().hex[:8]}"
        # store minimal hold info in response
        return {"type": "tentative_reserved", "tentative_id": tentative_id, "option_id": option_id}
