from typing import List, Dict, Tuple
import numpy as np
from Backend.EmbbedingManager import EmbeddingManager
from Backend.state import State
from Backend.BaseClass import BaseClass
class SimilaritySearch(BaseClass):

    def search(self, chunks:List[str],embeddings:np.ndarray,query: str, embedder: EmbeddingManager, top_k: int = 10) -> List[Dict]:
        """Return top-k most similar chunks for a given query."""
        q_emb = embedder.create_embeddings([query])[0]
        q_emb = q_emb / np.linalg.norm(q_emb)
        sims = np.dot(embeddings, q_emb)
        top_idx = np.argsort(sims)[::-1][:top_k]
        results = [
            {"text": chunks[i], "score": float(sims[i]), "source": "similarity"}
            for i in top_idx
        ]
        return results
    
    def execute(self, state) -> State:
        state["TitledQuery"]=state["vedioTitle"]+" "+state["query"]
        print(f"Similarity Search:{state}")
        query=state["TitledQuery"]
        chunks=state["chunks"]
        embbedings=state["embeddings"]
        # embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        state['SimilaritySearchResults']=self.search(query=query,embedder=EmbeddingManager(),chunks=chunks,embeddings=embbedings)
        return state