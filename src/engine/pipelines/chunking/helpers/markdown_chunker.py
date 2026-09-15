import hashlib, re
from ..document_schema import Chunk, Document



class MarkdownChunker:
    def chunk(self, document: Document) -> list[Chunk]:
        sections = self._parse_sections(document.content)

        chunks: list[Chunk] = []

        for section in sections:
            if section['level'] == 1:
                continue

            content = section['content'].strip()

            if not content:
                continue

            hierarchy_id = self._generate_hierarchy_id(
                document.document_id,
                section['path'],
            )

            chunk_id = self._generate_chunk_id(
                document.document_id,
                section['path'],
                content,
            )

            chunk_metadata = {
                **document.metadata,
                'content_type': 'markdown',
                'section': section['title'],
                'section_level': section['level'],
                'section_path': section['path'],
                'parent_section': section['parent_section'],
            }

            chunks.append(
                Chunk(
                    chunk_id = chunk_id,
                    document_id = document.document_id,
                    content = content,
                    hierarchy_id = hierarchy_id,
                    source = document.source,
                    metadata = chunk_metadata,
                )
            )


        return chunks


    def _parse_sections(self, content: str) -> list[dict]:
        heading_pattern = r"(?m)^(#{1,6})\s+(.+?)\s*$"
        matches = list(re.finditer(heading_pattern, content))

        if not matches:
            return []

        sections: list[dict] = []
        hierarchy_stack: list[tuple[int, str]] = []

        for index, match in enumerate(matches):
            level = len(match.group(1))
            title = match.group(2).strip()

            start = match.end()

            if index + 1 < len(matches):
                end = matches[index + 1].start()
            else:
                end = len(content)

            section_content = content[start:end].strip()

            while hierarchy_stack and hierarchy_stack[-1][0] >= level:
                hierarchy_stack.pop()

            parent_section = (
                hierarchy_stack[-1][1] if hierarchy_stack else None
            )

            section_path_parts = [
                item[1] for item in hierarchy_stack
            ]

            section_path_parts.append(title)

            section_path = ' > '.join(section_path_parts)

            sections.append(
                {
                    'title': title,
                    'level': level,
                    'content': f'{title}\n\n{section_content}',
                    'parent_section': parent_section,
                    'path': section_path,
                }
            )

            hierarchy_stack.append((level, title))


        return sections


    def _generate_hierarchy_id(self, document_id: str, section_path: str,) -> str:
        raw_value = f'{document_id}: {section_path}'

        return hashlib.sha256(
            raw_value.encode('utf-8')
        ).hexdigest()[:16]


    def _generate_chunk_id(self, document_id: str, section_path: str, content: str,) -> str:
            raw_value = (f'{document_id}: {section_path}: {content}')
    
            return hashlib.sha256(
                raw_value.encode('utf-8')
            ).hexdigest()[:16]