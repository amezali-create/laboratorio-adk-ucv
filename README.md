# Laboratorio UCV — Google ADK + Poetry + GitHub + SonarQube

Sistemas Inteligentes · Ingeniería de Sistemas

Mono-agente académico construido con **Google ADK**. Explica conceptos técnicos
básicos y calcula promedios mediante *tools* de Python. Las dependencias se
gestionan con **Poetry**, el código se versiona en **GitHub** y cada `push`
ejecuta las pruebas y un análisis de calidad en **SonarQube** mediante
**GitHub Actions**.

[![SonarQube](https://github.com/amezali-create/laboratorio-adk-ucv/actions/workflows/sonarqube.yml/badge.svg)](https://github.com/amezali-create/laboratorio-adk-ucv/actions/workflows/sonarqube.yml)

---

## Qué hace el agente

| Tool | Descripción |
| --- | --- |
| `explicar_concepto(concepto)` | Explica 8 conceptos: api, algoritmo, base de datos, framework, git, ci/cd, machine learning, agente. |
| `calcular_promedio(numeros)` | Devuelve el promedio de una lista de números, redondeado a 2 decimales. |

Ambas tools **validan su entrada** y siempre devuelven un diccionario con
`status` (`success`, `not_found` o `error`), de modo que el modelo puede
explicar el problema al usuario en lugar de fallar.

## Estructura

```
laboratorio-adk-ucv/
├── agente_ucv/
│   ├── __init__.py
│   └── agent.py                  # agente + tools
├── tests/
│   └── test_agent.py             # 24 pruebas con pytest
├── .github/workflows/
│   └── sonarqube.yml             # CI: pytest + cobertura + SonarQube
├── .env                          # tu API key (NO se sube a GitHub)
├── .env.example                  # plantilla sin secretos (sí se sube)
├── sonar-project.properties      # configuración de SonarQube
├── pyproject.toml
├── poetry.lock
├── README.md
└── .gitignore
```

## Requisitos

- **Python 3.11 o superior** (`google-adk` no instala en 3.10)
- Poetry (`pip install poetry`)
- Git y una cuenta de GitHub
- API key de Gemini: <https://aistudio.google.com/apikey>
- Cuenta en SonarQube Cloud: <https://sonarcloud.io>

## Instalación

```bash
poetry config virtualenvs.in-project true
poetry install
```

Abre el archivo `.env` y reemplaza el valor por tu API key real:

```
GOOGLE_API_KEY="tu_clave_real"
```

> El `.env` está en `.gitignore`. **Nunca subas tu API key a GitHub.**

## Ejecución del agente

En la terminal, con chat de texto:

```bash
poetry run adk run agente_ucv
```

Con interfaz web:

```bash
poetry run adk web --port 8000
```

Luego abre <http://localhost:8000> y selecciona `agente_ucv`.

Ejemplos para probar:

- `¿Qué es una API?` → usa `explicar_concepto`
- `Explícame qué es CI/CD` → usa `explicar_concepto`
- `Calcula el promedio de 12, 15 y 18` → usa `calcular_promedio`
- `¿Qué es blockchain?` → responde que el concepto no está registrado

## Pruebas

```bash
poetry run pytest -v
poetry run pytest --cov=agente_ucv --cov-report=term-missing
```

Las pruebas no necesitan API key: prueban las tools directamente.

## Publicar en GitHub

1. Crea en GitHub un repositorio **público** vacío llamado `laboratorio-adk-ucv`
   (sin README ni .gitignore, para evitar conflictos).
2. Desde la carpeta del proyecto:

```bash
git init
git add .
git commit -m "feat: initial google adk mono-agent"
git branch -M main
git remote add origin https://github.com/amezali-create/laboratorio-adk-ucv.git
git push -u origin main
```

Antes del `git add .`, verifica con `git status` que **`.env` no aparezca**
en la lista.

## Configurar SonarQube Cloud

1. Entra a <https://sonarcloud.io> e inicia sesión con tu cuenta de GitHub.
2. *Analyze new project* → selecciona el repositorio `laboratorio-adk-ucv`.
3. Elige **With GitHub Actions** como método de análisis.
4. SonarQube te mostrará un token. En GitHub ve a
   *Settings → Secrets and variables → Actions → New repository secret* y
   crea el secreto **`SONAR_TOKEN`** con ese valor.
5. Edita `sonar-project.properties` con tu organización y tu *project key*
   (ambos los muestra SonarQube en la pantalla de configuración):

```
sonar.organization=tu-organizacion
sonar.projectKey=tu-organizacion_laboratorio-adk-ucv
```

6. Haz commit y push. La pestaña **Actions** de tu repositorio debe mostrar el
   pipeline en verde, y el análisis aparece en el panel de SonarQube.

## Qué hace el pipeline

En cada `push` a `main` (y en cada pull request) GitHub Actions:

1. Descarga el código.
2. Instala Python 3.11 y Poetry.
3. Instala las dependencias con `poetry install`.
4. Ejecuta `pytest` y genera `coverage.xml`.
5. Envía el código y la cobertura a SonarQube.

---

## Preguntas de reflexión

**¿Qué diferencia existe entre un chatbot y un agente?**
Un chatbot responde con texto a lo que se le pregunta. Un agente además decide
qué acciones tomar y puede usar herramientas para cumplir un objetivo: aquí el
modelo decide si debe llamar a `explicar_concepto` o a `calcular_promedio`, la
ejecuta y usa el resultado para construir su respuesta.

**¿Qué función cumple Poetry?**
Gestiona las dependencias y el entorno virtual del proyecto. `pyproject.toml`
declara lo que el proyecto necesita y `poetry.lock` fija las versiones exactas,
de modo que cualquier persona (o el servidor de GitHub Actions) reproduce el
mismo entorno con `poetry install`.

**¿Por qué GitHub Actions es importante en DevOps?**
Automatiza la integración continua: en cada cambio se instalan dependencias, se
ejecutan las pruebas y se lanza el análisis de calidad sin intervención manual.
Así los errores se detectan al momento del push, no cuando ya están en
producción, y se evita el clásico "en mi máquina funciona".

**¿Qué problemas ayuda a detectar SonarQube?**
Errores probables (*bugs*), vulnerabilidades de seguridad (por ejemplo,
credenciales escritas en el código), código duplicado, funciones demasiado
complejas y otros *code smells*. Además muestra la cobertura de pruebas y
verifica un *quality gate* de aprobación.

**¿Qué mejoras agregaría a este agente?**
Guardar los conceptos en un archivo JSON o una base de datos en lugar de un
diccionario dentro del código; agregar más tools (por ejemplo, convertir
unidades o buscar en documentación); darle memoria de conversación; añadir
evaluaciones del comportamiento del agente con `adk eval`; y desplegarlo en un
servicio en la nube.

---

## Reto del laboratorio — estado

| Requisito | Estado |
| --- | --- |
| Agregar 5 conceptos nuevos | Hecho: framework, git, ci/cd, machine learning, agente |
| Tool `calcular_promedio()` | Hecho |
| Pruebas unitarias con pytest | Hecho: 24 pruebas, 100 % de cobertura |
| Validación de entrada | Hecho en ambas tools |
| Publicar en GitHub | Pendiente: seguir la sección *Publicar en GitHub* |
| Pipeline de GitHub Actions en verde | Pendiente: requiere `SONAR_TOKEN` |

## Evidencias a entregar

1. Captura del agente funcionando (`adk run` o `adk web`).
2. Enlace al repositorio GitHub público.
3. Captura del pipeline de GitHub Actions exitoso.
4. Captura del análisis en SonarQube.
5. Este `README.md`.
