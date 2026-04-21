from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from Backend.state import State
from Backend.BaseClass import BaseClass
from typing import List, Dict
class KeywordSearch(BaseClass):
    """
    Performs keyword-based search using TF-IDF cosine similarity.
    """

    def execute(self, state) -> State:
        query=state["TitledQuery"]
        chunks=state["chunks"]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(chunks)
        state["KeywordSearchResults"]=self.search(chunks=chunks,query=query)
        return state

    def search(self, chunks:List[str], query: str, top_k: int = 10) -> List[Dict]:
        """Return top-k chunks by keyword similarity."""
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        top_idx = np.argsort(scores)[::-1][:top_k]
        results = [
            {"text": chunks[i], "score": float(scores[i]), "source": "keyword"}
            for i in top_idx
        ]
        return results
    