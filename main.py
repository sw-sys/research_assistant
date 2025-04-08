# Activate venv with '.\venv\Scripts\activate' for Windows
# Docs https://python.langchain.com/docs/integrations/providers/anthropic/

import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(
    model='claude-3-5-sonnet-20241022',
)

response = llm.invoke("Do geese have teeth?")
print(response)
