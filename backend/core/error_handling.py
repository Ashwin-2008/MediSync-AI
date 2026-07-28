import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Prevents cascading failures when LLM providers or databases go down."""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout_sec: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.failures = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED" # CLOSED, OPEN, HALF_OPEN

    def _update_state(self):
        if self.state == "OPEN":
            if (time.time() - self.last_failure_time) > self.recovery_timeout_sec:
                self.state = "HALF_OPEN"
                logger.info("Circuit Breaker transitioned to HALF_OPEN")

    async def execute(self, func: Callable, fallback: Callable, *args, **kwargs) -> Any:
        self._update_state()
        
        if self.state == "OPEN":
            logger.warning("Circuit Breaker OPEN. Using fallback.")
            return await fallback(*args, **kwargs)
            
        try:
            result = await func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failures = 0
                logger.info("Circuit Breaker transitioned to CLOSED (Recovered)")
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            logger.error(f"Execution failed. Failure count: {self.failures}. Error: {e}")
            
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
                logger.critical("Circuit Breaker transitioned to OPEN")
                
            return await fallback(*args, **kwargs)

# Singleton instances for major external dependencies
llm_circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout_sec=60)
vector_db_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout_sec=30)
