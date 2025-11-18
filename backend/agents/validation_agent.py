import asyncio
from typing import Any, Dict, List
from .base_agent import BaseAgent

class ValidationAgent(BaseAgent):
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        availability = context.get("availability", {})
        prefs = context.get("user_prefs", {})
        validated = []
        # Example rules: budget cap in prefs, max legs
        budget = prefs.get("max_price")
        max_legs = prefs.get("max_legs")
        for opt_id, av in availability.items():
            ok = True
            # mock look up option details - in orchestrator we pass details if needed
            # For demo, assume ok
            if budget is not None:
                # naive check: parse price from opt id mapping if provided in context
                pass
            if ok:
                validated.append({"id": opt_id, "ok": True})
            await asyncio.sleep(0.05)
        return {"type": "validated", "validated_options": validated}
