from dataclasses import dataclass


@dataclass
class VectorSearchResult:
    content: str
    job_id: str
