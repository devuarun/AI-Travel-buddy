import asyncio
from typing import Any, Dict
from .base_agent import BaseAgent

class AvailabilityAgent(BaseAgent):
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        options = context.get("options", [])
        availability = {}
        # Simulate network calls for availability
        for opt in options:
            await asyncio.sleep(0.1)
            # simple mock: all options available, seats random
            availability[opt["id"]] = {"status": "available", "seats": 5}
        return {"type": "availability", "availability": availability}
