# Manual de Ejecucion — Multi-Agent RAG System

Guia practica para levantar, probar, entender y modificar el proyecto localmente.

---

## 1. Preparacion del entorno

### 1.1 Requisitos previos

- Python 3.11 o superior
- Una API key de OpenAI con credito disponible (se usa `gpt-4o-mini`)
- Cuenta en Langfuse (opcional, para observabilidad) — registro gratis en https://cloud.langfuse.com

### 1.2 Instalacion

```bash
# Clonar el repo
git clone https://github.com/ludwingra/multi-agent-rag.git
cd multi-agent-rag

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 1.3 Variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```
OPENAI_API_KEY=sk-...            # OBLIGATORIO
LANGFUSE_PUBLIC_KEY=pk-lf-...   # Opcional (tracing)
LANGFUSE_SECRET_KEY=sk-lf-...   # Opcional (tracing)
LANGFUSE_HOST=https://cloud.langfuse.com
```

Si no configuras Langfuse, el sistema funciona igual — las llamadas de tracing simplemente no envian datos.

---

## 2. Arquitectura del sistema

```
Documentos (.md)  ──>  DocumentLoader  ──>  Splitter (500 chars, 50 overlap)
                                                |
                                                v
                                           ChromaDB (local)
                                          /      |      \
                                     hr_docs  tech_docs  finance_docs
                                          \      |      /
                                           3 Retrievers
                                          /      |      \
                                    HRAgent  TechAgent  FinanceAgent
                                          \      |      /
                                        Orchestrator
                                    (classify_intent → route)
                                              |
                                              v
                                         Respuesta
                                    {query, intent, answer, sources}
                                              |
                                              v
                                    ResponseEvaluator (opcional)
                                    (LLM judge → scores a Langfuse)
```

### Componentes clave

| Archivo | Que hace |
|---------|----------|
| `src/config.py` | Carga variables de entorno con Pydantic Settings |
| `src/tracing.py` | Fabrica de clientes y handlers de Langfuse |
| `src/document_loader.py` | Lee archivos .md de cada dominio y los parte en chunks |
| `src/vector_store.py` | Gestiona colecciones ChromaDB (crear, cargar, buscar) |
| `src/agents/base_agent.py` | Clase abstracta que define el pipeline RAG (retriever → prompt → LLM) |
| `src/agents/hr_agent.py` | Agente especializado en RRHH |
| `src/agents/tech_agent.py` | Agente especializado en IT/Tech |
| `src/agents/finance_agent.py` | Agente especializado en Finanzas |
| `src/agents/orchestrator.py` | Clasifica la intencion y enruta al agente correcto |
| `src/evaluator.py` | LLM judge que puntua respuestas (relevance, completeness, accuracy) |

---

## 3. Ejecucion paso a paso

### 3.1 Via notebook (recomendado)

El notebook es el punto de entrada principal:

```bash
jupyter notebook notebooks/multi_agent_system.ipynb
# o
jupyter lab notebooks/multi_agent_system.ipynb
```

Ejecutar las celdas **en orden**. El notebook tiene 6 secciones:

| Seccion | Que hace | Tiempo estimado |
|---------|----------|----------------|
| 1. Setup e Imports | Configura paths, carga .env, verifica API keys | Instantaneo |
| 2. Carga de Documentos | Lee 60 .md, los fragmenta, crea/carga ChromaDB | ~30-60s (primera vez) / <1s (subsiguientes) |
| 3. Agentes RAG | Instancia los 3 agentes y prueba uno por uno | ~10s (3 llamadas a OpenAI) |
| 4. Orquestador | Prueba classify_intent y route con queries individuales | ~15s (4-5 llamadas) |
| 5. Batch Testing | Ejecuta 16 queries de test y mide accuracy del clasificador | ~2-3 min (16 queries x 2 LLM calls cada una) |
| 6. Langfuse | Verifica conexion y muestra como ver traces | ~5s |

**Primera ejecucion:** La seccion 2 embebe los 60 documentos en ChromaDB llamando a la API de OpenAI Embeddings. Esto toma 30-60 segundos. Las ejecuciones posteriores cargan las colecciones desde `./chroma_db/` sin re-embeber.

**Costo estimado:** Una ejecucion completa del notebook (16 batch queries + pruebas individuales) consume aprox. ~20-30K tokens de gpt-4o-mini (~$0.01-0.02 USD).

### 3.2 Via scripts individuales (para probar componentes aislados)

Cada modulo tiene un bloque `if __name__ == "__main__"` que funciona como smoke test:

```bash
# Probar carga de documentos (no requiere OpenAI)
python -m src.document_loader
# Output: 60 docs cargados, ~745 chunks generados

# Probar vector stores (requiere OPENAI_API_KEY para embeddings)
python -m src.vector_store
# Output: 3 colecciones creadas/cargadas + 1 query por dominio

