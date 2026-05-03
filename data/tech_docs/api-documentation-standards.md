# API Documentation Standards — TechNova Solutions

**Owner:** Engineering Platform Team | **Last Updated:** 2025-09-25 | **Applies To:** All Backend and Platform Engineers

---

## Overview

All internal and external APIs built at TechNova Solutions must be documented following these standards. Consistent documentation improves developer experience for FlowEngine customers and internal teams alike. Undocumented APIs will be blocked from merge to `main` by the CI/CD pipeline.

---

## API Documentation Toolchain

| Tool | Purpose |
|------|---------|
| **OpenAPI 3.1** | API specification format (YAML/JSON) |
| **Swagger UI** | Interactive documentation browser |
| **Redoc** | Customer-facing docs renderer |
| **Stoplight Studio** | Design-first API modeling |

All FlowEngine REST API specs live in the `flowengine-api-specs` repository at [github.technova.io/technova-engineering/flowengine-api-specs](https://github.technova.io/technova-engineering/flowengine-api-specs).

Public API docs are published at [developers.technova.io](https://developers.technova.io).

---

## OpenAPI Specification Requirements

Every endpoint must include:

```yaml
# Required fields per endpoint
paths:
  /v1/workflows:
    post:
      summary: "Create a new workflow"           # Required: short action phrase
      description: |                             # Required: full description (Markdown)
        Creates a new workflow definition in FlowEngine.
        Workflows must belong to an active tenant.
      operationId: createWorkflow                # Required: camelCase, globally unique
      tags:
        - Workflows                              # Required: group related endpoints
      security:
        - BearerAuth: []                         # Required: document auth method
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateWorkflowRequest'
            example:                             # Required: at least one example
              name: "Invoice Approval Flow"
              trigger_type: "webhook"
              steps: []
      responses:
        "201":
          description: "Workflow created successfully"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Workflow'
        "400":
          $ref: '#/components/responses/BadRequest'
        "401":
          $ref: '#/components/responses/Unauthorized'
        "422":
          $ref: '#/components/responses/UnprocessableEntity'
```

---

## Versioning Convention

TechNova APIs use **URI-based versioning**:

```
https://api.technova.io/v1/workflows
https://api.technova.io/v2/workflows   ← breaking changes require new major version
```

- Increment the **minor version** in the spec `info.version` for backward-compatible changes.
- Increment the **major version** (new URI prefix) for breaking changes.
- Deprecate old versions with a minimum **6-month sunset window**; add `Deprecation` and `Sunset` headers.

---

## Schema and Component Standards

- Reusable schemas go in `components/schemas/`. Avoid inline schema definitions for complex objects.
- Error responses must use the standard error envelope:

```yaml
components:
  schemas:
    ErrorResponse:
      type: object
      required: [error, message, request_id]
      properties:
        error:
          type: string
          example: "VALIDATION_ERROR"
        message:
          type: string
          example: "Field 'name' is required"
        request_id:
          type: string
          format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"
```

---

## Code-Level Documentation

### Python (FastAPI)

FastAPI generates OpenAPI specs automatically from docstrings and type annotations:

```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/v1/workflows", tags=["Workflows"])

@router.post("/", response_model=WorkflowResponse, status_code=201)
async def create_workflow(payload: CreateWorkflowRequest) -> WorkflowResponse:
    """
    Create a new workflow definition.

    - **name**: Human-readable workflow name (max 255 chars)
    - **trigger_type**: One of `webhook`, `schedule`, `manual`
    - **steps**: Ordered list of step definitions (may be empty on creation)
    """
    ...
```

### TypeScript (Express / NestJS)

Use **TSDoc** comments and `@nestjs/swagger` decorators:

```typescript
@ApiOperation({ summary: 'Create a new workflow' })
@ApiResponse({ status: 201, type: WorkflowDto })
@Post()
async createWorkflow(@Body() dto: CreateWorkflowDto): Promise<WorkflowDto> {
  // ...
}
```

---

## Documentation Checklist (Pre-Merge Gate)

- [ ] All new endpoints have `summary`, `description`, `operationId`, and `tags`
- [ ] All request/response schemas are documented with field descriptions
- [ ] At least one request example per endpoint
- [ ] All error responses (4xx, 5xx) are documented
- [ ] Breaking changes increment major version and add deprecation notice
- [ ] Spec validates without errors: `npx @stoplight/spectral-cli lint openapi.yaml`

See [Code Review Guidelines](code-review-guidelines.md) for API-specific review checklist items.

---

## Publishing and Keeping Docs Current

API docs are auto-published via the CI/CD pipeline on merge to `main`. The Redoc site at [developers.technova.io](https://developers.technova.io) refreshes within **10 minutes** of a successful deploy.

For internal API reference (not customer-facing), Swagger UI is available at [api-docs.internal.technova.io](https://api-docs.internal.technova.io) (VPN required).

---

## Related Documents

- [Code Review Guidelines](code-review-guidelines.md)
- [CI/CD Pipeline](ci-cd-pipeline.md)
- [Dev Environment Setup](dev-environment-setup.md)
- [Security Best Practices](security-best-practices.md)
