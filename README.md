# EduBridge AI

AI-powered educational platform featuring multiple specialized AI agents for personalized learning assistance.

## 🚀 Features

- **Roadmap Architect**: Creates structured learning paths and curricula
- **Lecturer**: Provides academic explanations and answers student inquiries
- **Support Assistant**: Handles user support and platform assistance
- **YouTube Integration**: Recommends relevant educational videos
- **Chat History**: Persistent conversation storage with Supabase
- **Streaming Responses**: Real-time AI responses

## 📁 Project Structure

```
EduBridge_Ai4/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (configure API keys)
├── .gitignore              # Git ignore rules
├── app/
│   ├── __init__.py
│   ├── schemas.py          # Pydantic models for API requests/responses
│   ├── storage.py          # AI clients, YouTube API, and Supabase setup
│   ├── middleware/
│   │   └── timer.py        # Request timing middleware
│   └── routes/
│       └── issues.py       # API endpoints for AI agents
└── .venv/                  # Virtual environment (created during setup, ignored by Git)
```

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python web framework)
- **AI Models**: DeepSeek-R1, Llama-3.1-8B (via SiliconFlow & Groq)
- **Database**: Supabase (PostgreSQL)
- **Video Integration**: YouTube Data API v3
- **Authentication**: API key-based
- **Deployment**: Uvicorn ASGI server

## 📋 Prerequisites

- Python 3.8+
- Git
- API Keys for:
  - SiliconFlow (DeepSeek models)
  - Groq (Llama models)
  - YouTube Data API
  - Supabase

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd EduBridge_Ai4
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the `.env` file and configure your API keys:

```bash
# Required API Keys
SILICONFLOW_API_KEY="your_siliconflow_api_key"
GROQ1_API_KEY="your_groq_api_key"
GROQ2_API_KEY="your_groq_api_key"
YOUTUBE_API_KEY="your_youtube_api_key"

# Supabase Configuration
SUPABASE_URL="your_supabase_project_url"
SUPABASE_KEY="your_supabase_anon_key"
```

## ▶️ Running the Application

### Development Mode
```bash
python main.py
```

The API will be available at: `http://localhost:8080`

### Alternative (using uvicorn directly)
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## 📡 API Endpoints

### Health Check
- **GET** `/` - Check API status

### AI Agents

#### Roadmap Architect
- **POST** `/api/v1/chat/roadmap_architect`
- Creates learning roadmaps and curricula
- Includes YouTube video recommendations

#### Lecturer
- **POST** `/api/v1/chat/Lecturer`
- Provides academic explanations and answers

#### Support Assistant
- **POST** `/api/v1/chat/support`
- Handles user support queries

### Request Format
```json
{
  "user_id": "string",
  "message": "string",
  "history": []
}
```

## 🔧 Development

### Project Structure Details

- **`main.py`**: FastAPI app initialization, CORS setup, route inclusion
- **`app/schemas.py`**: Data models for chat requests and responses
- **`app/storage.py`**: External service integrations (AI clients, YouTube, Supabase)
- **`app/routes/issues.py`**: AI agent endpoints with streaming responses
- **`app/middleware/timer.py`**: Performance monitoring middleware

### Adding New AI Agents

1. Define agent persona in `app/routes/issues.py`
2. Create new endpoint with `@router.post("/agent_name")`
3. Implement chat logic with appropriate AI client
4. Add database persistence for conversations

## 📝 Notes

- The application uses streaming responses for real-time AI interactions
- Chat history is automatically saved to Supabase
- YouTube videos are recommended based on user queries
- All AI agents run asynchronously for better performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 EduBridge AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```