"""Pruebas unitarias de las tools del agente (no requieren API key)."""

import pytest

from agente_ucv.agent import CONCEPTOS, calcular_promedio, explicar_concepto, root_agent


# ---------- explicar_concepto ----------

def test_concepto_existente():
    resultado = explicar_concepto("api")

    assert resultado["status"] == "success"
    assert "comunicación" in resultado["explicacion"]


def test_concepto_ignora_mayusculas_y_espacios():
    assert explicar_concepto("  API  ")["status"] == "success"


@pytest.mark.parametrize(
    "concepto", ["framework", "git", "ci/cd", "machine learning", "agente"]
)
def test_conceptos_nuevos_del_reto(concepto):
    assert explicar_concepto(concepto)["status"] == "success"


def test_hay_al_menos_8_conceptos():
    assert len(CONCEPTOS) >= 8


def test_concepto_no_registrado():
    assert explicar_concepto("blockchain")["status"] == "not_found"


@pytest.mark.parametrize("entrada", ["", "   ", None, 123])
def test_concepto_entrada_invalida(entrada):
    assert explicar_concepto(entrada)["status"] == "error"


# ---------- calcular_promedio ----------

def test_promedio_correcto():
    resultado = calcular_promedio([10, 12, 14])

    assert resultado == {"status": "success", "promedio": 12.0}


def test_promedio_con_decimales():
    assert calcular_promedio([10, 15])["promedio"] == 12.5


def test_promedio_redondea_a_dos_decimales():
    assert calcular_promedio([1, 2, 2])["promedio"] == 1.67


@pytest.mark.parametrize("entrada", [[], "no es lista", None])
def test_promedio_lista_invalida(entrada):
    assert calcular_promedio(entrada)["status"] == "error"


@pytest.mark.parametrize("entrada", [[1, "a", 3], [True, 2], [None, 5]])
def test_promedio_elementos_no_numericos(entrada):
    assert calcular_promedio(entrada)["status"] == "error"


# ---------- configuración del agente ----------

def test_agente_tiene_las_dos_tools():
    nombres = {tool.__name__ for tool in root_agent.tools}

    assert nombres == {"explicar_concepto", "calcular_promedio"}


def test_agente_se_llama_agente_ucv():
    assert root_agent.name == "agente_ucv"
