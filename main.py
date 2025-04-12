# Activate venv with '.\venv\Scripts\activate' for Windows
# Docs https://python.langchain.com/docs/integrations/providers/anthropic/
# model summary https://docs.anthropic.com/en/docs/about-claude/models/all-models

import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# specify how LLM should respond


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# define LLM model to respond
llm = ChatAnthropic(
    model='claude-3-7-sonnet-20250219',
)
# Check we can get response from LLM
# print(response=llm.invoke("Do geese have teeth?"))

parser = PydanticOutputParser(pydantic_object=ResearchResponse)
