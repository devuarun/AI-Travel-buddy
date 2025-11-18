import asyncio
from typing import Any, Dict, List
from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        query = context.get("query", {})
        origin = query.get("origin")
        destination = query.get("destination")
        dates = query.get("dates", {})
        # Simulate call to search index / OTA / GDS
        await asyncio.sleep(0.5)
        options = [
            {"id": "opt-1", "price": 350, "route": [origin, destination], "legs": 1, "provider": "DemoAir"},
            {"id": "opt-2", "price": 410, "route": [origin, "YYZ", destination], "legs": 2, "provider": "DemoAir+Train"},
            {"id": "opt-3", "price": 380, "route": [origin, destination], "legs": 1, "provider": "OtherAir"},
        ]
        # naive ranking by price
        ranked = sorted(options, key=lambda o: o["price"])
        return {"type": "options", "options": ranked}
