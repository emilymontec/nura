# ai/agents.py
"""Multi-agent orchestration for NURA."""

from dataclasses import dataclass
from typing import Dict, List

from .prompts import AGENT_SPECIALIST_PROMPT


@dataclass(frozen=True)
class AgentProfile:
    key: str
    name: str
    focus: str
    goal: str
    triggers: tuple[str, ...]
    requires_dataset: bool = False
    priority: int = 50


AGENT_REGISTRY = {
    "context": AgentProfile(
        key="context",
        name="Asistente de Memoria",
        focus="recordar lo que hablamos antes y dar continuidad a la charla",
        goal="asegurar que la conversación fluya sin que tengas que repetir las cosas",
        triggers=("antes", "anterior", "dijiste", "hablamos", "recuerda", "contexto", "referias"),
        requires_dataset=False,
        priority=100,
    ),
    "risk": AgentProfile(
        key="risk",
        name="Detector de Alertas",
        focus="cosas extrañas, datos faltantes y señales de alarma en tu negocio",
        goal="avisarte de posibles problemas antes de que crezcan",
        triggers=("riesgo", "anomalia", "anomal", "error", "inconsistencia", "alerta", "problema"),
        requires_dataset=False,
        priority=92,
    ),
    "insight": AgentProfile(
        key="insight",
        name="Explorador de Oportunidades",
        focus="descubrimientos interesantes y cosas que están funcionando bien",
        goal="encontrar los puntos positivos y curiosos de tu información",
        triggers=("patron", "insight", "hallazgo", "oportunidad", "comportamiento", "tendencia"),
        requires_dataset=False,
        priority=90,
    ),
    "recommendation": AgentProfile(
        key="recommendation",
        name="Consejero Estratégico",
        focus="pasos a seguir, soluciones y consejos para mejorar",
        goal="darte ideas claras de qué hacer con los resultados obtenidos",
        triggers=("recomienda", "acción", "mejora", "optimiza", "solución", "qué hago", "siguiente paso", "estrategia"),
        requires_dataset=False,
        priority=88,
    ),
    "executive": AgentProfile(
        key="executive",
        name="Visión de Negocio",
        focus="el panorama general, el impacto en dinero y tiempo",
        goal="darte el resumen que un dueño de negocio necesita para decidir rápido",
        triggers=("ejecutivo", "negocio", "prioriza", "dirección", "impacto", "ceo", "gerencia", "visión"),
        requires_dataset=False,
        priority=84,
    ),
    "operations": AgentProfile(
        key="operations",
        name="Gestor de Operaciones",
        focus="el día a día, procesos y cómo hacer las cosas más rápido",
        goal="mejorar la eficiencia de tu trabajo diario",
        triggers=("operacion", "proceso", "eficiencia", "flujo", "cuello", "productivity"),
        requires_dataset=False,
        priority=78,
    ),
    "forecast": AgentProfile(
        key="forecast",
        name="Guía del Futuro",
        focus="hacia dónde van las cosas y qué esperar los próximos meses",
        goal="ayudarte a ver el camino que lleva tu negocio según los datos",
        triggers=("proyeccion", "forecast", "escenario", "futuro", "crec", "caer", "tendencia"),
        requires_dataset=True,
        priority=76,
    ),
}


def _has_dataset(context: Dict) -> bool:
    return bool(context and context.get("file_name"))


def _dataset_signal_count(context: Dict) -> int:
    count = 0
    if context.get("summary"):
        count += 1
    if context.get("health"):
        count += 1
    if context.get("trends"):
        count += 1
    if context.get("insights"):
        count += 1
    return count


def select_agents(question: str, context: Dict, history: str) -> List[AgentProfile]:
    """Select a compact but meaningful set of specialist agents."""
    lowered_question = (question or "").lower()
    lowered_history = (history or "").lower()
    has_dataset = _has_dataset(context)
    selected: List[AgentProfile] = []

    for agent in AGENT_REGISTRY.values():
        if agent.requires_dataset and not has_dataset:
            continue

        if agent.key == "context":
            if any(trigger in lowered_question for trigger in agent.triggers) or any(
                trigger in lowered_history for trigger in agent.triggers
            ):
                selected.append(agent)
            continue

        if any(trigger in lowered_question for trigger in agent.triggers):
            selected.append(agent)

    if has_dataset:
        defaults = ["insight", "risk", "recommendation"]
        if _dataset_signal_count(context) >= 3:
            defaults.append("executive")
    else:
        defaults = ["executive", "recommendation"]

    for key in defaults:
        agent = AGENT_REGISTRY[key]
        if agent not in selected:
            selected.append(agent)

    if "context" not in [agent.key for agent in selected]:
        if any(term in lowered_question for term in ("antes", "anterior", "mencionaste", "dijiste", "eso", "esa", "ese")):
            selected.insert(0, AGENT_REGISTRY["context"])

    unique_agents = []
    seen = set()
    for agent in sorted(selected, key=lambda item: item.priority, reverse=True):
        if agent.key not in seen:
            unique_agents.append(agent)
            seen.add(agent.key)

    return unique_agents[:4]


def run_specialist_agent(agent: AgentProfile, question: str, context: str, history: str, industry: str, llm_callback) -> str:
    """Run a specialist agent through the shared LLM callback."""
    prompt = AGENT_SPECIALIST_PROMPT.format(
        agent_name=agent.name,
        agent_focus=agent.focus,
        agent_goal=agent.goal,
        industry=industry,
        context=context,
        history=history,
        question=question,
    )
    return llm_callback(prompt=prompt, system_message=f"Eres {agent.name} dentro del sistema multiagente de NURA.", temperature=0.25)


def run_agent_system(question: str, context: str, history: str, industry: str, llm_callback) -> List[Dict[str, str]]:
    """Execute selected agents and return their outputs."""
    selected_agents = select_agents(question, context, history) # Note: context here is a string from _summarize_context, but select_agents expects a dict? Let me check.
    results = []
    for agent in selected_agents:
        output = run_specialist_agent(agent, question, context, history, industry, llm_callback)
        results.append(
            {
                "key": agent.key,
                "name": agent.name,
                "focus": agent.focus,
                "output": output,
            }
        )
    return results

def get_agent_options() -> str:
    """Return a formatted string of available agents for the LLM router."""
    options = []
    for agent in AGENT_REGISTRY.values():
        options.append(f"- {agent.key}: {agent.name}. Enfoque: {agent.focus}")
    options.append("- chat: Conversación general o preguntas que no requieren un especialista.")
    return "\n".join(options)

