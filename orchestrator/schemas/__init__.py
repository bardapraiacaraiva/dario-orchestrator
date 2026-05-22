"""DARIO Orchestrator — central typed contracts (Onda 1 #2).

This package contains Pydantic v2 models that govern the I/O of every
agent, tool, and task in the orchestrator. They replace the dict-based
contracts that were the #1 source of silent failures.

Import surface:
    from schemas import (
        TaskSpec, TaskCreate, TaskComplete,           # tasks
        AgentInput, AgentOutput,                       # agents
        ToolCall, ToolResult,                          # tools
        ExecutionPolicy, Priority, ExecutorType,       # enums
    )
"""

from schemas.contracts import (
    AgentInput,
    AgentOutput,
    AssignResponse,
    AuditEntry,
    AuditResponse,
    BudgetResponse,
    ChainComposeResponse,
    ChainsListResponse,
    CheckoutResponse,
    CompleteResponse,
    DispatchResponse,
    EventStatsResponse,
    ExecutionPolicy,
    ExecutorType,
    HealthResponse,
    OnboardingChainResponse,
    ParsedDocumentResponse,
    Priority,
    PulseResponse,
    RubricResponse,
    ScoresResponse,
    StateResponse,
    TaskComplete,
    TaskCreate,
    TaskListResponse,
    TaskSpec,
    TaskStatus,
    TaxAlertResponse,
    TemplateInstantiateResponse,
    TemplateListResponse,
    ToolCall,
    ToolResult,
    ValidationCheckResponse,
    ValidationReport,
    WebhookEntry,
    WebhookListResponse,
    WebhookTestResponse,
)

__all__ = [
    "AgentInput",
    "AgentOutput",
    "AssignResponse",
    "AuditEntry",
    "AuditResponse",
    "BudgetResponse",
    "ChainComposeResponse",
    "ChainsListResponse",
    "CheckoutResponse",
    "CompleteResponse",
    "DispatchResponse",
    "EventStatsResponse",
    "ExecutionPolicy",
    "ExecutorType",
    "HealthResponse",
    "OnboardingChainResponse",
    "ParsedDocumentResponse",
    "Priority",
    "PulseResponse",
    "RubricResponse",
    "ScoresResponse",
    "StateResponse",
    "TaskComplete",
    "TaskCreate",
    "TaskListResponse",
    "TaskSpec",
    "TaskStatus",
    "TaxAlertResponse",
    "TemplateInstantiateResponse",
    "TemplateListResponse",
    "ToolCall",
    "ToolResult",
    "ValidationCheckResponse",
    "ValidationReport",
    "WebhookEntry",
    "WebhookListResponse",
    "WebhookTestResponse",
]
