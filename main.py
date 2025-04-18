# Activate venv with '.\venv\Scripts\activate' for Windows
# Docs https://python.langchain.com/docs/integrations/providers/anthropic/
# model summary https://docs.anthropic.com/en/docs/about-claude/models/all-models
# langchain prompt docs https://python.langchain.com/docs/concepts/prompt_templates/
# tool docs
# langchain community hub
# langchain tuts https://python.langchain.com/docs/tutorials/
# langchain how tos https://python.langchain.com/docs/how_to/
# duckduckgo-search https://pypi.org/project/duckduckgo-search/

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

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

# Set the research response format
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# prompt context
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query by using neceassary tools where appropriate.
            Wrap the output in this format and provide no other text {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),  # coming from the user
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# create tool calling agent
tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

# execute the agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
raw_response = agent_executor.invoke(
    {"query": input("Enter your topic to research: ")})
# print(raw_response)

# parse the raw_response in to the ResearchResponse structure
try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw response content: ", raw_response)
