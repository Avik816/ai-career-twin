from dataclasses import dataclass, field
from typing import Any



@dataclass
class Document:
    document_id: str
    content: Any
    source: str
    file_type: str
    metadata: dict[str, Any] = field(default_factory = dict)


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    content: str
    source: str
    hierarchy_id: str
    metadata: dict[str, Any] = field(default_factory = dict)