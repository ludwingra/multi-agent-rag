# ARCHITECTURE.md
> Generado por context-collector — ASD SDK v3.18.0 | Última actualización: 2026-05-03

## Stack Tecnológico

- **Lenguaje principal:** Python 3.11+
- **Runtime:** CPython
- **Framework:** LangChain
- **Package manager:** pip (requirements.txt)
- **Testing:** Jupyter notebook + test_queries.json (no framework formal)
- **Containerización:** N/A
- **Orquestación:** N/A
- **CI/CD:** N/A
- **Análisis estático:** N/A

## Patrón Arquitectónico

- **Patrón objetivo:** Modular con routing condicional (RunnableBranch/RunnableLambda)
- **Patrón actual (AS-IS):** Greenfield
- **Comunicación entre servicios:** In-process (single app)
- **Bus de eventos:** Ninguno

## Diagrama de Componentes

```
User Query
    │
    ▼
┌──────────────┐
│ Orchestrator │ ← classify_intent (LLM) → {hr|tech|finance|unknown}
│ (Router)     │
└──────┬───────┘
       │ RunnableBranch
       ├───────────────┬───────────────┐
       ▼               ▼               ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ HR Agent │    │Tech Agent│    │Fin Agent │
│ (RAG)    │    │ (RAG)    │    │ (RAG)    │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
     ▼               ▼               ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ChromaDB  │    │ChromaDB  │    │ChromaDB  │
│hr_docs   │    │tech_docs │    │fin_docs  │
└──────────┘    └──────────┘    └──────────┘

Observabilidad: Langfuse (traces jerárquicos por request)
Evaluador: Score API de Langfuse (bonus)
```

## Módulos del Sistema

| Módulo | Ruta | Responsabilidad |
|--------|------|----------------|
| config | src/config.py | Pydantic settings, env vars |
| tracing | src/tracing.py | Setup Langfuse CallbackHandler |
| document_loader | src/document_loader.py | Carga y chunking de .md → Documents |
| vector_store | src/vector_store.py | ChromaDB: create/load 3 colecciones |
| hr_agent | src/agents/hr_agent.py | RAG agent RRHH |
| tech_agent | src/agents/tech_agent.py | RAG agent soporte IT |
| finance_agent | src/agents/finance_agent.py | RAG agent finanzas |
| orchestrator | src/agents/orchestrator.py | Clasificador intención + router |
| evaluator | evaluator.py | Score API Langfuse (bonus) |

## Dependencias Externas

| Servicio | Tipo | Crítico |
|----------|------|---------|
| OpenAI API | REST (gpt-4o-mini) | Sí — LLM para clasificación y RAG |
| Langfuse | REST | Sí — observabilidad y scoring |
| ChromaDB | Local (disco) | Sí — vector store |

## Restricciones Técnicas

- Modelo LLM fijado en gpt-4o-mini (costo-eficiente para proyecto educativo)
- ChromaDB local, sin infraestructura externa
- chunk_size=500, chunk_overlap=50 (documentos cortos)
- Mínimo 50 chunks por dominio (15-20 archivos .md por carpeta)

---
*Actualizado por context-collector — 2026-05-03.*
