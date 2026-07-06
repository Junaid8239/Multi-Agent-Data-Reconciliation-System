from crewai import Agent, LLM
from app.config import settings
from app.tools.extraction_tool import ExtractionTool
from app.tools.db_validator_tool import DBValidatorTool
from app.tools.formatter_tool import FormatterTool

llm = LLM(model=settings.groq_model, api_key=settings.groq_api_key, temperature=0.1)

data_extractor = Agent(
    role="Data Extractor",
    goal="Parse messy, inconsistent raw records into clean structured fields.",
    backstory=(
        "You are meticulous at reading unstructured text and pulling out "
        "names, emails, phone numbers, and addresses even when formatting "
        "is inconsistent."
    ),
    tools=[ExtractionTool()],
    llm=llm,
    verbose=True,
)

database_validator = Agent(
    role="Database Validator",
    goal="Reconcile extracted fields against the authoritative SQL Server records.",
    backstory=(
        "You are a data-quality specialist who cross-checks incoming records "
        "against the source-of-truth database and flags the best match with "
        "a confidence score."
    ),
    tools=[DBValidatorTool()],
    llm=llm,
    verbose=True,
)

formatter = Agent(
    role="Formatter",
    goal="Produce a clean, standardized JSON record combining extraction and validation results.",
    backstory=(
        "You output only well-structured, consistent JSON matching the "
        "target schema, ready for downstream systems."
    ),
    tools=[FormatterTool()],
    llm=llm,
    verbose=True,
)