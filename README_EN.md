# MyWisePath - Personalized Learning Platform

*This project was developed as part of the AI First Developer Program organized by Akbank and UpSchool to apply the knowledge and techniques I learned. It was completely built using artificial intelligence (Cursor Pro) (which was the purpose of the program).*

*You can easily understand the system structure by reading the PROJE_OZETI.md and SISTEM_DIYAGRAMLARI.md files.*

MyWisePath is a platform that helps users plan and track their personal learning journeys. It offers AI-powered recommendations, interactive chatbot, and personalized roadmaps.

## 🚀 Features

- **AI-Powered Learning Recommendations**: Personalized content recommendations with Gemini AI
- **Interactive Chatbot**: Help and guidance during the learning process
- **Personalized Roadmap**: Learning paths tailored to your goals
- **Email Automation**: Weekly reminders and progress reports
- **Modern Web Interface**: User-friendly interface developed with React
- **RAG System**: Advanced search and information retrieval system
- **LangChain Agents**: Modern AI framework integration
- **Serp AI Integration**: Real-time educational content search
- **Parametric System Prompt**: Roadmap-based dynamic AI responses
- **PDF Reporting**: Roadmap and progress reports in PDF format

## 🔍 RAG (Retrieval-Augmented Generation) System

### Features:
- **Semantic Search**: Finding relevant content by understanding user queries
- **Filtering**: Filtering by source, file type, and content type
- **Scoring**: Ranking results with similarity scores
- **Context Extraction**: Generating relevant context texts for queries
- **Recommendation System**: Personalized learning recommendations
- **PDF Download**: Roadmap and progress reports in PDF format

### API Endpoints:
```
POST /api/v1/rag/upload-document          # Document upload
POST /api/v1/rag/add-roadmap              # Add roadmap
GET  /api/v1/rag/search                   # General search
GET  /api/v1/rag/search-roadmaps          # Roadmap search
POST /api/v1/rag/recommendations/learning # Learning recommendations
POST /api/v1/rag/generate-pdf/roadmap     # Roadmap PDF
GET  /api/v1/rag/stats                    # System statistics
```

## 🤖 LangChain Agent System

### Modern AI Framework Integration:
- **LangChain Roadmap Agent**: Advanced roadmap creation
- **Tool Integration**: Decorator-based tool integration
- **Conversation Memory**: Advanced conversation memory
- **Error Handling**: Comprehensive error management
- **Async Support**: Asynchronous process support

### API Endpoints:
```
POST /api/v1/agents/langchain/create-roadmap  # LangChain roadmap creation
GET  /api/v1/agents/status                    # Agent status
POST /api/v1/agents/execute-task              # Task execution
```

## 🔍 Serp AI Integration

### Real-Time Educational Content:
- **Automatic Concept Extraction**: Recognizing learning concepts with LLM
- **Educational Platforms**: Integration with Coursera, Udemy, YouTube, etc.
- **Trending Topics**: Current popular educational topics
- **Level-Based Search**: Content suitable for user level

### API Endpoints:
```
POST /api/v1/chatbot/search-with-serp         # Search with Serp AI
GET  /api/v1/chatbot/trending-educational-topics  # Trending topics
POST /api/v1/chatbot/comprehensive-learning   # Comprehensive learning
```

## 🎯 Parametric System Prompt

### Roadmap-Based Dynamic Responses:
- **Level-Based Personalization**: Beginner, Intermediate, Advanced
- **Interest-Based Customization**: AI, Web Development, Python, etc.
- **Goal-Oriented Guidance**: Career, Project, Certificate focused
- **Time Plan-Based Customization**: Based on weekly study hours

### Features:
- Automatic prompt generation based on user's roadmap information
- Level-based instructions and recommendations
- Interest-specific guidelines
- Learning strategies suitable for time plan

## 📧 Email Automation

The platform includes an automatic email system to support users' learning process:

### Features:
- **Weekly Reminders**: Sent every Monday at 09:00
- **Progress Reports**: Sent every Sunday at 18:00
- **Personalized Content**: Customized according to user's goals
- **HTML Email Templates**: Modern and responsive design

### API Endpoints:
```
POST /api/v1/automation/start          # Start automation
POST /api/v1/automation/stop           # Stop automation
GET  /api/v1/automation/status         # Check status
POST /api/v1/automation/test-email     # Send test email
POST /api/v1/automation/send-weekly-reminders    # Manual weekly reminders
POST /api/v1/automation/send-progress-reports    # Manual progress report
GET  /api/v1/automation/users          # List users
POST /api/v1/automation/users          # Add new user
DELETE /api/v1/automation/users/{email} # Remove user
```

