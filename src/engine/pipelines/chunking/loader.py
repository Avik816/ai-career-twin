import json
from pathlib import Path
from typing import Any
from .document import Document



SUPPORTED_EXTENSIONS = ['.json', '.md', '.markdown']

class KnowledgeBaseLoader:
    def __init__(self, knowledge_base_path: str | Path):
        self.knowledge_base_path = Path(knowledge_base_path)

    def load(self) -> list[Document]:
        documents = []

        for file_path in self.knowledge_base_path.rglob('*'):
            if not file_path.is_file():
                continue