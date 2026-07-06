from crewai import Crew, Task, Process
from app.agents.agent_configs import data_extractor, database_validator, formatter

def build_crew(raw_record: str) -> Crew:
    extract_task = Task(
        description=f"Extract structured fields from this raw record:\n\n{raw_record}",
        expected_output="A JSON string with fields: name, email, phone, raw_address_guess.",
        agent=data_extractor,
    )

    validate_task = Task(
        description="Validate the extracted fields from the previous task against the SQL Server customers table.",
        expected_output="A JSON string with the matched DB record and match_score, or 'NO_MATCH'.",
        agent=database_validator,
        context=[extract_task],
    )

    format_task = Task(
        description="Combine the extraction and validation outputs into the final standardized record.",
        expected_output="A single JSON object per the target schema.",
        agent=formatter,
        context=[extract_task, validate_task],
    )

    return Crew(
        agents=[data_extractor, database_validator, formatter],
        tasks=[extract_task, validate_task, format_task],
        process=Process.sequential,
        verbose=True,
    )