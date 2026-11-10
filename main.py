from dotenv import load_dotenv
import fastapi
from pydantic import BaseModel
from langchain.agents import create_agent
from pathlib import Path
from fastapi import FastAPI
from tools import web_seacrh
import os

app = FastAPI()

load_dotenv()

class NotesStructure(BaseModel):
    topic: str
    summary: str
    contents: str
    examples: str
    rememberPoints: str
    reference:str
    
class topicRequest(BaseModel):
    topic:str




system_prompt = (Path(__file__).parent/"prompts"/"system_prompt.txt").read_text(encoding="utf-8")

agent =  agent = create_agent(
        model=os.getenv("GOOGLE_GEMINI_MODEL"),
        system_prompt=system_prompt,
        tools=[web_seacrh.search_web],
        response_format=NotesStructure,
    )

@app.post("/internal/topic/")
def create_notes(topic:topicRequest):
    try:
        response = agent.invoke({"messages": {"role":"user", "content":f"{topic.topic}"}})
        print(response["structured_response"])
        return response["structured_response"]
    except Exception as e:
        print(f"Response cannot be fetched: {e}")