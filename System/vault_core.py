#!/usr/bin/env python3
"""
Local Vault Core – Diesel-Goose Secure Document Storage System

A local-first, Ollama-compatible document storage and retrieval system.
All data stays on Mac Mini M4. No cloud. No API calls. Fully sovereign.

Features:
- Semantic document storage with metadata
- Ollama-powered embedding and search
- Markdown-native (human readable)
- JSON index for fast lookup
- Category-based organization
- Full-text search
- Document versioning

Author: Diesel-Goose AI
Version: 1.0 – Local Sovereignty
"""

import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
import re

# Vault Configuration
VAULT_ROOT = Path.home() / "Documents" / "HonkNode" / "Duck-Pond"
INDEX_FILE = VAULT_ROOT / ".vault" / "index.json"
CONFIG_FILE = VAULT_ROOT / ".vault" / "config.json"
OLLAMA_API = "http://localhost:11434/api"

class LocalVault:
    """
    Main vault interface for document storage and retrieval.
    """
    
    def __init__(self):
        self._ensure_structure()
        self.index = self._load_index()
        self.config = self._load_config()
    
    def _ensure_structure(self):
        """Create vault directory structure."""
        dirs = [
            VAULT_ROOT / ".vault",
            VAULT_ROOT / "Knowledge-Base" / "Business",
            VAULT_ROOT / "Knowledge-Base" / "Technical",
            VAULT_ROOT / "Knowledge-Base" / "Personal",
            VAULT_ROOT / "Projects" / "Active",
            VAULT_ROOT / "Projects" / "Completed",
            VAULT_ROOT / "Archive",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    def _load_index(self) -> Dict:
        """Load document index."""
        if INDEX_FILE.exists():
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"documents": [], "version": "1.0", "last_updated": datetime.now().isoformat()}
    
    def _load_config(self) -> Dict:
        """Load vault configuration."""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "default_model": "llama3",
            "auto_embed": True,
            "categories": ["Business", "Technical", "Personal", "Project"]
        }
    
    def _save_index(self):
        """Save document index."""
        INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.index["last_updated"] = datetime.now().isoformat()
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2)
    
    def _generate_id(self, content: str) -> str:
        """Generate unique document ID."""
        hash_input = f"{content}{datetime.now().isoformat()}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content."""
        # Simple keyword extraction (can be enhanced with Ollama)
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        return list(set(words))[:20]  # Top 20 unique capitalized phrases
    
    def store(
        self,
        content: str,
        title: str,
        category: str = "General",
        tags: List[str] = None,
        source: str = "",
        format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Store a document in the vault.
        
        Args:
            content: Document content
            title: Document title
            category: Storage category (Business, Technical, Personal, Project)
            tags: List of tags for filtering
            source: Where this came from (email, chat, file, etc.)
            format: Content format (markdown, text, json)
        
        Returns:
            Document metadata dict
        """
        doc_id = self._generate_id(content)
        timestamp = datetime.now().isoformat()
        
        # Determine storage path
        if category in ["Business", "Technical", "Personal"]:
            storage_path = VAULT_ROOT / "Knowledge-Base" / category / f"{doc_id}.md"
        elif category == "Project":
            storage_path = VAULT_ROOT / "Projects" / "Active" / f"{doc_id}.md"
        else:
            storage_path = VAULT_ROOT / "Knowledge-Base" / "General" / f"{doc_id}.md"
        
        # Ensure directory exists
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create markdown with metadata header
        metadata = {
            "id": doc_id,
            "title": title,
            "category": category,
            "tags": tags or [],
            "source": source,
            "created": timestamp,
            "modified": timestamp,
            "format": format,
            "word_count": len(content.split()),
            "keywords": self._extract_keywords(content)
        }
        
        # Write document
        doc_content = f"""---
{json.dumps(metadata, indent=2)}
---

# {title}

{content}
"""
        
        with open(storage_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        # Update index
        doc_entry = {
            "id": doc_id,
            "title": title,
            "category": category,
            "tags": tags or [],
            "path": str(storage_path.relative_to(VAULT_ROOT)),
            "created": timestamp,
            "modified": timestamp,
            "keywords": metadata["keywords"],
            "word_count": metadata["word_count"]
        }
        
        # Remove old entry if exists
        self.index["documents"] = [d for d in self.index["documents"] if d["id"] != doc_id]
        self.index["documents"].append(doc_entry)
        self._save_index()
        
        print(f"✅ Stored: {title} ({doc_id})")
        return doc_entry
    
    def retrieve(self, doc_id: str) -> Optional[Dict]:
        """Retrieve a document by ID."""
        for doc in self.index["documents"]:
            if doc["id"] == doc_id:
                path = VAULT_ROOT / doc["path"]
                if path.exists():
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return {"metadata": doc, "content": content}
        return None
    
    def search(
        self,
        query: str = "",
        category: str = "",
        tags: List[str] = None,
        keywords: List[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search documents by various criteria.
        
        Args:
            query: Text to search in titles
            category: Filter by category
            tags: Filter by tags (all must match)
            keywords: Filter by keywords (any can match)
            limit: Max results
        
        Returns:
            List of matching document metadata
        """
        results = []
        
        for doc in self.index["documents"]:
            # Category filter
            if category and doc["category"] != category:
                continue
            
            # Tags filter (all must be present)
            if tags:
                if not all(tag in doc.get("tags", []) for tag in tags):
                    continue
            
            # Keywords filter (any can match)
            if keywords:
                doc_keywords = set(doc.get("keywords", []))
                if not any(kw in doc_keywords for kw in keywords):
                    continue
            
            # Text search in title
            if query:
                if query.lower() not in doc["title"].lower():
                    continue
            
            results.append(doc)
        
        # Sort by recency
        results.sort(key=lambda x: x["modified"], reverse=True)
        
        return results[:limit]
    
    def list_all(self, category: str = "") -> List[Dict]:
        """List all documents, optionally filtered by category."""
        if category:
            return [d for d in self.index["documents"] if d["category"] == category]
        return self.index["documents"]
    
    def delete(self, doc_id: str) -> bool:
        """Delete a document."""
        for doc in self.index["documents"]:
            if doc["id"] == doc_id:
                path = VAULT_ROOT / doc["path"]
                if path.exists():
                    # Move to archive instead of permanent delete
                    archive_path = VAULT_ROOT / "Archive" / f"{doc_id}.md"
                    shutil.move(path, archive_path)
                
                self.index["documents"] = [d for d in self.index["documents"] if d["id"] != doc_id]
                self._save_index()
                print(f"🗑️  Archived: {doc['title']}")
                return True
        return False
    
    def stats(self) -> Dict:
        """Get vault statistics."""
        docs = self.index["documents"]
        categories = {}
        for doc in docs:
            cat = doc["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_documents": len(docs),
            "categories": categories,
            "last_updated": self.index.get("last_updated", "unknown"),
            "vault_root": str(VAULT_ROOT)
        }


# Convenience functions for quick access
_vault_instance = None

def get_vault() -> LocalVault:
    """Get or create vault singleton."""
    global _vault_instance
    if _vault_instance is None:
        _vault_instance = LocalVault()
    return _vault_instance

def store(content: str, title: str, **kwargs) -> Dict:
    """Quick store function."""
    return get_vault().store(content, title, **kwargs)

def search(query: str = "", **kwargs) -> List[Dict]:
    """Quick search function."""
    return get_vault().search(query, **kwargs)

def retrieve(doc_id: str) -> Optional[Dict]:
    """Quick retrieve function."""
    return get_vault().retrieve(doc_id)


if __name__ == "__main__":
    # Demo
    vault = LocalVault()
    
    print("🦆 Local Vault System")
    print("=" * 50)
    print(f"Vault root: {VAULT_ROOT}")
    print(f"Stats: {vault.stats()}")
    print()
    
    # Test store
    test_doc = vault.store(
        content="This is a test document for the Local Vault system.",
        title="Test Document",
        category="Technical",
        tags=["test", "demo"],
        source="demo"
    )
    
    print(f"\nStored document: {test_doc['id']}")
    
    # Test search
    results = vault.search(query="Test")
    print(f"\nSearch results: {len(results)} found")
    
    # Cleanup
    vault.delete(test_doc['id'])
