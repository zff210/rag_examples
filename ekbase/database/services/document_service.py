from typing import List
from ekbase.database.utils import Database
from ekbase.database.models.document import Document

class DocumentService:
    def __init__(self):
        self.db = Database()

    def create(self, document: Document) -> Document:
        query = """
        INSERT INTO documents (id, file_name, file_path, created_at)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute(query, (
            document.id,
            document.file_name,
            document.file_path,
            document.created_at
        ))
        self.db.commit()
        return self.get_by_id(document.id)
    
    def list_all(self, with_file_path: bool = False) -> List[Document]:
        query = "SELECT id, file_name, created_at"
        if with_file_path:
            query += ", file_path"
        query += " FROM documents"
        cursor = self.db.execute(query)
        return [Document.from_dict(dict(row)) for row in cursor]
    
    def delete(self, document_id: str):
        query = "DELETE FROM documents WHERE id = ?"
        self.db.execute(query, (document_id,))
        self.db.commit()

    def get_by_id(self, document_id: str) -> Document:
        query = "SELECT * FROM documents WHERE id = ?"
        cursor = self.db.execute(query, (document_id,))
        return Document.from_dict(dict(cursor.fetchone()))