# Probar agentes (requiere OPENAI_API_KEY + ChromaDB poblada)
python -m src.agents
# Output: 3 agentes instanciados + 1 respuesta por agente
```

### 3.3 Via Python interactivo

```python
from dotenv import load_dotenv
load_dotenv()

from src.agents import Orchestrator

orch = Orchestrator()

# Query individual
result = orch.route("How do I request vacation days?")
print(result["intent"])     # "hr"
print(result["answer"])     # Respuesta del HRAgent
print(result["sources"])    # Documentos usados

# Batch con accuracy
import json
with open("data/test_queries.json") as f:
    queries = json.load(f)["test_queries"]
batch = orch.batch_route(queries)
print(f"Accuracy: {batch['accuracy']:.1%}")
```

---

## 4. Entender el flujo de una query

Cuando llamas `orch.route("How do I set up the VPN?")`, esto es lo que pasa:

### Paso 1 — Clasificacion de intencion

`classify_intent()` en `orchestrator.py:39` envia la query a gpt-4o-mini con un prompt que pide clasificar en `hr | tech | finance | unknown`. El LLM responde JSON:

```json
{"intent": "tech", "confidence": 0.97, "reasoning": "VPN is IT infrastructure"}
```

### Paso 2 — Seleccion del agente

El Orchestrator usa el `intent` para elegir el agente (`self.agents["tech"]` → TechAgent).

Si `intent == "unknown"`, retorna una respuesta generica sin llamar a ningun agente.

### Paso 3 — Retrieval + Generacion (RAG)

El TechAgent ejecuta su `self.chain.invoke({"input": query})`:
1. El **retriever** busca los 4 chunks mas similares en la coleccion `tech_docs` de ChromaDB
2. Los chunks se inyectan como `{context}` en el prompt del agente
3. El LLM genera una respuesta basada solo en esos documentos

### Paso 4 — Tracing (si Langfuse esta configurado)

Todo el flujo queda registrado como un trace con spans anidados:
```
Trace: user-query
  ├── Span: intent-classification  (input: query, output: {intent, confidence})
  └── Span: rag-retrieval          (input: query, output: {answer, sources})
```

### Paso 5 — Evaluacion (opcional)

Si usas el `ResponseEvaluator`, envia la respuesta a otro LLM call que puntua:
- **relevance** (1-10): ¿la respuesta aborda la pregunta?
- **completeness** (1-10): ¿cubre todos los aspectos?
- **accuracy** (1-10): ¿esta basada en los documentos?

Los scores se envian a Langfuse via `langfuse.score()`.

---

## 5. Estructura de datos

### Documentos sinteticos (`data/`)

60 archivos Markdown sobre la empresa ficticia TechNova Solutions:
- `data/hr_docs/` — 20 documentos (vacaciones, beneficios, onboarding, etc.)
- `data/tech_docs/` — 20 documentos (VPN, CI/CD, incident response, etc.)
- `data/finance_docs/` — 20 documentos (reembolsos, presupuestos, facturas, etc.)

Cada documento tiene 450-900 palabras y menciona "TechNova Solutions" para dar coherencia.

### Queries de test (`data/test_queries.json`)

16 queries etiquetadas con `expected_intent` y `difficulty`:

```json
{
  "id": 1,
  "query": "How many vacation days do I get per year...?",
  "expected_intent": "hr",
  "expected_keywords": ["vacation", "PTO", "rollover"],
  "difficulty": "easy"
}
```

Distribucion: 4 HR, 4 Tech, 5 Finance, 1 unknown, 2 edge cases (hard).

### ChromaDB (`chroma_db/`)

Base de datos vectorial local. Se crea automaticamente al ejecutar el notebook o `python -m src.vector_store`. Contiene 3 colecciones (~745 chunks total). Si quieres forzar re-creacion, borra la carpeta:

```bash
rm -rf chroma_db/
```

---

## 6. Como hacer cambios

### 6.1 Agregar un nuevo dominio (ej: "legal")

1. Crear directorio `data/legal_docs/` con archivos .md
2. En `src/vector_store.py`, agregar al dict `DOMAINS`:
   ```python
   "legal": ("data/legal_docs", "legal_docs"),
   ```
3. Crear `src/agents/legal_agent.py` copiando el patron de `hr_agent.py`:
   ```python
   class LegalAgent(BaseRAGAgent):
       def __init__(self, retriever, llm, langfuse_handler=None):
           super().__init__(retriever, llm, agent_name="legal_agent",
                            domain="legal", langfuse_handler=langfuse_handler)

       def get_system_prompt(self) -> str:
           return "You are a legal specialist at TechNova Solutions..."
   ```
4. Registrar en `src/agents/__init__.py`
5. En `orchestrator.py`, agregar `"legal"` al prompt de clasificacion y al dict `self.agents`
6. Borrar `chroma_db/` para forzar re-indexacion

### 6.2 Cambiar el modelo LLM

Editar `.env`:
```
MODEL_NAME=gpt-4o
```

O para un modelo especifico por componente, modificar directamente la instanciacion del `ChatOpenAI` en el archivo correspondiente.

### 6.3 Ajustar el chunking

En `src/config.py`:
```python
CHUNK_SIZE: int = 500      # caracteres por chunk
CHUNK_OVERLAP: int = 50    # solapamiento entre chunks
```

Despues de cambiar estos valores, borrar `chroma_db/` y re-ejecutar para re-indexar.

### 6.4 Modificar el prompt de clasificacion

En `src/agents/orchestrator.py`, la variable `CLASSIFICATION_PROMPT` (linea 22) define como el LLM clasifica queries. Puedes ajustar las definiciones de cada dominio o agregar nuevos dominios aqui.

### 6.5 Modificar el prompt de un agente

Cada agente define su personalidad en `get_system_prompt()`. Por ejemplo, en `hr_agent.py`:
```python
def get_system_prompt(self) -> str:
    return "You are an HR specialist at TechNova Solutions..."
