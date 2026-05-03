# AGENT_COMMS.md
> Handoff log entre agentes — ASD SDK v3.18.0

## Formato de Handoff

```yaml
- timestamp: ISO8601
  from_agent: agent_name
  to_agent: agent_name
  agent_source: asd | native
  task: descripción breve
  context: archivos o datos relevantes
  status: PENDING | ACCEPTED | COMPLETED | FAILED
```

## Handoffs

(vacío — ningún handoff registrado)

---
*Append-only. Cada agente registra su handoff antes de despachar.*
