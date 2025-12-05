# Distressed Home Prospect Finder

A CrewAI-powered system that discovers, enriches, and ranks distressed residential properties for a user-provided city/state. The stack combines a multi-agent backend (CrewAI + FastAPI) with a Next.js UI for entering search regions, reviewing prospects, and exporting to CSV/CRM.

## Project Status
- **Current focus:** Research and architecture definition. See `docs/research_summary.md` and `docs/architecture_blueprint.md` for findings and design.
- **Next steps:** Implement CrewAI agents, FastAPI endpoints, and the Next.js UI; wire data providers and compliance safeguards.

## Installation
Ensure you have Python >=3.10 and [uv](https://docs.astral.sh/uv/) installed.

```bash
pip install uv
crewai install
```

Add your credentials to `.env` (e.g., `OPENAI_API_KEY`, provider API keys) before running.

## Running (template)
From the project root:

```bash
crewai run
```

The default template will be replaced with the distressed-home workflow in upcoming iterations.

## Documentation
- Research summary: `docs/research_summary.md`
- Architecture blueprint: `docs/architecture_blueprint.md`
- Crew configuration (to be customized): `src/my_crew_project/config/agents.yaml`, `src/my_crew_project/config/tasks.yaml`

## Compliance and Safety
- Source contact data only from providers permitting outreach use; honor DNC/TCPA and CAN-SPAM.
- Encrypt PII in transit and at rest; log provenance and consent. Provide opt-out handling via suppression endpoints.

## Contributing
1. Create a branch for your feature/fix.
2. Run formatting/linting/tests as added.
3. Submit PRs with clear descriptions and links to updated docs.
