import asyncio
import logging
from typing import Dict, Any, List
from agents.planner_agent import PlannerAgent
from agents.availability_agent import AvailabilityAgent
from agents.validation_agent import ValidationAgent
from agents.booking_agent import BookingAgent
from agents.payment_agent import PaymentAgent

logger = logging.getLogger(__name__)

class SimpleAgentSystem:
    def __init__(self):
        self.planner = PlannerAgent()
        self.availability = AvailabilityAgent()
        self.validator = ValidationAgent()
        self.booker = BookingAgent()
        self.payment = PaymentAgent()
        # in-memory stores
        self.tentatives = {}  # tentative_id -> details
        self.bookings = {}  # pnr -> details

    async def discovery_flow(self, query: Dict[str, Any], client_send):
        logger.info("Starting discovery flow for query: %s", query)
        # 1) Planner
        planner_res = await self.planner.handle({"query": query})
        options = planner_res.get("options", [])
        await client_send({"stage": "options", "options": options})
        # 2) Availability
        av_res = await self.availability.handle({"options": options})
        availability = av_res.get("availability", {})
        await client_send({"stage": "availability", "availability": availability})
        # 3) Validation
        val_res = await self.validator.handle({"availability": availability, "user_prefs": query.get("user_prefs", {}), "options": options})
        validated = val_res.get("validated_options", [])
        # enrich validated with option details for client convenience
        validated_with_details = []
        for v in validated:
            for o in options:
                if o["id"] == v["id"]:
                    validated_with_details.append({**v, **o})
        await client_send({"stage": "validated", "validated": validated_with_details})
        return validated_with_details

    async def reserve_tentative(self, option_id: str, pax: Dict[str, Any], client_send):
        logger.info("Reserving tentative for option %s", option_id)
        res = await self.booker.handle({"option_id": option_id, "pax": pax})
        tentative_id = res.get("tentative_id")
        self.tentatives[tentative_id] = {"option_id": option_id, "pax": pax}
        await client_send({"stage": "tentative_reserved", "tentative_id": tentative_id})
        return tentative_id

    async def process_payment_and_confirm(self, tentative_id: str, payment_info: Dict[str, Any], client_send):
        logger.info("Processing payment for tentative %s", tentative_id)
        if tentative_id not in self.tentatives:
            await client_send({"stage": "error", "message": "tentative not found"})
            return
        pay_res = await self.payment.handle({"tentative_id": tentative_id, "payment_info": payment_info})
        if pay_res.get("status") != "success":
            await client_send({"stage": "payment_failed", "reason": "declined"})
            # Cancel tentative in real system
            return {"status": "failed"}
        txn_id = pay_res.get("txn_id")
        # Simulate booking confirmation with provider
        booking_pnr = f"PNR{txn_id[-6:]}" if txn_id else "PNR-DEMO"
        booking = {"pnr": booking_pnr, "tentative_id": tentative_id, "txn_id": txn_id, "status": "confirmed"}
        self.bookings[booking_pnr] = booking
        # cleanup tentative
        self.tentatives.pop(tentative_id, None)
        await client_send({"stage": "booked", "booking": booking})
        return booking
