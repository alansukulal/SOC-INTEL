from pathlib import Path

from soc_intel.models.incident import Incident

#this means the filepath can be str or a path and it should return an incident schema data and last it should validate the json and return the data if proper data is there else error.
def load_incident(file_path: str | Path) -> Incident:
    json_data = Path(file_path).read_text(encoding="utf-8")

    return Incident.model_validate_json(json_data)