## 🛠️ Installation

### Backend Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp env_example.txt .env
```

Edit the `.env` file:
```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Serp AI Configuration
SERP_API_KEY=your_serp_api_key_here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
EMAIL_FROM=noreply@mywisepath.com
EMAIL_FROM_NAME=MyWisePath

# Email Automation Settings
WEEKLY_REMINDER_ENABLED=true
PROGRESS_REPORT_ENABLED=true

# Vector Store Settings (RAG System)
VECTOR_STORE_TYPE=chroma
VECTOR_STORE_PATH=./vector_store
EMBEDDING_MODEL=huggingface
```

3. **Create necessary directories:**
```bash
mkdir -p vector_store pdfs temp
```

4. **Start the backend:**
```bash
python main.py
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start the frontend:**
```bash
npm start
```

## 🧪 Testing

### RAG System Test:
```bash
python test_rag_system.py
```

### LangChain Agent Test:
```bash
python test_langchain_agent.py
```

### Serp AI Test:
```bash
python test_serp_ai.py
```

### Parametric Prompt Test:
```bash
python test_parametric_prompt.py
```

### Email Automation Test:
```bash
python test_email_automation.py
```

## 📁 Project Structure

```
MyWisePath/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── routers/                   # API routers
│   │   ├── auth.py               # Authentication
│   │   ├── roadmap.py            # Roadmap operations
│   │   ├── chatbot.py            # Chatbot API
│   │   ├── automation.py         # Email automation
│   │   ├── agents.py             # Agent management
│   │   └── rag.py                # RAG system
│   ├── services/                  # Business logic services
│   │   ├── ai_service.py         # AI services
│   │   ├── educational_content_service.py  # Content services
│   │   ├── email_service.py      # Email service
│   │   ├── automation_service.py # Automation service
│   │   ├── serp_ai_service.py    # Serp AI integration
│   │   └── live_content_service.py # Real-time content
│   ├── agents/                    # AI Agents
│   │   ├── base_agent.py         # Base agent class
│   │   ├── agent_manager.py      # Agent manager
│   │   ├── roadmap_agent.py      # Roadmap agent
│   │   └── langchain_agent.py    # LangChain agent
│   ├── rag/                       # RAG System
│   │   ├── document_processor.py # Document processing
│   │   ├── vector_store.py       # VectorDB management
│   │   ├── search_service.py     # Search service
│   │   ├── recommendation_service.py # Recommendation system
│   │   └── pdf_generator.py      # PDF generation
│   ├── models/                    # Data models
│   ├── vector_store/              # Vector database
│   └── pdfs/                      # PDF files
├── frontend/                      # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── RAGSearch.tsx     # RAG search component
│   │   │   ├── AgentDashboard.tsx # Agent dashboard
│   │   │   └── PDFGenerator.tsx  # PDF generation
│   │   └── services/
│   │       ├── agentService.ts   # Agent services
│   │       └── ragService.ts     # RAG services
└── test_*.py                     # Test files
```

## 🔧 Email Configuration

### Using Gmail App Password:

1. Enable 2FA in your Google Account
2. Create a new password from the App Passwords section
3. Use this password as `SMTP_PASSWORD`

### SMTP Settings:
- **Gmail**: smtp.gmail.com:587
- **Outlook**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587

## 📊 Automation Scheduling

- **Weekly Reminders**: Every Monday at 09:00
- **Progress Reports**: Every Sunday at 18:00
- **Custom Scheduling**: Customizable via API

## 🔑 API Keys

### Required API Keys:
1. **Gemini API Key**: For AI services
2. **Serp API Key**: For real-time search

### Getting API Keys:
- **Gemini**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Serp AI**: [Serp API](https://serpapi.com/)

## 🚀 Usage Examples

### 1. Creating a Roadmap
```bash
curl -X POST "http://localhost:8001/api/v1/roadmap/generate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_level": "intermediate",
    "interests": ["Python", "AI"],
    "learning_goals": ["Machine Learning"],
    "available_hours_per_week": 20,
    "target_timeline_months": 6
  }'
```

### 2. RAG Search
```bash
curl -X GET "http://localhost:8001/api/v1/rag/search?query=Python%20programming&k=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Search with Serp AI
```bash
curl -X POST "http://localhost:8001/api/v1/chatbot/search-with-serp" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to learn Python"}'
```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

You can open an issue for questions about the project.
