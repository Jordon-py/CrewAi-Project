# Distressed Home Prospect Finder — Research Summary

## Goals and Scope
- Build a CrewAI-powered workflow that discovers, enriches, and ranks distressed residential properties for a user-provided city and state.
- Provide actionable outputs: property address, owner/contact, distress indicators, valuation, and recommended outreach steps while respecting privacy and regulatory guardrails.

## CrewAI Platform Notes
- CrewAI supports multi-agent orchestration with YAML-driven agent/task configs, tool injection (HTTP clients, browsers, custom APIs), memory, and logging.
- Agents can be grouped in crews or chained via flows; tools can include web search, scraping, geocoding, and property/valuation APIs.
- Observability: Crew logs, task transcripts, and optional OpenAI tool-call logging help trace which agent produced each data point.

## Potential Data Sources for Distress Signals
- **Pre-foreclosure / auction**: County recorder/tax assessor portals; state foreclosure listings; Auction.com; RealtyTrac; HUD Home Store.
- **Tax liens & delinquencies**: County treasurer/recorder bulk files; state-level open data portals; private aggregators (DataTree, CoreLogic, ATTOM).
- **Code violations & permits**: City open data portals (e.g., Socrata/CKAN); municipal code-enforcement CSV/JSON feeds; building permit delays.
- **Utility shutoff & vacancy**: USPS vacancy data (via resellers), USPS NCOA updates, municipal water/electric shutoff notices where public.
- **Probate / divorce / eviction filings**: County court search portals; state court bulk data (requires ToS/legal review); Eviction Lab datasets for context.
- **Valuation / property profile**: Zillow/Redfin unofficial APIs discouraged; prefer ATTOM, Estated, DataTree, Catalyst (Official APIs) or MLS partner feeds.
- **Geospatial context**: Census ACS for neighborhood income/age-of-housing, FEMA flood risk, crime stats for risk adjustment.

## Data Acquisition Considerations
- Favor official or licensed APIs/CSV feeds with clear terms; avoid scraping sites that prohibit automated access in their ToS.
- Cache normalized records by parcel/APN + address; track source URLs and retrieval timestamps for auditability.
- Use rate limiting, user-agent identification, and retries with exponential backoff; respect robots.txt when scraping public pages.

## Legal, Privacy, and Compliance Notes
- Homeowner contact data must be sourced from providers that permit marketing/lead-gen use; honor Do-Not-Call (TCPA/FTC), CAN-SPAM for email, and state privacy laws (CCPA/CPRA, CPA, VCDPA, etc.).
- Provide opt-out/record-removal workflow and honor within statutory timelines; log consent and suppression events.
- Avoid collection of sensitive attributes (race, religion, health) to mitigate Fair Housing risks; keep targeting criteria property-based.
- Retain audit trails: data source, timestamp, agent/tool used, and any transformations; encrypt PII at rest (KMS-managed) and in transit (TLS).
- If using court records, confirm permissible purpose and terms; some states restrict bulk reuse. Scraping authenticated portals may be prohibited.

## Proposed Technology Stack (Initial)
- **Backend**: FastAPI + CrewAI for orchestration; async HTTP via httpx; pydantic models for validation; PostgreSQL for structured data; Redis for task/cache; optional vector store (pgvector) for semantic deduplication.
- **Agents/Crews**: Specialized agents for research, enrichment, deduplication, scoring, and compliance checks.
- **Frontend**: Next.js (React) with server actions calling FastAPI; Tailwind UI for quick layouts; CSV export via client utility.
- **Infrastructure**: Dockerized services; deployed on AWS (ECS/Fargate or EKS) with RDS Postgres, ElastiCache Redis, S3 for raw files; GitHub Actions CI; IaC via Terraform.

## Distress Scoring Signals (example features)
- Days-in-pre-foreclosure, auction date proximity, tax delinquency amount/age.
- Code violations count/severity and recent permits stalled/denied.
- Estimated equity (AVM minus liens), owner occupancy status, USPS vacancy flag, utility shutoff indicators.
- Neighborhood risk modifiers: crime trend, FEMA flood risk, school quality, median income trajectory.
- Engagement feedback: prior outreach responses, conversion rates (used for model retraining).

## Ethical Use and User Safeguards
- Default to informational/research output; require explicit user confirmation before outreach/marketing actions.
- Provide redaction/limited-view mode for demos; gate full contact details behind authenticated/authorized roles.
- Add disclosures: data currency, possible inaccuracies, and instructions for opting out or correcting records.

## Open Questions / Next Steps
- Confirm which jurisdictions provide open foreclosure/tax lien data via APIs for MVP (e.g., Clark County NV, Maricopa AZ).
- Select primary property/valuation provider (ATTOM vs Estated) and ensure licensing fits outreach use.
- Define minimal acceptable consent evidence for storing/using contact info and implement suppression table.
- Determine acceptable latency per request (single sync call vs. async job + callback/webhook for slower counties).
