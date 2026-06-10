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
            if suffix == ".pdf":
                reader = PdfReader(file_obj)
                text_parts = []
                for page in reader.pages:
                    text_parts.append(page.extract_text())
                content = "\n".join(text_parts)
            
            elif suffix == ".docx":
                doc = Document(file_obj)
                content = "\n".join([p.text for p in doc.paragraphs])
            
            elif suffix in [".xlsx", ".xls"]:
                # For Excel, we extract a summary and some sample rows as text for RAG
                df = pd.read_excel(file_obj)
                content = f"Archivo Excel: {file_name}\nColumnas: {', '.join(df.columns)}\nResumen:\n{df.describe().to_string()}\nVista previa:\n{df.head(10).to_string()}"
            
            elif suffix == ".csv":
                df = pd.read_csv(file_obj)
                content = f"Archivo CSV: {file_name}\nColumnas: {', '.join(df.columns)}\nVista previa:\n{df.head(10).to_string()}"
            
            if content:
                # Chunk content for better retrieval
                chunks = self._chunk_text(content)
                for i, chunk in enumerate(chunks):
                    vector_memory._add_to_index(chunk, {
                        "session_id": session_id, 
                        "file_name": file_name, 
                        "type": "rag_document"
                    })
                return {"status": "success", "message": f"Contenido de '{file_name}' indexado correctamente."}
            
        except Exception as e:
            print(f"[RAGAnalytics] Error procesando {file_name}: {e}")
            return {"status": "error", "message": str(e)}
            
        return {"status": "skipped", "message": "Tipo de archivo no procesado para RAG."}

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
