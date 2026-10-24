"""Mono-agente académico UCV construido con Google ADK.

Incluye las tools del laboratorio más las del reto:
- explicar_concepto: ahora con 8 conceptos (3 originales + 5 nuevos).
- calcular_promedio: tool nueva con validación de entrada.
"""

from google.adk.agents.llm_agent import Agent

CONCEPTOS = {
    # --- Conceptos originales de la guía ---
    "api": "Una API permite comunicación entre sistemas.",
    "algoritmo": "Un algoritmo es una secuencia de pasos.",
    "base de datos": "Una base de datos almacena información.",
    # --- 5 conceptos nuevos (reto) ---
    "framework": (
        "Un framework es un conjunto de herramientas y reglas que "
        "facilita construir software sin partir de cero."
    ),
    "git": "Git es un sistema que guarda el historial de cambios de un proyecto.",
    "ci/cd": (
        "CI/CD es la automatización de pruebas y despliegues cada vez "
        "que se cambia el código."
    ),
    "machine learning": (
        "Machine learning es una rama de la IA donde el sistema aprende "
        "patrones a partir de datos."
    ),
    "agente": (
        "Un agente de IA es un programa que decide qué acciones tomar, "
        "incluso usando herramientas, para cumplir un objetivo."
    ),
}


def explicar_concepto(concepto: str) -> dict:
    """Explica un concepto técnico básico en lenguaje simple.

    Args:
        concepto: nombre del concepto a explicar (por ejemplo, "api").

    Returns:
        Un diccionario con `status` ("success", "not_found" o "error")
        y `explicacion`.
    """
    if not isinstance(concepto, str) or not concepto.strip():
        return {
            "status": "error",
            "explicacion": "Debes indicar un concepto (texto no vacío).",
        }

    clave = concepto.lower().strip()

    if clave in CONCEPTOS:
        return {"status": "success", "explicacion": CONCEPTOS[clave]}

    return {"status": "not_found", "explicacion": "Concepto no registrado."}


def calcular_promedio(numeros: list[float]) -> dict:
    """Calcula el promedio de una lista de números.

    Args:
        numeros: lista de valores numéricos (por ejemplo, notas).

    Returns:
        Un diccionario con `status` y `promedio` (o `mensaje` si hay error).
    """
    if not isinstance(numeros, list) or len(numeros) == 0:
        return {
            "status": "error",
            "mensaje": "Debes enviar una lista con al menos un número.",
        }

    # bool es subclase de int en Python; se excluye de forma explícita.
    if not all(
        isinstance(n, (int, float)) and not isinstance(n, bool) for n in numeros
    ):
        return {
            "status": "error",
            "mensaje": "Todos los elementos de la lista deben ser numéricos.",
        }

    promedio = sum(numeros) / len(numeros)
    return {"status": "success", "promedio": round(promedio, 2)}


root_agent = Agent(
    model="gemini-flash-latest",
    name="agente_ucv",
    description="Agente académico UCV",
    instruction="""
    Eres un asistente académico.
    Responde en español.
    Usa lenguaje simple.
    Cuando te pidan explicar un concepto técnico, usa la tool explicar_concepto.
    Cuando te pidan un promedio de números o notas, usa la tool calcular_promedio.
    """,
    tools=[explicar_concepto, calcular_promedio],
)
