# uvicorn app:app --reload --host 0.0.0.0 --port 8000

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from orchestrator import orchestrator
from GetAnswer import results
from SummarizerAgent import Summarizer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
orch = orchestrator()

# In-memory cache {video_link: state_dict}
state = {
        "link":"",
        "query": "",
        "vedioTitle": "",
        "TitledQuery":"",
        "isEnglishAvailable": True,
        "EnglishTranscript": "",
        "SimilaritySearchResults": [],
        "KeywordSearchResults": [],
        "MergeResults": [],
        "chunks": [],
        "embeddings": [],
        "rerankedDocuments": [],

}

class TranscriptRequest(BaseModel):
    url: str
   

class QueryRequest(BaseModel):
    query:str


@app.post("/transcript")
async def transcript_video(request: TranscriptRequest):
    global state
    state["link"]=request.url
    transcript_state = orch.pipeline_1_execute(state)
    if "Message" in transcript_state:
        return transcript_state
    state=transcript_state
    return {"message": "Transcript and embeddings created successfully.", "title": state.get("vedioTitle")}


@app.post("/query")
async def query_video(request: QueryRequest):
    global state
    if state["EnglishTranscript"] =="":
        return {"error": "No transcript found. Please call /transcript first."}
    state["query"]=request.query

    queryState = orch.pipline_2_execute(state)

    async def stream_output():
        async for token in results(queryState):
            yield token

    return StreamingResponse(
    stream_output(),
    media_type="text/plain",
    headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Transfer-Encoding": "chunked",
    },
)

@app.post("/summary")
async def summary():
    global state
    
    if state["EnglishTranscript"] =="":
        return {"error": "No transcript found. Please call /transcript first."}
    summary= Summarizer(state)
    return summary

    