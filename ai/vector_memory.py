# ai/vector_memory.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Optional

class VectorMemory:
    """Vector-based memory for NURA using TF-IDF (extremely stable and lightweight)."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words=None)
        self.metadata = []

    def _add_to_index(self, content: str, meta: Dict[str, Any]):
        """Helper to add content and metadata."""
        try:
            self.metadata.append({
                "content": content,
                "meta": meta
            })
        except Exception as e:
            print(f"[VectorMemory] Error adding to memory: {e}")

    def store_conversation(self, session_id: str, role: str, content: str, message_id: str):
        """Store a chat message in memory."""
        self._add_to_index(content, {
            "session_id": session_id, 
            "role": role, 
            "type": "chat",
            "message_id": message_id
        })

    def store_analysis(self, session_id: str, file_name: str, analysis_text: str):
        """Store a business analysis summary in memory."""
        self._add_to_index(analysis_text, {
            "session_id": session_id, 
            "file_name": file_name, 
            "type": "analysis"
        })

    def store_dataset_meta(self, session_id: str, file_name: str, meta_description: str):
        """Store dataset metadata/summary for long-term recall."""
        self._add_to_index(meta_description, {
            "session_id": session_id, 
            "file_name": file_name, 
            "type": "dataset_meta"
        })

    def query_memory(self, query: str, n_results: int = 3) -> Dict[str, List[Any]]:
        """Search across all stored data for relevant past information using TF-IDF similarity."""
        results = {
            "conversations": [],
            "analyses": [],
            "datasets": []
        }
        
        if not self.metadata:
            return results
            
        try:
            # Prepare documents for TF-IDF
            documents = [item["content"] for item in self.metadata]
            
            # Fit and transform
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            query_vec = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            # Get top N indices
            top_indices = similarities.argsort()[-n_results:][::-1]
            
            for idx in top_indices:
                if similarities[idx] < 0.1: # Threshold to avoid irrelevant matches
                    continue
                    
                item = self.metadata[idx]
                content = item["content"]
                m_type = item["meta"].get("type")
                
                if m_type == "chat":
                    results["conversations"].append(content)
                elif m_type == "analysis":
                    results["analyses"].append(content)
                elif m_type == "dataset_meta" or m_type == "rag_document":
                    results["datasets"].append(content)
                    
        except Exception as e:
            print(f"[VectorMemory] Error querying: {e}")
            
        return results

vector_memory = VectorMemory()