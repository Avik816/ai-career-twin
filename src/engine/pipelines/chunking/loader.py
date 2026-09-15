import hashlib, json
from pathlib import Path
from typing import Any
from .document_schema import Document



SUPPORTED_EXTENSIONS = ['.json', '.md', '.markdown']

class KnowledgeBaseLoader:
    def __init__(self, knowledge_base_path: str | Path):
        self.knowledge_base_path = Path(knowledge_base_path)

    def load(self) -> list[Document]:
        documents: list[Document] = []

        for file_path in self.knowledge_base_path.rglob('*'):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            document = self._load_file(file_path)

            if document is not None:
                documents.append(document)


        return documents


    def _load_file(self, file_path: Path) -> Document | None:
        suffix = file_path.suffix.lower()

        if suffix == '.json':
            return self._load_json(file_path)

        if suffix in {'.md', '.markdown'}:
            return self._load_markdown(file_path)


        return None


    def _load_json(self, file_path: Path) -> Document:
        with file_path.open('r', encoding='utf-8') as file:
            content: Any = json.load(file)


        return Document(
            document_id = self._generate_document_id(file_path),
            content = content,
            source = str(file_path),
            file_type = 'json',
            metadata = {
                'filename': file_path.name,
                'path': str(file_path)
            },
        )


    def _load_markdown(self, file_path: Path) -> Document:
        content = file_path.read_text(encoding = 'utf-8')


        return Document(
            document_id = self._generate_document_id(file_path),
            content = content,
            source = str(file_path),
            file_type = 'markdown',
            metadata = {
                'filename': file_path.name,
                'path': str(file_path)
            },
        )


    def _generate_document_id(self, file_path: Path) -> str:
        source = str(file_path.resolve())


        return hashlib.sha256(
            source.encode('utf-8')
        ).hexdigest()[:16]