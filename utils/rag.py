"""
Simple RAG (Retrieval-Augmented Generation) utility for Shadow AI
"""
import os
import glob
from typing import List

def list_knowledge_files():
    kb_dir = os.path.join(os.path.dirname(__file__), 'knowledge_base')
    return glob.glob(os.path.join(kb_dir, '*'))

def search_knowledge_base(query: str, max_results=3) -> List[str]:
    """Naive search: return lines containing the query from all files."""
    results = []
    for fpath in list_knowledge_files():
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if query.lower() in line.lower():
                        results.append(line.strip())
                        if len(results) >= max_results:
                            return results
        except Exception:
            continue
    return results