```

Cambiar este texto altera como el agente responde (tono, restricciones, formato).

### 6.6 Agregar queries de test

Editar `data/test_queries.json` y agregar entradas al array `test_queries`:
```json
{
  "id": 17,
  "query": "Tu nueva query aqui",
  "expected_intent": "hr",
  "expected_keywords": ["keyword1"],
  "difficulty": "medium"
}
```

---

## 7. Evaluador (ResponseEvaluator)

El evaluador es un componente bonus que usa un LLM como "juez" para puntuar respuestas.

### Uso basico

```python
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from src.config import Settings
from src.tracing import get_langfuse_client
from src.agents import Orchestrator
from evaluator import ResponseEvaluator

settings = Settings()
orch = Orchestrator()
langfuse = get_langfuse_client()
eval_llm = ChatOpenAI(model=settings.MODEL_NAME, api_key=settings.OPENAI_API_KEY)

evaluator = ResponseEvaluator(langfuse_client=langfuse, llm=eval_llm)

# Evaluar una respuesta individual
result = orch.route("What is the vacation policy?")
trace_id = langfuse.create_trace_id()
evaluation = evaluator.evaluate_response(
    trace_id=trace_id,
    query=result["query"],
    answer=result["answer"],
    intent=result["intent"],
    sources=result["sources"],
)
print(evaluation)
# {'trace_id': '...', 'query': '...', 'relevance': 9.0, 'completeness': 8.0,
#  'accuracy': 9.0, 'overall': 8.67, 'summary': '...'}
```

### Evaluacion batch

```python
# Ejecutar batch primero
batch = orch.batch_route(queries)

# Evaluar todas las respuestas
evaluations = evaluator.evaluate_batch(batch["results"])

# Generar reporte de texto
report = evaluator.generate_report(evaluations)
print(report)
```

El reporte muestra promedios por dimension, mejor y peor respuesta.

---

## 8. Troubleshooting

### "OPENAI_API_KEY is not set"

El archivo `.env` no existe o no tiene la variable. Verificar:
```bash
cat .env | grep OPENAI
```

### ChromaDB tarda mucho o falla

Borrar y recrear:
```bash
rm -rf chroma_db/
```
Luego re-ejecutar el notebook desde la seccion 2.

### "ModuleNotFoundError: No module named 'src'"

El directorio de trabajo no es la raiz del proyecto. Si estas en el notebook, la celda 1 ya maneja esto. Si estas en terminal:
```bash
cd /ruta/al/proyecto
python -c "from src.config import Settings; print('OK')"
```

### Langfuse no muestra traces

1. Verificar que `.env` tenga `LANGFUSE_PUBLIC_KEY` y `LANGFUSE_SECRET_KEY`
2. Probar conexion:
   ```python
   from src.tracing import get_langfuse_client
   client = get_langfuse_client()
   print(client.auth_check())  # debe imprimir True
   ```
3. Asegurar que `LANGFUSE_HOST` apunte al server correcto

### Accuracy del clasificador baja

- Revisar el `CLASSIFICATION_PROMPT` en `orchestrator.py` — puede necesitar ejemplos mas claros
- Revisar los documentos: si una query de "finance" tiene keywords de "hr", el clasificador puede confundirse
- Considerar cambiar a un modelo mas capaz (`gpt-4o`) para clasificacion

---

## 9. Resumen de comandos rapidos

```bash
# Activar entorno
source .venv/bin/activate

# Ejecutar notebook
jupyter notebook notebooks/multi_agent_system.ipynb

# Smoke tests por modulo
python -m src.document_loader    # Carga documentos (sin API call)
python -m src.vector_store       # Crea/carga ChromaDB + queries de prueba
python -m src.agents             # Instancia agentes + smoke test

# Reset de ChromaDB
rm -rf chroma_db/

# Query rapida desde terminal
python -c "
from dotenv import load_dotenv; load_dotenv()
from src.agents import Orchestrator
orch = Orchestrator()
r = orch.route('How do I request time off?')
print(f'{r[\"intent\"]} ({r[\"confidence\"]:.0%}): {r[\"answer\"][:200]}')
"
```
