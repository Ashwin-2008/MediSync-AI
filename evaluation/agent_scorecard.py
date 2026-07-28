import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AgentScorecard:
    """Tracks metrics and success rates for individual agents over time."""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}

    def record_execution(self, agent_name: str, success: bool, latency_ms: float, tokens: int, requires_review: bool):
        if agent_name not in self.metrics:
            self.metrics[agent_name] = {
                "total_runs": 0,
                "successes": 0,
                "human_reviews": 0,
                "total_latency_ms": 0.0,
                "total_tokens": 0
            }
            
        stats = self.metrics[agent_name]
        stats["total_runs"] += 1
        if success: stats["successes"] += 1
        if requires_review: stats["human_reviews"] += 1
        stats["total_latency_ms"] += latency_ms
        stats["total_tokens"] += tokens

    def get_report(self) -> Dict[str, Any]:
        report = {}
        for agent, stats in self.metrics.items():
            runs = stats["total_runs"]
            report[agent] = {
                "success_rate": f"{(stats['successes'] / runs) * 100:.1f}%" if runs else "0%",
                "review_rate": f"{(stats['human_reviews'] / runs) * 100:.1f}%" if runs else "0%",
                "avg_latency_ms": round(stats['total_latency_ms'] / runs, 2) if runs else 0,
                "avg_tokens": round(stats['total_tokens'] / runs, 0) if runs else 0
            }
        return report

agent_scorecard = AgentScorecard()
