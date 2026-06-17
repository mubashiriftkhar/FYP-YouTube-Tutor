# import asyncio
from Backend.state import State
from Backend.Transcript import Trancript
from Backend.EmbbedingManager import EmbeddingManager
from Backend.SimilaritySearch import SimilaritySearch
from Backend.KeywordSearch import KeywordSearch
from Backend.Merger import MergeSearches
from Backend.Reranker import Reranker
# from Backend.QueryCleaner import Querycleaner
# from Backend.GetAnswer import results
# from Backend.SummarizerAgent import Summarizer
# import multiprocessing
# from multiprocessing import Pool, cpu_count, Manager, freeze_support

def execute_stage(args):
    cls, state = args
    cls.execute(state)
    return True


class orchestrator():
    def __init__(self):
        self.pipeline_1 = [
            Trancript(),       
            EmbeddingManager(),  
                     
        ]
        self.pipeline_2=[
            # Querycleaner(),
            SimilaritySearch(),          
            KeywordSearch(),             
            MergeSearches(),             
            Reranker()  
        ]
    
        # self.pipeline_3=[
        #      Summarizer(),
        # ]
    def pipeline_1_execute(self, state: State):
        for node in self.pipeline_1:
            print(f"Running {node.__class__.__name__}")
            node.execute(state)
            if not state.get("isEnglishAvailable", True):
                return {"Massage":f"English Transcript of video {state.get('vedioTitle','Unknown')} is not available."}
        # return state

    def pipline_2_execute(self,state:State):
        for node in self.pipeline_2:
            print(f"Running {node.__class__.__name__}")
            node.execute(state)
            if not state.get("isEnglishAvailable", True):
                return {"Massage":f"English Transcript of video {state.get('vedioTitle','Unknown')} is not available."}
        
    # def pipeline_3_execute(self,state:State)->State:
    #     for node in self.pipeline_2:
    #         print(f"Running {node.__class__.__name__}")
    #         node.execute(state)
    #     return state
            


# if __name__ == "__main__":
#     # freeze_support()  # ✅ Required on Windows for multiprocessing
#     # manager = Manager()
#     sample_state = {
#         "link":"https://youtu.be/62wEk02YKs0",
#         "query": "What this Video is Explaining?",
#         "vedioTitle": "",
#         "TitledQuery":"",
#         "isEnglishAvailable": True,
#         # "originalTranscript": "",
#         "EnglishTranscript": "",
#         "SimilaritySearchResults": [],
#         "KeywordSearchResults": [],
#         "MergeResults": [],
#         "chunks": [],
#         "embeddings": [],
#         "rerankedDocuments": []
#     }

#     orch=orchestrator()
#     finalState=orch.execute(state=sample_state)
#     # output=asyncio.run(results(finalState))
#     # print(output)
#     for key, val in finalState.items():
#         print(f"{key} : {val}")