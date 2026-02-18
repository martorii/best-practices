# AI Chat Assistant with ReAct Agent

A complete chat assistant system with a beautiful Apple-style UI, powered by Google's Gemini LLM and a ReAct agent with MCP (Model Context Protocol) tools.

## 🎯 Features

- **Apple-style UI**: Beautiful Streamlit frontend with Apple-inspired design
- **ReAct Agent**: LangChain-based agent that can reason and use tools
- **MCP Tools**: Calculator, weather, and time tools via MCP server
- **Real-time Streaming**: See the agent's thinking process in real-time
- **Docker Compose**: Easy deployment with three containerized services

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │  Streamlit (Port 8501)
│   (Streamlit)   │  Apple-style UI
└────────┬────────┘
         │
         │ HTTP/SSE
         ▼
┌─────────────────┐
│   Backend       │  FastAPI (Port 8000)
│   (FastAPI)     │  ReAct Agent + LangChain
└────────┬────────┘
         │
         │ Tool Calls
         ▼
┌─────────────────┐
│   MCP Server    │  Python MCP Server
│   (Python)      │  Calculator, Weather, Time
└─────────────────┘
```

## 📁 Project Structure

```
chat-assistant-system/
├── frontend/
│   ├── app.py              # Streamlit application
│   ├── Dockerfile
│   └── requirements.txt
├── backend/
│   ├── main.py             # FastAPI + ReAct agent
│   ├── Dockerfile
│   └── requirements.txt
├── mcp-server/
│   ├── server.py           # MCP server with tools
│   ├── Dockerfile
│   └── requirements.txt
├── docker compose.yml      # Orchestration
├── .env.example           # Environment template
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Google API Key for Gemini ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone and navigate to the project**
   ```bash
   cd chat-assistant-system
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

3. **Build and start all services**
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Testing

To test individual components:

**Backend API:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 25 * 4?"}'
```

**List Available Tools:**
```bash
curl http://localhost:8000/tools
```

## 🛠️ Available Tools

The MCP server provides three tools:

1. **Calculator** (`calculate`)
   - Perform mathematical calculations
   - Example: "What is 25 * 4 + 10?"

2. **Weather** (`get_weather`)
   - Get weather information for cities
   - Example: "What's the weather in London?"

3. **Current Time** (`get_current_time`)
   - Get current date and time
   - Example: "What time is it in UTC?"

## 💡 How It Works

### ReAct Agent Flow

1. **User Input**: User types a message in the Streamlit UI
2. **Backend Processing**: FastAPI receives the request
3. **Agent Reasoning**: LangChain ReAct agent analyzes the query
4. **Tool Selection**: Agent decides which MCP tools to use
5. **Tool Execution**: Tools are called via the MCP server
6. **Response Streaming**: Results are streamed back to the UI
7. **Display**: UI shows the agent's thinking process and final answer

### Streaming Implementation

The system uses Server-Sent Events (SSE) to stream:
- Agent thoughts
- Tool usage
- Intermediate results
- Final answers

## 🎨 UI Components

The frontend includes:
- **Chat bubbles**: User (blue) and Assistant (white)
- **Tool indicators**: Shows when tools are being used
- **Thinking indicators**: Shows agent reasoning
- **Timestamps**: For each message
- **Smooth animations**: Slide-in effects for messages

## 🔧 Development

### Running Services Individually

**MCP Server:**
```bash
cd mcp-server
pip install -r requirements.txt
python server.py
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Adding New MCP Tools

1. Edit `mcp-server/server.py`
2. Add tool to `list_tools()` function
3. Implement tool logic in `call_tool()` function
4. Update backend's `create_langchain_tools()` to expose the new tool

### Customizing the UI

Edit `frontend/app.py` and modify the CSS in the `st.markdown()` section to customize:
- Colors
- Fonts
- Layout
- Animations

## 📊 Monitoring

View logs for each service:

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f frontend
docker compose logs -f backend
docker compose logs -f mcp-server
```

## 🐛 Troubleshooting

**Backend can't connect to MCP server:**
- Ensure all services are in the same Docker network
- Check `docker compose logs mcp-server`

**Frontend can't reach backend:**
- Verify backend is healthy: `curl http://localhost:8000/health`
- Check network configuration in docker compose.yml

**Gemini API errors:**
- Verify your API key is correct in `.env`
- Check API quota at Google Cloud Console

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- Use environment variables for all secrets
- In production, use proper authentication
- Limit MCP tool capabilities as needed

## 📚 Technologies Used

- **Frontend**: Streamlit, Custom CSS
- **Backend**: FastAPI, LangChain, Google Gemini
- **MCP Server**: Python MCP SDK
- **Infrastructure**: Docker, Docker Compose
- **LLM**: Google Gemini 2.0 Flash

## 🚢 Deployment

For production deployment:

1. Use a reverse proxy (nginx/Traefik)
2. Add HTTPS/SSL certificates
3. Set up proper logging and monitoring
4. Use secrets management (Vault, AWS Secrets Manager)
5. Configure rate limiting
6. Add user authentication

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions:
- Open a GitHub issue
- Check existing documentation
- Review logs for error messages

---

Built with ❤️ using LangChain, Gemini, and MCP
