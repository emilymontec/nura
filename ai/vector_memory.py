# ai/vector_memory.py
import os
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional

class VectorMemory:
    """Vector-based memory for NURA using ChromaDB."""
    
    def __init__(self, db_path: str = "nura_memory"):
        self.client = chromadb.PersistentClient(path=db_path)
        # Using default embedding function (sentence-transformers/all-MiniLM-L6-v2)
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        
        # Collections for different types of memory
        self.conversations = self.client.get_or_create_collection(
            name="conversations", 
            embedding_function=self.ef
        )
        self.analyses = self.client.get_or_create_collection(
            name="analyses", 
            embedding_function=self.ef
        )
        self.datasets = self.client.get_or_create_collection(
            name="datasets", 
            embedding_function=self.ef
        )

    def store_conversation(self, session_id: str, role: str, content: str, message_id: str):
        """Store a chat message in vector memory."""
        self.conversations.add(
            ids=[f"msg_{message_id}"],
            documents=[content],
            metadatas=[{"session_id": session_id, "role": role, "type": "chat"}]
        )

    def store_analysis(self, session_id: str, file_name: str, analysis_text: str):
        """Store a business analysis summary in vector memory."""
        self.analyses.add(
            ids=[f"analysis_{session_id}_{file_name}"],
            documents=[analysis_text],
            metadatas=[{"session_id": session_id, "file_name": file_name, "type": "analysis"}]
        )

    def store_dataset_meta(self, session_id: str, file_name: str, meta_description: str):
        """Store dataset metadata/summary for long-term recall."""
        self.datasets.add(
            ids=[f"dataset_{session_id}_{file_name}"],
            documents=[meta_description],
            metadatas=[{"session_id": session_id, "file_name": file_name, "type": "dataset_meta"}]
        )

    def query_memory(self, query: str, limit: int = 3, n_results: int = 3) -> Dict[str, List[Any]]:
        """Search across all collections for relevant past information."""
        results = {
            "conversations": [],
            "analyses": [],
            "datasets": []
        }
        
        try:
            # Query conversations
            chat_res = self.conversations.query(query_texts=[query], n_results=n_results)
            if chat_res["documents"]:
                results["conversations"] = chat_res["documents"][0]
                
            # Query analyses
            anal_res = self.analyses.query(query_texts=[query], n_results=n_results)
            if anal_res["documents"]:
                results["analyses"] = anal_res["documents"][0]
                
            # Query datasets
            data_res = self.datasets.query(query_texts=[query], n_results=n_results)
            if data_res["documents"]:
                results["datasets"] = data_res["documents"][0]
        except Exception as e:
            print(f"[VectorMemory] Error querying: {e}")
            
        return results

vector_memory = VectorMemory()
