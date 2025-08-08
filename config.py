from pydantic import BaseModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai import Agent
from prompt import SYSTEM_PROMPT
from playwright.async_api import Page
import os
from dotenv import load_dotenv
load_dotenv()

with open("/mnt/a/downloads/Lin_Mei_Experiened_Level_Software.pdf", "rb") as f:
    b64 = f.read()

class Item(BaseModel):
    label: str
    type: str
    id: str
    answer: str 

provider = GoogleProvider(api_key=f"{os.getenv("GOOGLE_GEMINI_API_KEY")}")
model = GoogleModel('gemini-2.5-flash', provider=provider)
Profile_agent = Agent(model, system_prompt=SYSTEM_PROMPT, deps_type=Page, output_type=list[Item])
