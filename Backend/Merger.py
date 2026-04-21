from typing import List, Dict
from Backend.BaseClass import BaseClass
from Backend.state import State

class MergeSearches(BaseClass):
    """
    Combines similarity search and keyword search results using late fusion.
    """

    def __init__(self, weight_vector: float = 0.6, weight_keyword: float = 0.4):
        self.wv = weight_vector
        self.wk = weight_keyword

    def merge(self, sim_results: List[Dict], key_results: List[Dict], top_k: int = 5) -> List[Dict]:
        """Merge results and normalize scores."""
        combined: Dict[str, float] = {}

        for r in sim_results:
            combined[r["text"]] = combined.get(r["text"], 0) + r["score"] * self.wv
        for r in key_results:
            combined[r["text"]] = combined.get(r["text"], 0) + r["score"] * self.wk

        # Sort by combined score
        merged = sorted(
            [{"text": k, "score": v} for k, v in combined.items()],
            key=lambda x: x["score"],
            reverse=True,
        )
        return merged
    def execute(self, state) -> State:
        similarityResults=state["SimilaritySearchResults"]
        keywordResults=state["KeywordSearchResults"]
        state["MergeResults"]=self.merge(sim_results=similarityResults,key_results=keywordResults)
        return state