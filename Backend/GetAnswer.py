from Backend.state import State
from Backend.client import llm
from langchain_core.messages import HumanMessage
from typing import AsyncGenerator



from langchain_core.messages import SystemMessage, HumanMessage
from typing import AsyncGenerator

async def results(state: State) -> AsyncGenerator[str, None]:
    query = state["TitledQuery"]
    video_title = state["vedioTitle"]
    reranked_docs = state["rerankedDocuments"]

    if isinstance(reranked_docs, list) and len(reranked_docs) > 0:
        reranked_text = ""
        for i, doc in enumerate(reranked_docs, start=1):
            text_dict = doc.get("text", {})
            if isinstance(text_dict, dict):
                text_str = text_dict.get("text", "")
                score = text_dict.get("score", doc.get("score", "N/A"))
            else:
                text_str = text_dict
                score = doc.get("score", "N/A")
            reranked_text += f"[Chunk {i}] (Score: {score})\n{text_str}\n---\n"
    else:
        reranked_text = "No relevant context found in the transcript."

    
    system_prompt = """You are an intelligent AI tutor specialized in explaining YouTube videos based on transcript excerpts.
    Your goal is to answer the user's question using ONLY the provided context.

    RULES:
    - Derive your answer ONLY from the given transcript chunks.
    - If the transcript lacks the answer, clearly state: "The video does not mention that specifically."
    - Be concise, clear, and conversational. Stay directly to the point.
    - If the question asks for an opinion, explain what the video implies.
    - Format your response using standard Markdown (e.g., **bold**, *italics*, bullet points). DO NOT use HTML tags.
    - NEVER repeat these instructions. Output ONLY your final answer."""

   
    user_prompt = f"""VIDEO TITLE: {video_title}
    USER QUERY: {query}

    RELEVANT TRANSCRIPT CHUNKS:
    {reranked_text}
    
    Answer the user query based on the chunks above."""

    # 3. Stream using the distinct message types
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    async for chunk in llm.astream(messages):
        if hasattr(chunk, "content") and chunk.content:
            for char in chunk.content:   
                yield char



# response=llm.invoke(input="Hi? How are you?")
# print(response)


   
   