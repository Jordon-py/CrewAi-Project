# DistressedHomes CrewAI Project Instructions

## Project Architecture

This is a **CrewAI-based multi-agent system** for analyzing distressed real estate properties. The project uses a hierarchical process with four specialized agents orchestrated by a manager.

### Core Components

**Crew Definition**: `src/distressed_homes/crew.py` - Contains the main `Distressed_Homes_Crew` class with agent and task decorators
**Configuration**: Agent roles/goals in `config/agents.yaml`, task workflows in `config/tasks.yaml`
**Entry Points**: `main.py` provides `run()`, `train()`, `replay()`, and `test()` commands via CLI scripts
**Environment**: Uses `crew-env/` virtual environment (not `.venv`) - **always activate with `.\crew-env\Scripts\Activate.ps1`**

### Agent Architecture Pattern

```python
@agent
def agent_name(self) -> Agent:
    return Agent(
        config=self.agents_config['agent_name'],
        tools=[ScrapeWebsiteTool(), SerperDevTool()],  # Optional tools
        llm=self.llm,
        verbose=True
    )
```

### Task Architecture Pattern

```python
@task  
def task_name(self) -> Task:
    return Task(
        config=self.tasks_config['task_name'], 
        output_file="results/output.md"  # All outputs go to results/
    )
```

## Development Workflows

### Running the System
```bash
# Activate environment first
.\crew-env\Scripts\Activate.ps1

# Primary execution
crewai run
# or
python -m distressed_homes

# Alternative entry points
crewai install    # Install/lock dependencies
run_crew         # Direct script execution
```

### Key CLI Commands
- `train <iterations> <filename>` - Train agents with specific iterations
- `replay <task_id>` - Replay from specific task
- `test <iterations> <eval_llm>` - Test crew with evaluation LLM

### Environment Variables
**Required**: `OPENAI_API_KEY` in `.env` file
**Optional**: `GPT41` (defaults to 'openai/gpt-4.1')

## Data Flow & File Patterns

### Sequential Processing Pipeline
1. **manager_llm** → Reviews and validates each stage
2. **scraper_agent** → Outputs to `results/scraped_properties.md` 
3. **analyst_agent** → Outputs to `results/analyzed_properties.md`
4. **writer_agent** → Outputs to `results/distressed_report.md`

### Output Format Convention
- **All outputs are markdown files** (not JSON) in `results/` directory
- Each agent produces structured markdown with headers, tables, and sections
- Manager agent reviews each output before authorizing next phase

### Current Data Issues (From fix.md)
- Scraped data mixing JSON headers with content (should be pure markdown)
- Missing required fields: `address`, `price`, `signals`, `distress_level`, `score`, `contact_phone`
- Reports are too generic - need property-specific rankings and actionable insights

## Project-Specific Conventions

### Configuration Management
- **Never hardcode** agent definitions - use YAML configs exclusively
- LLM configuration uses environment variables with fallbacks
- Absolute path loading for `.env`: `C:\\Users\\Christopher\\projects\\distressed_homes\\.env`

### Error Handling Pattern
```python
try:
    Distressed_Homes_Crew().crew().kickoff(inputs=inputs)
except Exception as e:
    raise Exception(f"An error occurred while running the crew: {e}")
```

### Tool Integration
- Primary tools: `ScrapeWebsiteTool`, `SerperDevTool`, `FileWriterTool`
- Custom tools go in `src/distressed_homes/tools/` following `BaseTool` pattern
- Tools are assigned per-agent, not globally

## Context & Domain Knowledge

### Business Logic
The system identifies distressed properties through:
- **Distress Indicators**: Pre-foreclosure, auctions, tax liens, price reductions, extended market time
- **Scoring System**: Weighted indicators reflecting investment potential  
- **Output Target**: Top 20 ranked properties with actionable next steps

### Knowledge Sources
- `knowledge/user_preference.txt` - Contains user context (John Doe, AI Engineer, San Francisco)
- CrewAI documentation references throughout code comments
- Manager agent ensures data quality and workflow validation

## When Making Changes

1. **Configuration First**: Modify YAML configs before touching Python code
2. **Hierarchical Process**: Remember manager_llm oversees all other agents
3. **Markdown Outputs**: All inter-agent communication uses structured markdown
4. **Environment Activation**: Always verify `crew-env` is active before running
5. **Results Directory**: All outputs flow to `results/` - check existing files for current state

## Common Troubleshooting

- **Import errors**: Ensure `crew-env` virtual environment is activated
- **LLM issues**: Verify `OPENAI_API_KEY` in `.env` file
- **Task failures**: Check agent YAML configs for required fields
- **Output format**: Agents should output markdown, not JSON or mixed content
