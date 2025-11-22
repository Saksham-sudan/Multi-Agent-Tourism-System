# AI Tourism Assistant

A multi-agent AI tourism system built with LangChain that helps users plan trips, check weather conditions, and discover tourist attractions through natural language conversation.

**Created by:** Saksham Sudan (USN-1CR22IS129)  
**Assignment:** Inkle AI Intern Assignment

## Live Demo

[View Live App on Streamlit Cloud](https://multi-agent-tourism-system-7yysesgfr9mowtr3xmeaba.streamlit.app)

## Features

### Multi-Agent Architecture
- **Orchestrator Agent**: Main conversational interface that delegates tasks to specialized agents
- **Weather Agent**: Handles weather-related queries using Open-Meteo API
- **Places Agent**: Discovers tourist attractions using Overpass API
- **Conversation Memory**: Maintains context across multiple conversation turns

### Technical Capabilities
- Natural language understanding powered by GPT-4o (via GitHub Models)
- Real-time weather data fetching
- Tourist attraction recommendations for any city
- Context-aware responses (e.g., "What's the weather there?" after mentioning a city)
- Clean web interface built with Streamlit

## APIs Used

All APIs used in this project are free and require no authentication:

- **Open-Meteo API**: Weather forecasting and current conditions
- **Overpass API**: OpenStreetMap data for tourist attractions
- **Nominatim API**: Geocoding service to convert city names to coordinates

## Project Structure

```
ai-tourism-system/
├── agents/
│   ├── __init__.py
│   ├── langchain_agent.py    # Orchestrator agent with memory
│   └── sub_agents.py          # Weather and Places specialized agents
├── tools/
│   ├── __init__.py
│   └── custom_tools.py        # API integration tools
├── .streamlit/
│   └── secrets.toml           # Streamlit secrets (gitignored)
├── app.py                     # Streamlit web interface
├── main.py                    # CLI interface
├── requirements.txt           # Python dependencies
├── .env                       # Local environment variables (gitignored)
└── .gitignore                 # Git ignore rules
```

## Installation

### Prerequisites
- Python 3.11 or higher
- GitHub account with access to GitHub Models
- Git

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Saksham-sudan/Multi-Agent-Tourism-System.git
   cd Multi-Agent-Tourism-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```
   
   Or for Streamlit, create `.streamlit/secrets.toml`:
   ```toml
   GITHUB_TOKEN = "your_github_token_here"
   ```

4. **Get your GitHub Token**
   - Visit https://github.com/marketplace/models
   - Sign up for GitHub Models access
   - Generate a Personal Access Token with access to GitHub Models

## Usage

### Web Interface (Streamlit)

Run the Streamlit app:
```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### Command Line Interface

Run the CLI version:
```bash
python main.py
```

### Example Conversations

**Example 1: Trip Planning**
```
You: Plan a trip to Paris
AI: [Lists 5+ tourist attractions in Paris]

You: What's the weather there?
AI: [Provides current weather for Paris]
```

**Example 2: Weather Query**
```
You: What's the weather in Tokyo?
AI: In Tokyo it's currently 15°C with a chance of 20% to rain.
```

## Deployment

### Deploy to Streamlit Community Cloud

1. Push your code to GitHub
2. Visit https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app" and select your repository
5. Set main file path to `app.py`
6. Add your `GITHUB_TOKEN` in the Secrets section:
   ```toml
   GITHUB_TOKEN = "your_token_here"
   ```
7. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app`

## Technical Implementation

### Agent Architecture

The system uses a hierarchical multi-agent architecture:

1. **User Input** → **Orchestrator Agent** (with ConversationBufferMemory)
2. **Orchestrator** determines intent and delegates to:
   - **Weather Agent** → `get_weather` tool → Open-Meteo API
   - **Places Agent** → `get_places` tool → Overpass API

Both specialized agents use the `get_coordinates` function (Nominatim API) to geocode city names.

### Key Technologies

- **LangChain 0.3.0**: Agent framework and orchestration
- **OpenAI GPT-4o**: Language model (via GitHub Models)
- **Streamlit 1.40.0**: Web interface
- **Pydantic**: Data validation
- **Requests**: HTTP client for API calls

### Memory Management

The Orchestrator uses `ConversationBufferMemory` to maintain conversation history, enabling context-aware responses across multiple turns.

## Error Handling

- Graceful handling of non-existent cities
- Informative error messages for API failures
- Validates environment variables on startup
- Handles missing or limited data gracefully

## Author

**Saksham Sudan**  
USN: 1CR22IS129  
Assignment: Inkle AI Intern Position

## Acknowledgments

- Inkle for the assignment opportunity

