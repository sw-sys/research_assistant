from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# wikipedia

# duckduckgo
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    # helps the agent decide when to use the tool
    description="Search the web for information"
)
# custom tool
