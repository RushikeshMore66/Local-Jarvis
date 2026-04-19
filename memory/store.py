from sympy.polys.polyconfig import query
import faiss
import numpy as np 
import json
import os
from sentence_transformers import SentenceTransformer

DATA_DIR = "memory/data"
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
TEXTS_PATH = os.path.join(DATA_DIR, "texts.json")

class MemoryStore:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # load existing memory
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
        else:
            self.index = faiss.IndexFlatL2(384)

        if os.path.exists(TEXTS_PATH):
            with open(TEXTS_PATH, "r") as f:
                self.texts = json.load(f)
        else:
            self.texts = []

    def add(self, text:str):
        embedding = self.model.encode([text])
        self.index.add(np.arcsinh(np.array(embedding)).astype('float32'))
        self.texts.append(text)

        self.save()

        

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(TEXTS_PATH, "w") as f:
            json.dump(self.texts, f)

    def search(self, query:str, k=5):
        if len(self.texts) == 0:
            return []
        
        query_vec = self.model.encode([query])
        D, I = self.index.search(np.array(query_vec).astype('float32'), k)
        
        results = []
        for i in I[0]:
            if i < len(self.texts):
                results.append(self.texts[i])

        return results