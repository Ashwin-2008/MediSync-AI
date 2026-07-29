import asyncio
import logging
import uuid
import json
import time
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

# Hard ceiling for the entire workflow execution (seconds)
WORKFLOW_TIMEOUT = 120

# Keyword → agent routing table (no LLM call needed)
_KEYWORD_ROUTES: list[tuple[list[str], str]] = [
    (["diagnos", "symptom", "fever", "pain", "dizzy", "headache", "chest", "breath", "nausea", "vomit", "cough"], "diagnosis_agent"),
    (["treatment", "medic", "prescri", "drug", "therapy"],  "treatment_agent"),
    (["emergency", "urgent", "critical", "ambulance"],       "emergency_agent"),
    (["appointment", "schedule", "book", "slot"],            "appointment_agent"),
    (["lab", "test", "blood", "urine", "sample", "result"],  "lab_agent"),
    (["pharmacy", "dispens", "pill", "tablet"],              "pharmacy_agent"),
    (["bill", "invoice", "payment", "charge"],               "billing_agent"),
    (["insurance", "claim", "coverage", "policy"],           "insurance_agent"),
    (["intake", "register", "admit", "new patient"],         "intake_agent"),
]

def _route_by_keywords(payload: Dict[str, Any]) -> str:
    """Determine the target agent from payload keywords. No LLM call."""
    text = " ".join([
        str(payload.get("message", "")),
        str(payload.get("symptoms", "")),
        str(payload.get("type", "")),
    ]).lower()

    for keywords, agent_name in _KEYWORD_ROUTES:
        if any(kw in text for kw in keywords):
            return agent_name

    return "diagnosis_agent"  # safe default for clinical chat


class OrchestratorAIPlanner:
    def __init__(self):
        self.registered_agents: Dict[str, Any] = {}

    def register_agent(self, name: str, agent: Any):
        self.registered_agents[name] = agent
        logger.info("Orchestrator registered agent: %s", name)

    async def handle_request(
        self,
        db: AsyncSession,
        workflow_id: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        t0 = time.time()

        if not workflow_id:
            workflow_id = str(uuid.uuid4())
            logger.info("[Orchestrator] New workflow: %s", workflow_id)
            await self._persist_workflow(db, workflow_id, payload)

        payload["workflow_id"] = workflow_id

        # Fast keyword routing — no LLM call
        next_agent_name = _route_by_keywords(payload)
        logger.info(
            "[Orchestrator] workflow=%s routed_to=%s payload_keys=%s",
            workflow_id, next_agent_name, list(payload.keys()),
        )

        agent = self.registered_agents.get(next_agent_name)
        if not agent:
            raise RuntimeError(f"Agent not registered: {next_agent_name}")

        try:
            result = await asyncio.wait_for(
                agent.run(db, payload),
                timeout=WORKFLOW_TIMEOUT,
            )
        except asyncio.TimeoutError:
            elapsed = time.time() - t0
            logger.error(
                "[Orchestrator] workflow=%s agent=%s timed out after %.1fs",
                workflow_id, next_agent_name, elapsed,
            )
            raise RuntimeError(
                f"Agent '{next_agent_name}' did not respond within {WORKFLOW_TIMEOUT}s"
            )

        elapsed = time.time() - t0
        logger.info(
            "[Orchestrator] workflow=%s completed in %.2fs", workflow_id, elapsed
        )

        result["workflow_id"] = workflow_id
        return result

    async def _persist_workflow(
        self, db: AsyncSession, workflow_id: str, payload: Dict[str, Any]
    ) -> None:
        try:
            from backend.crud import workflow_instance
            from backend.schemas.workflow import WorkflowInstanceCreate
            await workflow_instance.create(
                db,
                obj_in=WorkflowInstanceCreate(
                    session_id=workflow_id,
                    status="STARTED",
                    context_data=payload,
                ),
            )
        except Exception as e:
            logger.error("[Orchestrator] Failed to persist workflow: %s", e)

    async def resume_workflow(
        self, workflow_id: str, approved: bool, payload: Dict[str, Any]
    ) -> None:
        from backend.core.database import AsyncSessionLocal
        from backend.crud import workflow_instance
        from backend.schemas.workflow import WorkflowInstanceUpdate

        async with AsyncSessionLocal() as db:
            db_wi = await workflow_instance.get_by_session(db, session_id=workflow_id)
            if not db_wi:
                logger.error("[Orchestrator] Workflow not found: %s", workflow_id)
                return
            context = {**(db_wi.context_data or {}), **payload}
            await workflow_instance.update(
                db,
                db_obj=db_wi,
                obj_in=WorkflowInstanceUpdate(
                    status="RESUMED" if approved else "REJECTED",
                    context_data=context,
                ),
            )
            if approved:
                await self.handle_request(db, workflow_id, context)


hospital_orchestrator = OrchestratorAIPlanner()

from agents.intake_agent.agent     import intake_agent
from agents.diagnosis_agent.agent  import diagnosis_agent
from agents.treatment_agent.agent  import treatment_agent
from agents.emergency_agent.agent  import emergency_agent
from agents.pharmacy_agent.agent   import pharmacy_agent
from agents.lab_agent.agent        import lab_agent
from agents.appointment_agent.agent import appointment_agent
from agents.billing_agent.agent    import billing_agent
from agents.insurance_agent.agent  import insurance_agent

hospital_orchestrator.register_agent(intake_agent.name,      intake_agent)
hospital_orchestrator.register_agent(diagnosis_agent.name,   diagnosis_agent)
hospital_orchestrator.register_agent(treatment_agent.name,   treatment_agent)
hospital_orchestrator.register_agent(emergency_agent.name,   emergency_agent)
hospital_orchestrator.register_agent(pharmacy_agent.name,    pharmacy_agent)
hospital_orchestrator.register_agent(lab_agent.name,         lab_agent)
hospital_orchestrator.register_agent(appointment_agent.name, appointment_agent)
hospital_orchestrator.register_agent(billing_agent.name,     billing_agent)
hospital_orchestrator.register_agent(insurance_agent.name,   insurance_agent)
