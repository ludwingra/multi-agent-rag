# Plan de Trabajo: Sistema Multiagente RAG con LangChain + Langfuse

## 1. Análisis del Proyecto

### 1.1 Qué se pide

Un sistema de routing inteligente que clasifique consultas de clientes por departamento (HR, Tech, Finance) y las dirija a agentes RAG especializados, con observabilidad completa vía Langfuse.

### 1.2 Componentes principales

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| Orquestador | LangChain + LLM | Clasificar intención del usuario y enrutar al agente correcto |
| HR Agent | LangChain RAG | Responder consultas de RRHH con contexto de documentos internos |
| Tech Agent | LangChain RAG | Responder consultas de soporte IT |
| Finance Agent | LangChain RAG | Responder consultas financieras |
| Vector Stores | ChromaDB (1 por dominio) | Almacenar embeddings de documentos por dominio |
| Observabilidad | Langfuse | Tracing completo de cada request: clasificación → retrieval → generación |
| Evaluator (Bonus) | Langfuse Score API | Evaluar calidad de respuestas (1-10) automáticamente |

### 1.3 Decisiones de arquitectura recomendadas

**¿Por qué LangChain y no LangGraph?**
El proyecto pide explícitamente LangChain. Se usa `RunnableSequence`, `RunnableBranch` y `RunnableLambda` para el enrutamiento condicional, que es suficiente para este caso. No se necesita un grafo de estados complejo.

**¿Por qué ChromaDB?**
Es la opción más ligera para un proyecto educativo. No requiere infraestructura externa, se persiste en disco, y tiene integración nativa con LangChain.

**¿Por qué la estructura modular `src/agents/`?**
El enunciado permite notebook o archivos separados. La estructura modular facilita testing, mantenibilidad, y demuestra criterio de ingeniería — que es un objetivo explícito.

**Estrategia de chunking:**
Se recomienda `RecursiveCharacterTextSplitter` con `chunk_size=500` y `chunk_overlap=50`. Los documentos son cortos (políticas, FAQs), así que chunks pequeños mejoran la precisión del retrieval.

### 1.4 Estructura de archivos objetivo

```
multi-agent-rag/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── multi_agent_system.ipynb          # Notebook principal
├── test_queries.json                 # 10+ queries de prueba
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py           # Clasificador + router
│   │   ├── hr_agent.py               # RAG agent HR
│   │   ├── tech_agent.py             # RAG agent Tech
│   │   └── finance_agent.py          # RAG agent Finance
│   ├── config.py                     # Settings y env vars
│   ├── document_loader.py            # Carga y chunking de docs
│   ├── vector_store.py               # Inicialización de ChromaDB
│   └── tracing.py                    # Setup de Langfuse
├── data/
│   ├── hr_docs/                      # Mín 50 chunks (~15-20 archivos .md)
│   ├── tech_docs/                    # Mín 50 chunks (~15-20 archivos .md)
│   └── finance_docs/                 # Mín 50 chunks (~15-20 archivos .md)
└── evaluator.py                      # Bonus: Evaluator agent
```

---

## 2. Plan de Trabajo (6 fases)

### Fase 1: Scaffolding y configuración (30 min)

**Objetivo:** Tener el proyecto inicializado, dependencias instaladas, y configuración lista.

**Tareas:**
- Crear estructura de directorios
- Generar `requirements.txt` con las 9+ dependencias requeridas
- Crear `.env.example` con las API keys necesarias
- Crear `.gitignore`
- Crear `src/config.py` con Pydantic settings
- Crear `src/tracing.py` con el setup de Langfuse (CallbackHandler)

### Fase 2: Generación de documentos sintéticos (45 min)

**Objetivo:** 50+ chunks por dominio (HR, Tech, Finance) con contenido realista.

