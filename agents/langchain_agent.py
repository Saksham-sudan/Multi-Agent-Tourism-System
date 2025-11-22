import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from agents.sub_agents import ask_weather_agent, ask_places_agent
from langchain.memory import ConversationBufferMemory

class LangChainAgent:
    def __init__(self):
        api_key = os.environ.get("GITHUB_TOKEN")
        if not api_key:
            raise ValueError("GITHUB_TOKEN environment variable is not set. Please set it to use the agent.")

        # Initialize ChatOpenAI for GitHub Models
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=api_key,
            base_url="https://models.inference.ai.azure.com",
            temperature=0
        )
        
        # Define tools for the Orchestrator
        self.tools = [
            Tool(
                name="WeatherAgent",
                func=ask_weather_agent,
                description="Useful for answering questions about weather, temperature, rain, or climate. Input should be the full question."
            ),
            Tool(
                name="PlacesAgent",
                func=ask_places_agent,
                description="Useful for answering questions about tourist attractions, places to visit, sightseeing, or trip planning. Input should be the full question."
            )
        ]
        
        # Initialize Memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Initialize the Orchestrator Agent
        self.agent_executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, # Supports chat history
            verbose=True,
            handle_parsing_errors=True,
            memory=self.memory
        )

    def handle_request(self, user_input):
        try:
            # The Orchestrator decides which tool (sub-agent) to call
            result = self.agent_executor.invoke({"input": user_input})
            return result["output"]
        except Exception as e:
            return f"An error occurred while processing your request: {e}"
