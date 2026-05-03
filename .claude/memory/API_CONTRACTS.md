# API_CONTRACTS.md
> Contratos de APIs externas — ASD SDK v3.18.0 | Última actualización: 2026-05-03

## APIs Internas

No aplica — aplicación single-process, sin endpoints HTTP expuestos.

Interfaz interna principal:
```python
Orchestrator.route(query: str, user_id: str = "test-user") -> dict
# Returns: {query, intent, confidence, reasoning, answer, sources, agent}
```

## APIs Externas / Integraciones

| Servicio | Tipo | Credenciales |
|----------|------|-------------|
| OpenAI | REST/SDK (langchain-openai) | .env → OPENAI_API_KEY |
| Langfuse | REST/SDK (langfuse) | .env → LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST |

## Contratos de Mensajes (Events/MQ)

N/A — sin bus de eventos.

---
*Actualizado por context-collector — 2026-05-03.*