**Tareas:**
- Generar documentos para `data/hr_docs/` (políticas de vacaciones, onboarding, código de conducta, beneficios, evaluaciones, etc.)
- Generar documentos para `data/tech_docs/` (guías de troubleshooting, setup de VPN, políticas de seguridad, configuración de email, acceso a repos, etc.)
- Generar documentos para `data/finance_docs/` (políticas de reembolsos, presupuestos por departamento, calendario fiscal, procedimientos de compras, políticas de viajes, etc.)
- Cada archivo `.md` debe ser una política/FAQ coherente de ~200-500 palabras

### Fase 3: Vector Stores y Document Loading (45 min)

**Objetivo:** Pipeline funcional de carga de documentos → chunking → embeddings → ChromaDB.

**Tareas:**
- Implementar `src/document_loader.py`: cargar `.md`/`.txt` desde cada carpeta
- Implementar `src/vector_store.py`: crear/cargar 3 colecciones ChromaDB separadas
- Usar `RecursiveCharacterTextSplitter` para chunking
- Usar `OpenAIEmbeddings` para generar embeddings
- Persistir los vector stores en disco (`./chroma_db/`)
- Verificar que cada dominio tiene 50+ chunks

### Fase 4: Agentes RAG especializados (1h)

**Objetivo:** 3 agentes RAG funcionales, cada uno con su retriever y prompt específico.

**Tareas:**
- Crear clase base `BaseRAGAgent` con interfaz común
- Implementar `hr_agent.py` con prompt especializado en RRHH
- Implementar `tech_agent.py` con prompt especializado en soporte IT
- Implementar `finance_agent.py` con prompt especializado en finanzas
- Cada agente usa `RetrievalQA` o `create_retrieval_chain` de LangChain
- System prompt de cada agente incluye: rol, dominio, instrucciones de formato
- Instrumentar con `langfuse_callback` para tracing

### Fase 5: Orquestador y enrutamiento (1h)

**Objetivo:** Agente orquestador que clasifica la intención y enruta al agente correcto.

**Tareas:**
- Implementar clasificador de intención con `ChatPromptTemplate` + structured output
- Implementar router con `RunnableBranch` o `RunnableLambda` condicional
- Manejar caso `unknown` (intención no clasificable → respuesta genérica)
- Integrar los 3 agentes como branches del router
- Crear trace padre en Langfuse que agrupe: clasificación → retrieval → generación
- Testing manual con queries de cada dominio

### Fase 6: Notebook, Tests y Evaluator (1h)

**Objetivo:** Notebook completo con las 6 secciones requeridas + test queries + evaluator bonus.

**Tareas:**
- Crear `multi_agent_system.ipynb` con secciones marcadas en Markdown
- Crear `test_queries.json` con 10+ queries cubriendo HR, Tech, Finance y edge cases
- Ejecutar todas las queries y verificar resultados
- Implementar `evaluator.py` con la Score API de Langfuse (bonus)
- Escribir `README.md` completo
- Revisión final de todos los entregables

---

## 3. Prompts para Claude Code

Los siguientes prompts están diseñados para ejecutarse secuencialmente en Claude Code. Cada uno es autocontenido y referencia los archivos del paso anterior.

---

### PROMPT 1: Scaffolding del proyecto

