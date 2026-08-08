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
        focus="recordar lo que hablamos antes, buscar en archivos antiguos y dar continuidad a la charla",
        goal="asegurar que la conversación fluya y que recuerde detalles de otros chats o archivos pasados",
        triggers=("antes", "anterior", "dijiste", "hablamos", "recuerda", "contexto", "referias", "archivo antiguo", "otro chat", "pasado"),
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


def get_agent_options() -> str:
    # Antes: 'priority' se definía en cada AgentProfile pero nunca se leía en
    # ningún lugar del código; el orden dependía solo del orden de inserción
    # del diccionario. Ahora se ordena explícitamente por prioridad.
    ordered_agents = sorted(AGENT_REGISTRY.values(), key=lambda a: -a.priority)
    options = []
    for agent in ordered_agents:
        options.append(f"- {agent.key}: {agent.name}. Enfoque: {agent.focus}")
    options.append("- chat: Conversación general o preguntas que no requieren un especialista.")
    return "\n".join(options)


def run_specialist_agent(agent: AgentProfile, question: str, context: str, history: str, industry: str, llm_callback) -> str:
    prompt = AGENT_SPECIALIST_PROMPT.format(
        agent_name=agent.name,
        agent_focus=agent.focus,
        agent_goal=agent.goal,
        industry=industry,
        context=context,
        history=history,
        question=question,
    )
    return llm_callback(prompt=prompt, system_message=f"Eres {agent.name} dentro del sistema multiagente.", temperature=0.25)
