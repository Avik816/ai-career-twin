from sqlalchemy import text
from .connection import engine
from .schema import Base



def initialize_database() -> None:
    with engine.begin() as connection:
        connection.execute(
            text('CREATE EXTENSION IF NOT EXISTS vector')
        )

        Base.metadata.create_all(connection)