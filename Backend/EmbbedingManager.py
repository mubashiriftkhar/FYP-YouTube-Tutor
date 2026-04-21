from typing import List
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
import cohere
from Backend.state import State
from Backend.BaseClass import BaseClass
from Backend.client import cohereClient
class EmbeddingManager(BaseClass):
    """
    Handles real-time chunking and embedding using Cohere embeddings.
    """

    def __init__(self):
        self.model = "embed-english-v3.0"
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

    def create_chunks(self, transcript: str) -> List[str]:
        """Split transcript into overlapping chunks using LangChain splitter."""
        chunks = self.text_splitter.split_text(transcript)
        print(chunks)
        print(type(chunks))
        return chunks

    def create_embeddings(self, chunks: List[str]) -> np.ndarray:
        """Embed chunks using Cohere model."""
        response = cohereClient.embed(texts=chunks,input_type = "search_query", model=self.model, embedding_types=["float"])
        embeddings = np.array(response.embeddings.float_, dtype=np.float32)
        return embeddings
    def execute(self,state:State) -> State:
        transcript=state["EnglishTranscript"]
        chunks=self.create_chunks(transcript=transcript)
        embeddings=self.create_embeddings(chunks=chunks)
        state["chunks"]=chunks
        state["embeddings"]=embeddings
        return embeddings
