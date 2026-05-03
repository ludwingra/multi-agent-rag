# TECH_DECISIONS.md
> ADRs del proyecto — ASD SDK v3.18.0 | Última actualización: 2026-05-03

## ADR-001: Framework RAG — LangChain
- **Decisión:** LangChain (no LangGraph)
- **Estado:** Activo
- **Alternativas consideradas:** LangGraph, LlamaIndex, Haystack
- **Justificación:** El proyecto pide explícitamente LangChain. RunnableSequence/RunnableBranch/RunnableLambda son suficientes para routing condicional sin grafo de estados.

## ADR-002: Vector Store — ChromaDB
- **Decisión:** ChromaDB con persistencia local en disco (`./chroma_db/`)
- **Estado:** Activo
- **Alternativas consideradas:** Pinecone, Weaviate, FAISS
- **Justificación:** Ligero, sin infraestructura externa, integración nativa con LangChain. Adecuado para proyecto educativo.

## ADR-003: LLM — gpt-4o-mini
- **Decisión:** OpenAI gpt-4o-mini para clasificación y generación RAG
- **Estado:** Activo
- **Alternativas consideradas:** gpt-4o, Claude, modelos open-source
- **Justificación:** Costo-eficiente para clasificación de intenciones y RAG sobre documentos cortos.

## ADR-004: Observabilidad — Langfuse
- **Decisión:** Langfuse (cloud) para tracing jerárquico + Score API para evaluación
- **Estado:** Activo
- **Alternativas consideradas:** LangSmith, Weights & Biases, custom logging
- **Justificación:** Open-source, traces jerárquicos, Score API nativa para evaluación automática.

## ADR-005: Chunking Strategy
- **Decisión:** RecursiveCharacterTextSplitter con chunk_size=500, chunk_overlap=50
- **Estado:** Activo
- **Justificación:** Documentos son cortos (políticas, FAQs ~200-500 palabras). Chunks pequeños mejoran precisión de retrieval. RecursiveCharacterTextSplitter respeta estructura markdown.

## ADR-006: Estructura Modular
- **Decisión:** Archivos separados en src/ con notebook principal como demo
- **Estado:** Activo
- **Alternativas consideradas:** Todo en notebook
- **Justificación:** Facilita testing, mantenibilidad, demuestra criterio de ingeniería.

## ADR-007: Estrategia de Branching
- **Decisión:** main + feature branches simples
- **Estado:** Activo
- **Convención de commits:** Conventional Commits (feat/fix/chore/docs/refactor)

## ADR-008: Modelo Claude Code
- **Sesión principal (orquestador):** Opus 4.6
- **Agentes de ejecución:** Sonnet 4.6
- **Estado:** Activo

---
*Nuevos ADRs: usar formato ADR-NNN con campos Decisión, Estado, Alternativas, Consecuencias.*
