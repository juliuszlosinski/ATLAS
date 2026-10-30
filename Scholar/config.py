from pathlib import Path

ROOT = Path(__file__).parent
PDF_DIR = ROOT / "data" / "pdf"
QDRANT_DIR = ROOT / "data" / "qdrant"
BM25_PATH = ROOT / "data" / "bm25.pkl"
COLLECTION = "scholar"