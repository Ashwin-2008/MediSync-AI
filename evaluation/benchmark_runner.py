import asyncio
import time
import json
import logging
from .agent_scorecard import agent_scorecard

logger = logging.getLogger(__name__)

class BenchmarkRunner:
    """Executes load tests and computes costs."""
    
    def __init__(self, cost_per_1k_tokens: float = 0.0015):
        self.cost_per_1k = cost_per_1k_tokens

    async def run_load_test(self, concurrent_users: int = 10, iterations: int = 5):
        logger.info(f"Starting Benchmark: {concurrent_users} users, {iterations} iterations.")
        start_time = time.time()
        
        total_tasks = concurrent_users * iterations
        
        # Simulate load
        async def mock_workflow():
            await asyncio.sleep(0.2) # Simulate network/processing
            agent_scorecard.record_execution(
                agent_name="DiagnosisAgent",
                success=True,
                latency_ms=250.0,
                tokens=1500,
                requires_review=False
            )
            return True

        tasks = [mock_workflow() for _ in range(total_tasks)]
        await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        report = agent_scorecard.get_report()
        total_tokens = sum(s["total_tokens"] for s in agent_scorecard.metrics.values())
        cost = (total_tokens / 1000) * self.cost_per_1k
        
        results = {
            "test_duration_sec": round(duration, 2),
            "total_requests": total_tasks,
            "requests_per_sec": round(total_tasks / duration, 2),
            "estimated_cost_usd": round(cost, 4),
            "agent_metrics": report
        }
        
        # Write to JSON
        with open("benchmark_report.json", "w") as f:
            json.dump(results, f, indent=2)
            
        logger.info("Benchmark complete. Wrote benchmark_report.json")
        return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    runner = BenchmarkRunner()
    asyncio.run(runner.run_load_test())
