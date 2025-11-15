# Copilot Instructions for AI_Course_Eden_Marco

## Project Overview
This is an **AI Course Codebase** covering LangChain integration and generative AI concepts. The project is organized by course sections, each building progressively on prior knowledge.

## Key Technologies
- **Python 3.x** with `uv` package manager (preferred) or `pip`
- **LangChain**: Framework for building AI chains and prompts
- **External APIs**: OpenAI, Google, HuggingFace, LangSmith
- **Environment Management**: `python-dotenv` for credentials

## Project Structure
```
├── .env.example          # Template for environment variables
├── .github/
│   └── copilot-instructions.md  # This file
├── Section-2/            # LangChain fundamentals & chains
├── Section-4/            # Structured output & Pydantic
├── Section-5/            # Advanced patterns
└── pyproject.toml        # Root project config (if exists)
```

## Critical Security Rules
⚠️ **NEVER commit `.env` files containing API keys**

### Setup for New Development
1. Copy `.env.example` to `.env` in your section folder
2. Fill in actual credentials from your API providers
3. Never commit `.env` - it's in `.gitignore`
4. Use `python-dotenv` to load: `from dotenv import load_dotenv; load_dotenv()`

### If Credentials Are Exposed
- Immediately revoke tokens on: OpenAI, Google Cloud, HuggingFace, LangSmith
- Force push to remove from history if needed
- Never reuse compromised keys

## Development Workflow
1. **Setup**: `cd Section-X && uv sync` (or `pip install -r requirements.txt`)
2. **Run scripts**: `python script_name.py`
3. **Activate venv**: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
4. **Debugging**: Enable LangSmith tracing via `LANGSMITH_TRACING="true"` in `.env`

## LangChain Patterns
Common chain structure in this codebase:
```python
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

# Fluent API pattern: Prompt | Model | Parser
chain = prompt_template | model | output_parser
result = chain.invoke({"input": "..."})
```

### Key Files by Section
- **Section-2**: `first_langchain_chain.py` - Basic chain setup
- **Section-4**: `StrucuturedOutput.py`, `schemas.py` - Pydantic integration
- **Section-5**: `main.py` - Advanced workflows

## Dependencies Management
- **Windows line endings**: Repository uses LF; Windows Git may warn about CRLF conversion
- **Git submodules**: Section-4 is a git repository - consider converting to submodule with `git submodule add`
- **Nested venvs**: Each section has its own virtual environment (`.venv/` or `venv/`)

## Code Style & Conventions
- Follow Python PEP 8
- Use type hints where applicable
- Document API calls and their dependencies
- Include error handling for external API calls

## When Debugging
1. Check `.env` file is properly loaded and formatted
2. Verify API keys are active (not expired/revoked)
3. Use LangSmith dashboard (if tracing enabled) to inspect chain execution
4. Check Python version compatibility (see `.python-version` file in each section)
