from Backend.state import State
from Backend.BaseClass import BaseClass
from typing import List,Dict
from Backend.client import cohereClient

class Reranker(BaseClass):
    def rerank(self, query: str, documents: List[str], top_k: int = 5) -> List[Dict]:
        response = cohereClient.rerank(
            model="rerank-english-v3.0",
            query=query,
            documents=documents,
            top_n=top_k
        )

        results = [
            {
                "text": documents[r.index],  # original document
                "relevance_score": r.relevance_score,
                "rank": i + 1  # rank in the reranked order
            }
            for i, r in enumerate(response.results)
        ]
        return results
    def execute(self, state:State) -> State:
        query=state["TitledQuery"]
        documents=state["MergeResults"]
        rerankedDocuments=self.rerank(query=query,documents=documents)
        state["rerankedDocuments"]=rerankedDocuments
        return state
