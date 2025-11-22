# from agents.parent_agent import ParentAgent
from agents.langchain_agent import LangChainAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    print("Welcome to the AI Tourism System (LangChain Edition)!")
    
    if not os.environ.get("GITHUB_TOKEN"):
        print("Error: GITHUB_TOKEN environment variable not set.")
        print("Please set it to run this application.")
        return

    try:
        agent = LangChainAgent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            response = agent.handle_request(user_input)
            print(f"AI: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
