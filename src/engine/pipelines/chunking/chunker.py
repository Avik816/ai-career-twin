from .document_schema import Chunk, Document
from .helpers.json_chunker import JsonChunker
from .helpers.markdown_chunker import MarkdownChunker



class KnowledgeChunker:
    def __init__(self):
        self.markdown_chunker = MarkdownChunker()
        self.json_chunker = JsonChunker()


    def chunk_documents(self, documents: list[Document],) -> list[Chunk]:
        chunks: list[Chunk] = []

        for document in documents:
            if document.file_type == 'markdown':
                document_chunks = self.markdown_chunker.chunk(document)

            elif document.file_type == 'json':
                document_chunks = self.json_chunker.chunk(document)

            else:
                continue

            chunks.extend(document_chunks)


        return chunks