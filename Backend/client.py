import cohere
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()



llm = ChatOpenAI(
  api_key=os.getenv("OpenRouterKey"),
  base_url="https://openrouter.ai/api/v1",
  model="nvidia/nemotron-3-super-120b-a12b:free",
  streaming=True
)
cohereClient=cohere.ClientV2(os.getenv("Cohere_API_KEY"))

