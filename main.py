from dotenv import load_dotenv
from pydantic import BaseModel
from langchain.agents import create_agent
from pathlib import Path
from tools import web_seacrh
import os


load_dotenv()

class NotesStructure(BaseModel):
    topic: str
    summary: str
    contents: str
    examples: str
    rememberPoints: str
    reference:str




system_prompt = (Path(__file__).parent/"prompts"/"system_prompt.txt").read_text(encoding="utf-8")

agent =  agent = create_agent(
        model=os.getenv("GOOGLE_GEMINI_MODEL"),
        system_prompt=system_prompt,
        tools=[web_seacrh.search_web],
        response_format=NotesStructure,
    )

query = "Transformers in AI"



try:
    response = agent.invoke({"messages": {"role":"user", "content":f"{query}"}})
    print(response["structured_response"])
except Exception as e:
    print("Response cannot be fetched")