```
Crea el scaffolding completo para un proyecto Python de sistema multiagente RAG.

## Estructura de directorios:
multi-agent-rag/
├── README.md (placeholder por ahora)
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py (placeholder con docstring)
│   │   ├── hr_agent.py (placeholder con docstring)
│   │   ├── tech_agent.py (placeholder con docstring)
│   │   └── finance_agent.py (placeholder con docstring)
│   ├── config.py
│   ├── document_loader.py (placeholder con docstring)
│   ├── vector_store.py (placeholder con docstring)
│   └── tracing.py
├── data/
│   ├── hr_docs/.gitkeep
│   ├── tech_docs/.gitkeep
│   └── finance_docs/.gitkeep
└── evaluator.py (placeholder con docstring)

## Archivos a implementar completamente:

### requirements.txt
Dependencias: langchain, langchain-openai, langchain-community, langfuse, openai, chromadb, tiktoken, python-dotenv, jupyter, ipykernel, pydantic-settings

### .env.example
OPENAI_API_KEY=your-openai-api-key-here
LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com

### .gitignore
.env, __pycache__, .ipynb_checkpoints, chroma_db/, *.pyc, node_modules/

### src/config.py
Usa pydantic-settings BaseSettings para cargar las env vars.
Incluye: OPENAI_API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST
Modelo por defecto: gpt-4o-mini
Chunk size: 500, chunk overlap: 50

### src/tracing.py
Setup de Langfuse usando CallbackHandler de langfuse.
Función get_langfuse_handler(trace_name: str, user_id: str = "test-user") que retorna un CallbackHandler configurado.
Función get_langfuse_client() que retorna el cliente Langfuse para la Score API.

Los placeholders deben tener un docstring describiendo su responsabilidad y la firma de los métodos principales (sin implementación, solo `pass` o `raise NotImplementedError`).
```

---

### PROMPT 2: Generación de documentos sintéticos

```
Genera documentos sintéticos realistas para una empresa SaaS ficticia llamada "TechNova Solutions" que gestiona clientes empresariales. Los documentos simulan la base de conocimiento interna de la empresa.

## Requisitos:
- Cada archivo debe ser coherente, profesional, y tener entre 200-500 palabras
- Formato: Markdown (.md)
- El contenido debe ser lo suficientemente detallado para que un RAG pueda responder preguntas específicas
- Cada carpeta debe tener 15-20 archivos para garantizar 50+ chunks después del splitting (chunk_size=500)

## data/hr_docs/ (20 archivos):
1. vacation-policy.md - Política de vacaciones (días por antigüedad, solicitud, aprobación)
2. remote-work-policy.md - Política de trabajo remoto (elegibilidad, equipos, horarios)
3. onboarding-guide.md - Guía de onboarding para nuevos empleados
4. benefits-overview.md - Resumen de beneficios (salud, dental, visión, 401k)
5. performance-review-process.md - Proceso de evaluación de desempeño
6. code-of-conduct.md - Código de conducta
7. parental-leave-policy.md - Política de licencia parental
8. training-development.md - Programas de capacitación y desarrollo
9. compensation-bands.md - Bandas salariales por nivel
10. sick-leave-policy.md - Política de licencia por enfermedad
11. diversity-inclusion.md - Programa de diversidad e inclusión
12. grievance-procedure.md - Procedimiento de quejas
13. employee-referral-program.md - Programa de referidos
14. dress-code.md - Política de vestimenta
15. termination-process.md - Proceso de terminación
16. internal-transfers.md - Política de transferencias internas
17. overtime-policy.md - Política de horas extra
18. team-events-budget.md - Presupuesto para eventos de equipo
19. mental-health-resources.md - Recursos de salud mental
20. stock-options-guide.md - Guía de stock options

## data/tech_docs/ (20 archivos):
1. vpn-setup-guide.md - Configuración de VPN corporativa
2. password-policy.md - Política de contraseñas
3. email-setup.md - Configuración de email corporativo
4. github-access.md - Acceso a repositorios GitHub
5. jira-workflow.md - Workflow de tickets en Jira
6. aws-access-request.md - Solicitud de acceso a AWS
7. incident-response.md - Procedimiento de respuesta a incidentes
8. security-best-practices.md - Mejores prácticas de seguridad
9. laptop-setup.md - Setup de laptop (Mac/Linux)
10. slack-guidelines.md - Guías de uso de Slack
11. ci-cd-pipeline.md - Pipeline CI/CD documentación
12. database-access.md - Acceso a bases de datos
13. api-documentation-standards.md - Estándares de documentación de APIs
14. code-review-guidelines.md - Guías de code review
15. monitoring-alerting.md - Monitoreo y alertas (Datadog)
16. disaster-recovery.md - Plan de recuperación ante desastres
17. data-backup-policy.md - Política de respaldos
18. network-troubleshooting.md - Troubleshooting de red
19. software-licenses.md - Licencias de software
20. dev-environment-setup.md - Setup de ambiente de desarrollo

## data/finance_docs/ (20 archivos):
1. expense-reimbursement.md - Política de reembolso de gastos
2. travel-policy.md - Política de viajes corporativos
3. purchase-requisition.md - Proceso de requisición de compras
4. budget-allocation.md - Asignación de presupuesto por departamento
5. invoice-processing.md - Procesamiento de facturas
6. corporate-card-policy.md - Política de tarjeta corporativa
7. fiscal-calendar.md - Calendario fiscal
8. vendor-payment-terms.md - Términos de pago a proveedores
9. audit-procedures.md - Procedimientos de auditoría
10. financial-reporting.md - Reportes financieros trimestrales
11. tax-compliance.md - Cumplimiento tributario
12. petty-cash-policy.md - Política de caja menor
13. subscription-management.md - Gestión de suscripciones SaaS
14. revenue-recognition.md - Reconocimiento de ingresos
15. cost-center-codes.md - Códigos de centros de costo
16. payroll-schedule.md - Calendario de nómina
17. contractor-payments.md - Pagos a contratistas
18. equipment-depreciation.md - Depreciación de equipos
19. charitable-donations.md - Política de donaciones
20. financial-controls.md - Controles financieros internos

## Instrucciones de contenido:
- Incluir datos específicos: fechas, montos, porcentajes, nombres de herramientas
- Cada documento debe referenciar al menos 1-2 otros documentos (para cross-references)
- Incluir secciones tipo FAQ dentro de algunos documentos
- Usar lenguaje corporativo profesional en inglés
- Los datos deben ser coherentes entre documentos (misma empresa, mismos beneficios, etc.)
```

