import hashlib, json
from typing import Any
from ..document_schema import Chunk, Document



class JsonChunker:
    def chunk(self, document: Document) -> list[Chunk]:
        data = Document.content

        if not isinstance(data, (dict, list)):
            return []

        if isinstance(data, list):
            return self._chunk_list(
                document = document,
                data = data,
                path = 'root'
            )

        list_fields = {
            key: value for key, value in data.items() if isinstance(value, list)
        }

        if not list_fields:
            return [
                self._create_chunk(
                    document = document,
                    data = data,
                    path = 'root'
                )
            ]

        chunks: list[Chunk] = []

        for field_name, items in list_fields.items():
            chunks.extend(
                self._chunk_list(
                    document = document,
                    data = items,
                    path = field_name,
                )
            )

        remaining_data = {
            key: value for key, value in data.items() if key not in list_fields
        }

        if remaining_data:
            chunks.append(
                self._create_chunk(
                    document = document,
                    data = remaining_data,
                    path = 'root',
                )
            )


        return chunks


    def _chunk_list(self, document: Document, data: list[Any], path: str,) -> list[Chunk]:
        chunks: list[Chunk] = []

        for index, item in enumerate(data):
            item_path = f'{path}[{index}]'

            chunks.append(
                self._create_chunk(
                    document = document,
                    data = item,
                    path = item_path,
                )
            )


        return chunks


    def _create_chunk(self, document: Document, data: Any, path: str,) -> Chunk:
        content = json.dumps(data, indent = 2, ensure_ascii = False)

        hierarchy_id = self._generate_hierarchy_id(document.document_id, path,)

        chunk_id = self._generate_chunk_id(document.document_id, path, content)

        metadata = {
            **document.metadata,
            'content_type': 'json',
            'json_path': path,
        }


        return Chunk(
            chunk_id = chunk_id,
            document_id = document.document_id,
            content = content,
            hierarchy_id = hierarchy_id,
            source = document.source,
            metadata = metadata,
        )


    def _generate_hierarchy_id(self, document_id: str, path: str,) -> str:
        raw_value = f'{document_id}: {path}'

        return hashlib.sha256(raw_value.encode('utf-8')).hexdigest()[:16]


    def _generate_chunk_id(self, document_id: str, path: str, content: str,) -> str:
            raw_value = (f'{document_id}: {path}: {content}')
    
            return hashlib.sha256(raw_value.encode('utf-8')).hexdigest()[:16]