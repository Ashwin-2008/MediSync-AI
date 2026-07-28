from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import AbstractBaseModel

class Conversation(AbstractBaseModel):
    __tablename__ = "conversations"
    session_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    summary: Mapped[Optional[str]] = mapped_column(String)
    
    messages: Mapped[List["Message"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")

class Message(AbstractBaseModel):
    __tablename__ = "messages"
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(50)) # user, assistant, system, tool
    content: Mapped[str] = mapped_column(String)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

class WorkflowInstance(AbstractBaseModel):
    __tablename__ = "workflow_instances"
    session_id: Mapped[str] = mapped_column(String(100), index=True)
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))
    status: Mapped[str] = mapped_column(String(50)) # RUNNING, COMPLETED, FAILED
    context_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    executions: Mapped[List["AgentExecution"]] = relationship(back_populates="workflow", cascade="all, delete-orphan")

class AgentExecution(AbstractBaseModel):
    __tablename__ = "agent_executions"
    workflow_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_instances.id", ondelete="CASCADE"))
    agent_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50)) # SUCCESS, FAILED
    execution_metrics: Mapped[Optional[dict]] = mapped_column(JSONB) # Summarized metrics (cost, time, tools used)
    output_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    workflow: Mapped["WorkflowInstance"] = relationship(back_populates="executions")

# Consolidated Analytics/System Table
class SystemAnalytics(AbstractBaseModel):
    __tablename__ = "system_analytics"
    metric_type: Mapped[str] = mapped_column(String(100)) # API_USAGE, MODEL_COST
    metric_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    aggregated_data: Mapped[dict] = mapped_column(JSONB)