---

### PROMPT 3: Document Loader y Vector Store

```
Implementa el pipeline de carga de documentos y vector stores para el proyecto multi-agent-rag.

## Contexto:
- Los documentos ya existen en data/hr_docs/, data/tech_docs/, data/finance_docs/
- Cada carpeta tiene ~20 archivos .md
- Se necesitan 3 colecciones ChromaDB separadas (una por dominio)

## src/document_loader.py

Implementa una clase DocumentLoader con:

1. `load_documents(directory: str) -> list[Document]`
   - Usa DirectoryLoader con UnstructuredMarkdownLoader o TextLoader
   - Añade metadata: source_file, domain (hr/tech/finance)
   
2. `split_documents(documents: list[Document], chunk_size: int = 500, chunk_overlap: int = 50) -> list[Document]`
   - Usa RecursiveCharacterTextSplitter
   - Preserva metadata del documento original
   
3. `load_and_split(directory: str, domain: str) -> list[Document]`
   - Método de conveniencia que combina load + split
   - Imprime stats: # documentos originales, # chunks resultantes

## src/vector_store.py

Implementa una clase VectorStoreManager con:

1. `__init__(self, persist_directory: str = "./chroma_db")`
   - Inicializa OpenAIEmbeddings
   
2. `create_store(self, documents: list[Document], collection_name: str) -> Chroma`
   - Crea colección ChromaDB con los documentos
   - Persiste en disco
   
3. `load_store(self, collection_name: str) -> Chroma`
   - Carga colección existente desde disco
   
4. `get_retriever(self, collection_name: str, k: int = 4) -> BaseRetriever`
   - Retorna un retriever configurado para búsqueda por similitud
   
5. `initialize_all_stores(self) -> dict[str, Chroma]`
   - Método que carga los 3 dominios, crea vector stores, retorna dict
   - Imprime stats de chunks por dominio
   - Si ya existen las colecciones persistidas, las carga en lugar de recrear

## Decisiones técnicas a documentar en docstrings:
- Por qué RecursiveCharacterTextSplitter (respeta estructura de markdown)
- Por qué chunk_size=500 (documentos cortos, mejor precisión)
- Por qué ChromaDB (ligero, sin infraestructura, buena integración LangChain)
- Por qué k=4 en retrieval (balance precisión/contexto para docs cortos)

## Testing:
Al final del archivo, incluir un bloque `if __name__ == "__main__"` que:
1. Cargue documentos de los 3 dominios
2. Cree los vector stores
3. Haga una query de prueba por dominio
4. Imprima los chunks recuperados
```

