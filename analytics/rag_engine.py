# analytics/rag_engine.py
import os
import io
import pandas as pd
from pypdf import PdfReader
from docx import Document
from typing import List, Dict, Any, Optional
from ai.vector_memory import vector_memory

class RAGAnalytics:
    """RAG (Retrieval-Augmented Generation) engine for documents and datasets."""
    
    def process_file(self, file_obj, session_id: str) -> Dict[str, Any]:
        """Extract text from various file types and index in vector memory."""
        file_name = getattr(file_obj, "name", "documento")
        suffix = os.path.splitext(file_name)[1].lower()
        content = ""

        try:
            # Read file into BytesIO to avoid consuming the cursor for downstream consumers
            raw_bytes = file_obj.read()
            buffer = io.BytesIO(raw_bytes)

            if suffix == ".pdf":
                buffer.seek(0)
                reader = PdfReader(buffer)
                text_parts = []
                for page in reader.pages:
                    text_parts.append(page.extract_text())
                content = "\n".join(text_parts)

            elif suffix == ".docx":
                buffer.seek(0)
                doc = Document(buffer)
                content = "\n".join([p.text for p in doc.paragraphs])

            elif suffix in [".xlsx", ".xls"]:
                buffer.seek(0)
                df = pd.read_excel(buffer)
                content = f"Archivo Excel: {file_name}\nColumnas: {', '.join(df.columns)}\nResumen:\n{df.describe().to_string()}\nVista previa:\n{df.head(10).to_string()}"

            elif suffix == ".csv":
                buffer.seek(0)
                df = pd.read_csv(buffer)
                content = f"Archivo CSV: {file_name}\nColumnas: {', '.join(df.columns)}\nVista previa:\n{df.head(10).to_string()}"

            if content:
                chunks = self._chunk_text(content)
                for i, chunk in enumerate(chunks):
                    vector_memory._add_to_index(chunk, {
                        "session_id": session_id,
                        "file_name": file_name,
                        "type": "rag_document"
                    })
                return {"status": "success", "content": content, "message": f"Contenido de '{file_name}' indexado correctamente."}

        except Exception as e:
            print(f"[RAGAnalytics] Error procesando {file_name}: {e}")
            return {"status": "error", "message": str(e), "content": ""}

        return {"status": "skipped", "message": "Tipo de archivo no procesado para RAG.", "content": ""}

    def _chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into manageable chunks for vector indexing."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1
            if current_size >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

rag_analytics = RAGAnalytics()
