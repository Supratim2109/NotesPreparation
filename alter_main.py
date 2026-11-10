from pathlib import Path
from pydantic import BaseModel
from langchain.agents import create_agent
from dotenv import load_dotenv  
from tools import web_seacrh
import os

load_dotenv()


class NotesStructure(BaseModel):
    topic: str
    summary: str
    contents: str
    examples: str
    rememberPoints: str
    reference: str


# Load system prompt
system_prompt = (
    Path(__file__).parent / "prompts" / "system_prompt.txt"
).read_text(encoding="utf-8")


print("1. System prompt loaded")
print("--------------------------------")
print(system_prompt[:500])
print("--------------------------------")


# Create agent
try:
    agent = create_agent(
        model=os.getenv("GOOGLE_GEMINI_MODEL"),
        system_prompt=system_prompt,
        tools=[web_seacrh.search_web],
        response_format=NotesStructure,
    )

    print("2. Agent created successfully")

except Exception as e:
    print("❌ Agent creation failed")
    print(type(e).__name__)
    print(e)
    raise


# Invoke agent
query = "Transformers in AI"

try:
    print("\n3. Invoking agent...")
    print("Query:", query)

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )

    print("\n4. Agent invocation successful")
    print("--------------------------------")
    print("Response type:")
    print(type(response))

    print("\nResponse:")
    print(response)

except Exception as e:
    print("\n❌ Agent invocation failed")
    print("--------------------------------")
    print("Exception type:")
    print(type(e).__name__)
    print("Exception:")
    print(e)

    import traceback
    traceback.print_exc()