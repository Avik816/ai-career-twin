from sqlalchemy import select
from sqlalchemy.orm import Session
from ..pipelines.chunking.document_schema import Chunk, Document
from .schema import (ChunkEmbeddingModel, ChunkModel, DocumentModel,)



class KnowledgeRepository:
    def __init__(self, session: Session):
        self.session = session


    # Documents
    def save_document(self, document: Document) -> None:
        document_model = DocumentModel(
            document_id = document.document_id,
            source = document.source,
            file_type = document.file_type,
            metadata_ = document.metadata,
        )

        self.session.merge(document_model)


    # Chunks
    def save_chunks(self, chunks: list[Chunk]) -> None:
        for chunk in chunks:
            chunk_model = ChunkModel(
                chunk_id = chunk.chunk_id,
                document_id = chunk.document_id,
                hierarchy_id = chunk.hierarchy_id,
                content = chunk.content,
                metadata_ = chunk.metadata,
            )

            self.session.merge(chunk_model)

    def get_chunk(self, chunk_id: str,) -> ChunkModel|None:
        statement = (select(ChunkModel).where(ChunkModel.chunk_id == chunk_id))

        return self.session.scalar(statement)


    # Embeddings
    def save_embedding(self, chunk_id: str, embedding: list[float],) -> None:
        embedding_model = ChunkEmbeddingModel(chunk_id = chunk_id, embedding = embedding,)

        self.session.merge(embedding_model)


    # Vector Search
    def search_similar_chunks(self, query_embedding: list[float], limit: int = 5,) -> list[tuple[ChunkModel, float]]:
        distance = ChunkEmbeddingModel.embedding.cosine_distance(query_embedding)

        statement = (
            select(ChunkModel, distance.label('distance'),).
            join(ChunkEmbeddingModel, ChunkModel.chunk_id == ChunkEmbeddingModel.chunk_id,).
            order_by(distance).
            limit(limit)
        )

        results = self.session.execute(statement).all()

        return [(chunk, float(distance)) for chunk, distance in results]


    # Transaction Management
    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()