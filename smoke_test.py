"""Lightweight smoke test for CI.

This script performs a minimal runtime check:
- imports the backend package
- if possible, loads the sentence-transformers model and runs a small encode
"""
import sys
import time

print('Python', sys.version)

try:
    from yt_rag import backend
    print('Imported yt_rag.backend')
except Exception as e:
    print('Failed to import yt_rag.backend:', e)
    raise

try:
    from sentence_transformers import SentenceTransformer
    print('Loading sentence-transformers model (mini)...')
    start = time.time()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print('Model loaded in', time.time() - start)
    emb = model.encode(['CI smoke test'], convert_to_numpy=True)
    print('Encoded vector shape:', getattr(emb, 'shape', None))
except Exception as e:
    print('Embedding test skipped/failed:', e)

print('Smoke test completed')
