import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from tools.custom_tools import get_weather, get_places

def _get_llm():
    api_key = os.environ.get("GITHUB_TOKEN")
    if not api_key:
        raise ValueError("GITHUB_TOKEN environment variable is not set.")
    
    return ChatOpenAI(
        model="gpt-4o",
        api_key=api_key,
        base_url="https://models.inference.ai.azure.com",
        temperature=0
    )

def create_weather_agent():
    """Creates the specialized Weather Agent."""
    llm = _get_llm()
    tools = [get_weather]
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "system_message": "You are a specialized Weather Agent. You MUST use the 'get_weather' tool to fetch accurate weather information. Do not guess or use your own knowledge."
        }
    )
    return agent

def create_places_agent():
    """Creates the specialized Tourism/Places Agent."""
    llm = _get_llm()
    tools = [get_places]
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "system_message": "You are a specialized Tourism Agent. You MUST use the 'get_places' tool to find tourist attractions. Do not guess or use your own knowledge."
        }
    )
    return agent



def ask_weather_agent(query: str) -> str:
    """
    Useful for answering questions about weather, temperature, rain, or climate.
    Input should be a full natural language question or instruction regarding weather.
    """
    try:
        agent = create_weather_agent()
        return agent.run(query)
    except Exception as e:
        return f"Weather Agent failed: {e}"

def ask_places_agent(query: str) -> str:
    """
    Useful for answering questions about tourist attractions, places to visit, sightseeing, or trip planning.
    Input should be a full natural language question or instruction regarding places.
    """
    try:
        agent = create_places_agent()
        return agent.run(query)
    except Exception as e:
        return f"Places Agent failed: {e}"