---

### PROMPT 4: Agentes RAG especializados

```
Implementa los 3 agentes RAG especializados para el sistema multiagente.

## Contexto:
- Los vector stores ya están creados (src/vector_store.py)
- Langfuse tracing ya está configurado (src/tracing.py)
- Cada agente recibe queries de su dominio y responde usando RAG

## Patrón de diseño:
Crear una clase base y 3 implementaciones.

## src/agents/base_agent.py (NUEVO - agregar este archivo)

```python
class BaseRAGAgent(ABC):
    """Agente RAG base con retriever, LLM y tracing."""
    
    def __init__(self, retriever, llm, agent_name: str):
        # Configura la chain de RAG
        # Configura el system prompt específico del dominio
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Retorna el system prompt específico del dominio."""
        
    def invoke(self, query: str, callbacks=None) -> dict:
        """Ejecuta la chain RAG con la query y retorna respuesta + sources."""
        # Retorna: {"answer": str, "sources": list[str], "agent": str}
```

## src/agents/hr_agent.py

System prompt: "Eres un especialista en Recursos Humanos de TechNova Solutions. Tu rol es responder consultas sobre políticas de la empresa, beneficios, procesos de RRHH y bienestar laboral. Responde ÚNICAMENTE basándote en los documentos proporcionados. Si no encuentras la información, indica que no está disponible en la documentación actual y sugiere contactar al equipo de HR directamente."

Debe usar create_retrieval_chain con:
- ChatOpenAI (gpt-4o-mini)
- Retriever del vector store de hr_docs
- Prompt que combine system prompt + contexto + pregunta
- Langfuse callback para tracing

## src/agents/tech_agent.py

System prompt: "Eres un especialista de Soporte Técnico de TechNova Solutions. Tu rol es ayudar a los empleados con problemas técnicos, configuración de herramientas, acceso a sistemas y troubleshooting. Proporciona instrucciones paso a paso cuando sea posible. Responde ÚNICAMENTE basándote en los documentos proporcionados. Si el problema requiere intervención manual del equipo de IT, indica el proceso de escalamiento."

## src/agents/finance_agent.py

System prompt: "Eres un especialista del departamento de Finanzas de TechNova Solutions. Tu rol es asistir con consultas sobre políticas financieras, reembolsos, presupuestos, procesos de compra y reportes financieros. Proporciona referencias específicas a políticas cuando sea posible. Responde ÚNICAMENTE basándote en los documentos proporcionados. Para transacciones que requieran aprobación, indica el flujo de aprobación correspondiente."

## Implementación de cada agente:

Usa este patrón con LangChain:
1. ChatPromptTemplate con: system message + contexto (from retriever) + human message
2. create_stuff_documents_chain para combinar docs con prompt
3. create_retrieval_chain para conectar retriever con la chain
4. El invoke() debe pasar el langfuse callback handler

## Cada agente debe:
- Retornar un dict con: answer, sources (nombres de archivos fuente), agent_name, domain
- Loggear en Langfuse: el trace debe incluir generation name = agent_name
- Manejar errores gracefully (si el retriever no encuentra nada relevante)

## Exports en src/agents/__init__.py:
Exportar las 3 clases de agentes y la base.
```

---

### PROMPT 5: Orquestador y enrutamiento

```
Implementa el agente orquestador que clasifica la intención del usuario y enruta al agente RAG correcto.

## Contexto:
- Los 3 agentes RAG ya están implementados (hr_agent, tech_agent, finance_agent)
- Los vector stores ya están inicializados
- Langfuse tracing ya está configurado

## src/agents/orchestrator.py

### Clasificador de intención

Implementa una función classify_intent que:

1. Recibe una query del usuario (str)
2. Usa ChatOpenAI con un prompt estructurado que clasifica en: "hr", "tech", "finance", "unknown"
3. El prompt de clasificación debe incluir:
   - Descripción de cada categoría con ejemplos
   - Instrucción de retornar JSON: {"intent": "hr|tech|finance|unknown", "confidence": 0.0-1.0, "reasoning": "..."}
4. Parsea la respuesta JSON
5. Instrumenta con Langfuse: span type="classification"

### Prompt de clasificación sugerido:
```
Eres un clasificador de intenciones para TechNova Solutions.
Analiza la consulta del usuario y clasifícala en UNA de estas categorías:

- "hr": Consultas sobre recursos humanos, políticas de personal, beneficios, vacaciones, 
  onboarding, evaluaciones, conducta laboral, compensación, licencias.
  Ejemplos: "¿Cuántos días de vacaciones tengo?", "¿Cómo funciona el proceso de onboarding?"

- "tech": Consultas sobre tecnología, soporte IT, configuración de herramientas, acceso a 
  sistemas, VPN, seguridad, incidentes técnicos, desarrollo.
  Ejemplos: "¿Cómo configuro la VPN?", "No puedo acceder a GitHub"

- "finance": Consultas sobre finanzas, reembolsos, presupuestos, compras, facturas, 
  viajes, tarjetas corporativas, impuestos.
  Ejemplos: "¿Cómo solicito un reembolso?", "¿Cuál es la política de viajes?"

- "unknown": Si la consulta no encaja claramente en ninguna categoría anterior.

Responde SOLO con un JSON válido:
{"intent": "...", "confidence": 0.0-1.0, "reasoning": "breve justificación"}
```

### Router

Implementa una clase Orchestrator con:

1. `__init__(self)`:
   - Inicializa los 3 agentes RAG
   - Inicializa los vector stores
   - Configura el Langfuse client

2. `route(self, query: str, user_id: str = "test-user") -> dict`:
   - Crea un trace padre en Langfuse para toda la operación
   - Llama a classify_intent (span hijo: classification)
   - Según la intención, delega al agente correspondiente (span hijo: rag_retrieval)
   - Si intent == "unknown", retorna respuesta genérica
   - Retorna dict completo: 
     {
       "query": str,
       "intent": str,
       "confidence": float,
       "reasoning": str,
       "answer": str,
       "sources": list[str],
       "agent": str
     }

3. `batch_route(self, queries: list[dict]) -> list[dict]`:
   - Procesa una lista de queries con intent esperado
   - Retorna resultados + accuracy del clasificador

### Tracing en Langfuse:

El trace de cada request debe verse así en Langfuse:
```
Trace: "user-query-{timestamp}"
├── Span: "intent-classification"
│   ├── Input: query del usuario
│   ├── Output: {intent, confidence, reasoning}
│   └── Generation: llamada al LLM clasificador
├── Span: "rag-retrieval" 
│   ├── Input: query + intent
│   ├── Retrieval: chunks recuperados del vector store
│   └── Generation: llamada al LLM del agente RAG
└── Output: respuesta final con sources
```

### Manejo de errores:
- Si la clasificación falla → loggear error en Langfuse, retornar respuesta genérica
- Si el RAG agent falla → loggear error, retornar "No pude procesar tu consulta"
- Si confidence < 0.5 → considerar manejar como "unknown" o enrutar con advertencia
```

---

### PROMPT 6: Test queries y notebook

```
Crea el archivo de test queries y el notebook principal del proyecto.

## test_queries.json

Crea un archivo JSON con mínimo 15 queries de prueba organizadas así:

```json
{
  "test_queries": [
    {
      "id": 1,
      "query": "How many vacation days do new employees get?",
      "expected_intent": "hr",
      "expected_keywords": ["vacation", "days", "new employees"],
      "difficulty": "easy"
    },
    // ... incluir:
    // - 4 queries de HR (easy y medium)
    // - 4 queries de Tech (easy y medium) 
    // - 4 queries de Finance (easy y medium)
    // - 3 edge cases:
    //   - Query ambigua entre 2 dominios
    //   - Query completamente fuera de dominio
    //   - Query que mezcla 2 dominios
  ]
}
```

## multi_agent_system.ipynb

Crea un Jupyter notebook con estas secciones exactas (separadas por Markdown headers):

### Sección 1: Setup e imports
- Imports de todos los módulos del proyecto
- Carga de variables de entorno con dotenv
- Verificación de que las API keys están configuradas
- Print de versiones de dependencias clave

### Sección 2: Carga de documentos y vector stores
- Instanciar DocumentLoader
- Cargar documentos de los 3 dominios
- Crear/cargar vector stores con VectorStoreManager
- Mostrar estadísticas: # docs y # chunks por dominio
- Query de prueba rápida por dominio para verificar retrieval

### Sección 3: Definición de agentes
- Instanciar los 3 agentes RAG
- Probar cada agente individualmente con 1 query
- Mostrar respuesta + sources de cada uno

### Sección 4: Orquestador y enrutamiento
- Instanciar el Orchestrator
- Demostración de clasificación de intención con 3 queries
- Demostración de enrutamiento completo
- Mostrar el dict de respuesta completo

### Sección 5: Pruebas y ejemplos
- Cargar test_queries.json
- Ejecutar batch_route con todas las queries
- Calcular y mostrar accuracy del clasificador
- Mostrar tabla de resultados: query | expected | actual | correct?
- Análisis de errores de clasificación (si hay)

### Sección 6: Integración con Langfuse
- Verificar conexión con Langfuse
- Ejecutar una query completa con tracing
- Mostrar cómo acceder al dashboard de Langfuse
- Print del trace URL para inspección
- Explicación en Markdown de qué métricas buscar en el dashboard

### Cada sección debe tener:
- Header Markdown claro (## Sección N: Título)
- Celdas de código funcionales
- Markdown explicativo entre celdas
- Comentarios inline en el código
```

---

### PROMPT 7: Evaluator agent (Bonus) y README

```
Implementa el evaluator agent y el README final del proyecto.

## evaluator.py

Implementa un evaluador automático que usa la Score API de Langfuse para puntuar cada respuesta.

### Lógica del evaluador:

1. Recibe: query original, respuesta del agente, intent clasificado, sources
2. Usa un LLM (gpt-4o-mini) para evaluar la respuesta en 3 dimensiones:
   - **relevance** (1-10): ¿La respuesta aborda directamente la pregunta?
   - **completeness** (1-10): ¿La respuesta cubre todos los aspectos de la pregunta?
   - **accuracy** (1-10): ¿La respuesta parece basarse en los documentos fuente?
3. Calcula un score overall = promedio de las 3 dimensiones
4. Envía los scores a Langfuse usando la Score API:
   ```python
   langfuse.score(
       trace_id=trace_id,
       name="relevance",
       value=score,
       comment="..."
   )
   ```

### Prompt del evaluador:
```
Evalúa la siguiente respuesta de un agente RAG corporativo.

Pregunta del usuario: {query}
Intención clasificada: {intent}
Respuesta del agente: {answer}
Documentos fuente: {sources}

Evalúa en estas dimensiones (1-10):
1. Relevance: ¿La respuesta aborda directamente la pregunta?
2. Completeness: ¿Cubre todos los aspectos necesarios?
3. Accuracy: ¿Parece basarse en documentos reales, no inventada?

Responde SOLO con JSON:
{
  "relevance": {"score": N, "reasoning": "..."},
  "completeness": {"score": N, "reasoning": "..."},
  "accuracy": {"score": N, "reasoning": "..."},
  "overall": N,
  "summary": "Resumen de la evaluación"
}
```

### Clase ResponseEvaluator:
- `evaluate_response(trace_id, query, answer, intent, sources) -> dict`
- `evaluate_batch(results: list[dict]) -> list[dict]` — evalúa múltiples respuestas
- `generate_report(evaluations: list[dict]) -> str` — genera reporte en texto

## README.md

Escribe un README profesional y completo con:

### Secciones:
1. **Título y descripción** del proyecto (qué es, qué problema resuelve)
2. **Arquitectura** (descripción de alto nivel con lista de componentes)
3. **Requisitos previos** (Python 3.11+, API keys necesarias)
4. **Instalación** paso a paso:
   - Clonar repo
   - Crear virtualenv
   - pip install -r requirements.txt
   - Copiar .env.example a .env y configurar keys
5. **Cómo ejecutar**:
   - Orden de ejecución de celdas del notebook
   - Qué celdas son opcionales (evaluator)
   - Cómo verificar en Langfuse
6. **Estructura del proyecto** (tree con explicación de cada archivo)
7. **Decisiones técnicas**:
   - Por qué LangChain (componentes production-grade, chains, retrievers)
   - Por qué ChromaDB (ligero, sin infra, persistencia local)
   - Por qué gpt-4o-mini (costo-eficiente para clasificación y RAG)
   - Por qué RecursiveCharacterTextSplitter (respeta estructura markdown)
   - Por qué RunnableBranch para routing (nativo LangChain, declarativo)
   - Por qué Langfuse (open-source, traces jerárquicos, Score API)
8. **Ejemplos de uso** (3 queries con respuesta esperada)
9. **Limitaciones conocidas**
10. **Mejoras futuras**

### Tono: profesional, conciso, orientado a un reviewer técnico.
```

---

## 4. Orden de ejecución recomendado

| Paso | Prompt | Tiempo estimado | Verificación |
|------|--------|-----------------|-------------|
| 1 | Scaffolding | 15 min | `tree multi-agent-rag/`, verificar requirements.txt |
| 2 | Documentos sintéticos | 30 min | Contar archivos por carpeta (20 cada una) |
| 3 | Document Loader + Vector Store | 30 min | `python -m src.vector_store` (debe imprimir 50+ chunks/dominio) |
| 4 | Agentes RAG | 30 min | Test manual de cada agente con 1 query |
| 5 | Orquestador | 30 min | Test de clasificación + routing con 3 queries |
| 6 | Notebook + Tests | 30 min | Ejecutar notebook completo, verificar test_queries |
| 7 | Evaluator + README | 20 min | Verificar scores en Langfuse, README legible |

**Tiempo total estimado: ~3 horas**

## 5. Checklist final antes de entregar

- [ ] `requirements.txt` tiene 9+ paquetes
- [ ] `.env.example` tiene las 4 variables requeridas
- [ ] `data/hr_docs/` tiene 20 archivos → 50+ chunks
- [ ] `data/tech_docs/` tiene 20 archivos → 50+ chunks
- [ ] `data/finance_docs/` tiene 20 archivos → 50+ chunks
- [ ] `test_queries.json` tiene 10+ queries con intent esperado
- [ ] Notebook tiene 6 secciones con headers Markdown
- [ ] Notebook ejecuta sin errores de principio a fin
- [ ] Langfuse muestra traces con spans de clasificación y RAG
- [ ] README tiene instrucciones de instalación y ejecución
- [ ] `evaluator.py` implementado (bonus)
- [ ] Repo es autocontenido (no depende de elementos externos no documentados)
- [ ] `.gitignore` excluye .env, chroma_db/, __pycache__