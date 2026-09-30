from datetime import datetime
from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



EMBEDDING_DIM = 384

class Base(DeclarativeBase):
    pass


class DocumentModel(Base):
    __tablename__ = 'documents'

    document_id: Mapped[str] = mapped_column(String(64), primary_key = True,)

    source: Mapped[str] = mapped_column(Text, nullable = False,)

    file_type: Mapped[str] = mapped_column(String(32), nullable = False,)

    metadata_: Mapped[dict] = mapped_column(
        'metadata',
        JSONB,
        nullable = False,
        default = dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now(),
        nullable = False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now(),
        onupdate = func.now(),
        nullable = False,
    )


class ChunkModel(Base):
    __tablename__ = 'chunks'

    chunk_id: Mapped[str] = mapped_column(String(64), primary_key = True,)

    document_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(
            'documents.document_id',
            ondelete = 'CASCADE',
        ),
        nullable = False,
        index = True,
    )

    hierarchy_id: Mapped[str] = mapped_column(
        String(64),
        nullable = False,
        index = True,
    )

    content: Mapped[str] = mapped_column(Text, nullable = False,)

    metadata_: Mapped[dict] = mapped_column(
        'metadata',
        JSONB,
        nullable = False,
        default = dict,
    )

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now(),
        nullable = False,
    )


class ChunkEmbeddingModel(Base):
    __tablename__ = 'chunk_embeddings'

    vector_id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True,
    )

    chunk_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(
            'chunks.chunk_id',
            ondelete = 'CASCADE',
        ),
        nullable = False,
        unique = True,
        index = True,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(EMBEDDING_DIM),
        nullable = False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now(),
        nullable = False,
    )