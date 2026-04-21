from typing import TypedDict,List,Dict
import numpy as np
class State(TypedDict):
    link:str
    query:str
    Cleanedquery:str
    TitledQuery:str
    vedioTitle:str
    isEnglishAvailable:bool
    originalTranscript:str
    EnglishTranscript:str
    SimilaritySearchResults:List[Dict]
    KeywordSearchResults:List[Dict]
    MergeResults:List[Dict]
    chunks:List[str]
    embeddings:np.ndarray
    rerankedDocuments:List[Dict]

    