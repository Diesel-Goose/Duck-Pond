#!/usr/bin/env python3
"""
Local Vault Search – Ollama-Powered Semantic Search

Enables natural language search across all vault documents using
local Ollama embeddings. No data leaves the Mac Mini.

Features:
- Semantic similarity search
- Natural language queries
- Document summarization
- Question answering over documents

Author: Diesel-Goose AI
Version: 1.0 – Ollama Integration
"""

import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
import math

from vault_core import get_vault, VAULT_ROOT

# Optional numpy for better performance
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

OLLAMA_API = "http://localhost:11434/api"
DEFAULT_MODEL = "llama3"

class VaultSearch:
    """Semantic search engine for Local Vault."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.vault = get_vault()
        self.embedding_cache = {}
    
    def _get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector from Ollama.
        
        Uses Ollama's generate API to create embeddings.
        Falls back to simple keyword-based if Ollama unavailable.
        """
        try:
            # Check cache
            text_hash = hash(text) % 1000000
            if text_hash in self.embedding_cache:
                return self.embedding_cache[text_hash]
            
            # Get embedding from Ollama
            response = requests.post(
                f"{OLLAMA_API}/embeddings",
                json={
                    "model": self.model,
                    "prompt": text[:512]  # Truncate for efficiency
                },
                timeout=30
            )
            
            if response.status_code == 200:
                embedding = response.json().get("embedding", [])
                self.embedding_cache[text_hash] = embedding
                return embedding
            else:
                # Fallback: return empty (will use keyword search)
                return []
        
        except Exception as e:
            print(f"⚠️  Ollama embedding failed: {e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2:
            return 0.0
        
        if HAS_NUMPY:
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            dot = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
        else:
            # Pure Python implementation
            dot = sum(a * b for a, b in zip(vec1, vec2))
            norm1 = math.sqrt(sum(a * a for a in vec1))
            norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot / (norm1 * norm2)
    
    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        category: str = ""
    ) -> List[Dict]:
        """
        Search documents by semantic similarity.
        
        Args:
            query: Natural language query
            top_k: Number of top results
            category: Optional category filter
        
        Returns:
            List of documents with similarity scores
        """
        print(f"🔍 Searching: '{query}'")
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Get all documents
        documents = self.vault.list_all(category=category)
        
        if not documents:
            print("📭 No documents in vault")
            return []
        
        results = []
        
        for doc in documents:
            # Get document embedding (from content preview)
            doc_text = f"{doc['title']} {' '.join(doc.get('keywords', []))}"
            doc_embedding = self._get_embedding(doc_text)
            
            # Calculate similarity
            if query_embedding and doc_embedding:
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
            else:
                # Fallback to keyword matching
                similarity = self._keyword_similarity(query.lower(), doc_text.lower())
            
            results.append({
                **doc,
                "similarity": similarity
            })
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        return results[:top_k]
    
    def _keyword_similarity(self, query: str, text: str) -> float:
        """Fallback keyword matching."""
        query_words = set(query.split())
        text_words = set(text.split())
        
        if not query_words:
            return 0.0
        
        matches = len(query_words & text_words)
        return matches / len(query_words)
    
    def ask(self, question: str, context_docs: int = 3) -> str:
        """
        Answer a question using vault documents as context.
        
        Args:
            question: Question to answer
            context_docs: Number of documents to use as context
        
        Returns:
            Generated answer from Ollama
        """
        # Find relevant documents
        relevant = self.semantic_search(question, top_k=context_docs)
        
        if not relevant:
            return "I don't have any documents that can help answer that question."
        
        # Build context
        context = "\n\n".join([
            f"Document {i+1}: {doc['title']}\n{doc.get('keywords', [])}"
            for i, doc in enumerate(relevant)
        ])
        
        # Build prompt
        prompt = f"""You are Diesel-Goose AI, the executive assistant to the Chairman of Greenhead Labs.

Use the following documents from the Local Vault to answer the question.
If the documents don't contain the answer, say so.

DOCUMENTS:
{context}

QUESTION: {question}

ANSWER:"""
        
        try:
            response = requests.post(
                f"{OLLAMA_API}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "No response")
            else:
                return f"Error: Ollama returned {response.status_code}"
        
        except Exception as e:
            return f"Error querying Ollama: {e}"
    
    def summarize_document(self, doc_id: str) -> str:
        """Generate a summary of a document using Ollama."""
        doc = self.vault.retrieve(doc_id)
        
        if not doc:
            return "Document not found"
        
        content = doc["content"]
        
        # Truncate if too long
        if len(content) > 4000:
            content = content[:4000] + "..."
        
        prompt = f"""Summarize the following document in 3-5 bullet points:

{content}

SUMMARY:"""
        
        try:
            response = requests.post(
                f"{OLLAMA_API}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "No summary generated")
            else:
                return f"Error: {response.status_code}"
        
        except Exception as e:
            return f"Error: {e}"
    
    def list_categories(self) -> Dict[str, int]:
        """List all categories and document counts."""
        stats = self.vault.stats()
        return stats.get("categories", {})


def main():
    """CLI interface for vault search."""
    import sys
    
    search = VaultSearch()
    
    if len(sys.argv) < 2:
        print("🦆 Local Vault Search")
        print("Usage:")
        print(f"  python vault_search.py 'your query'")
        print(f"  python vault_search.py --ask 'question'")
        print(f"  python vault_search.py --categories")
        return
    
    command = sys.argv[1]
    
    if command == "--categories":
        cats = search.list_categories()
        print("📁 Categories:")
        for cat, count in cats.items():
            print(f"  {cat}: {count} documents")
    
    elif command == "--ask":
        question = " ".join(sys.argv[2:])
        answer = search.ask(question)
        print(f"\n❓ {question}")
        print(f"\n💡 {answer}")
    
    else:
        # Regular search
        query = " ".join(sys.argv[1:])
        results = search.semantic_search(query)
        
        print(f"\n🔍 Results for: '{query}'\n")
        for i, doc in enumerate(results, 1):
            similarity = doc.get("similarity", 0)
            print(f"{i}. {doc['title']}")
            print(f"   Category: {doc['category']} | Score: {similarity:.2f}")
            print(f"   Tags: {', '.join(doc.get('tags', []))}")
            print()


if __name__ == "__main__":
    main()
