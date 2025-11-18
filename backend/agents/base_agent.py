from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """Simple agent base class."""

    @abstractmethod
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
