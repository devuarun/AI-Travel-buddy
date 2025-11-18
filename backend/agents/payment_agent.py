import asyncio
from typing import Any, Dict
from .base_agent import BaseAgent
import random, uuid

class PaymentAgent(BaseAgent):
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        tentative_id = context.get("tentative_id")
        payment_info = context.get("payment_info", {})
        # Simulate external PSP call
        await asyncio.sleep(0.4)
        success = random.random() > 0.1  # 90% success in demo
        txn_id = None
        if success:
            txn_id = f"txn-{uuid.uuid4().hex[:10]}"
            status = "success"
        else:
            status = "failure"
        return {"type": "payment_result", "status": status, "txn_id": txn_id}
