# Chart Boat - AI Document Intelligence Platform

Chart Boat is a modern AI-powered document intelligence platform that allows users to upload documents and ask questions about their content using advanced natural language processing and vector search capabilities.

## 🚀 Features

### For Administrators
- **Document Management**: Upload, process, and delete documents
- **AI Chat Interface**: Ask questions about all documents with upload capability
- **System Monitoring**: View system health, statistics, and performance metrics
- **User Management**: Oversee all users and document access

### For Regular Users
- **Document Query**: Ask questions about available documents
- **AI-Powered Search**: Get intelligent answers with source citations
- **Clean Interface**: Focused question-answering experience

## 🏗️ Architecture

### Backend (FastAPI + Python)
```
app/
├── api/                    # API endpoints
│   ├── auth.py            # Authentication (login, register, user management)
│   ├── documents.py       # Document management (upload, list, delete)
│   └── search.py          # Search and Q&A functionality
├── core/                  # Core application logic
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection and session management
│   └── security.py        # Security utilities (password hashing, JWT tokens)
├── models/                # Database models and schemas
│   ├── document.py        # Document and DocumentChunk models
│   └── user.py            # User model and authentication schemas
├── services/              # Business logic services
│   ├── chunking.py        # Text chunking for vector storage
│   ├── embeddings.py      # Embedding generation using Azure OpenAI
│   ├── rag.py             # Retrieval-Augmented Generation logic
│   ├── text_extraction.py # Extract text from various document formats
│   └── vector_db.py       # ChromaDB vector database operations
├── utils/                 # Utility functions
│   └── file_utils.py      # File handling operations
└── main.py               # Application entry point
```

### Frontend (React + TypeScript)
```
frontend/src/
├── components/            # React components
│   ├── auth/             # Authentication components
│   │   ├── LoginPage.tsx
│   │   └── RegisterPage.tsx
│   ├── chat/             # Chat interface
│   │   └── ChatInterface.tsx
│   ├── dashboard/        # Dashboard components
│   │   ├── AdminDashboard.tsx
│   │   └── UserDashboard.tsx
│   ├── documents/        # Document management
│   │   └── DocumentUpload.tsx
│   ├── LandingPage.tsx   # Home page
│   └── ProtectedRoute.tsx # Route protection
├── contexts/             # React contexts
│   └── AuthContext.tsx   # Authentication state management
├── services/             # API services
│   └── api.ts            # API communication layer
├── types/                # TypeScript type definitions
│   └── index.ts
├── App.tsx               # Main app component with routing
└── index.tsx             # Application entry point
```

## 🔐 User Roles & Access Control

### Administrator (`admin` role)
- **Routes**: `/admin` (blocked from `/dashboard`)
- **Capabilities**:
  - Upload documents via admin panel or AI chat
  - Delete any document
  - View all system statistics
  - Monitor system health
  - Access admin-only AI chat with upload functionality

### Regular User (`user` role)
- **Routes**: `/dashboard` (blocked from `/admin`)
- **Capabilities**:
  - View all available processed documents (read-only)
  - Ask questions about documents
  - Cannot upload or delete documents

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Database**: SQLite with SQLAlchemy ORM
- **Vector Database**: ChromaDB
- **AI/ML**: Azure OpenAI (GPT-4 + Text Embeddings)
- **Authentication**: JWT tokens with password hashing
- **File Processing**: PyPDF2, python-docx, openpyxl, python-pptx

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Build Tool**: Create React App

## 📋 Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **npm or yarn**
- **Azure OpenAI API access** (GPT-4 and text-embedding models)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd chart-boat
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the root directory:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# Database Configuration
DATABASE_URL=sqlite:///./docbot.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE=2097152  # 2MB in bytes
UPLOAD_DIR=./uploads
```

#### Database Initialization
The database will be automatically created when you first run the application.

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Dependencies
```bash
npm install
```

#### Environment Configuration
Create a `.env` file in the `frontend` directory:
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Running the Application

### Start Backend Server
```bash
# From project root
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Development Server
```bash
# From frontend directory
cd frontend
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 User Workflow

### For First-Time Setup
1. **Access the application** at http://localhost:3000
2. **Register an account** (first user becomes admin)
3. **Login** to access the platform

### Administrator Workflow
1. **Login** → Redirected to `/admin`
2. **Upload Documents**:
   - Via "All Documents" tab in admin panel
   - Via paperclip icon in "AI Chat" tab
3. **Monitor System**: Check "System Health" and "Overview" tabs
4. **Ask Questions**: Use AI Chat with full document access

### User Workflow
1. **Login** → Redirected to `/dashboard`
2. **View Available Documents**: See all processed documents in sidebar
3. **Ask Questions**: Use chat interface to query document content
4. **Review Answers**: Get AI responses with source citations

## 🔄 Document Processing Pipeline

1. **Upload**: Admin uploads document via web interface
2. **Storage**: File saved to `uploads/` directory with unique ID
3. **Text Extraction**: Extract text content based on file type:
   - PDF: PyPDF2
   - Word: python-docx
   - Excel: openpyxl
   - PowerPoint: python-pptx
4. **Chunking**: Split text into manageable chunks with overlap
5. **Embedding Generation**: Create vector embeddings using Azure OpenAI
6. **Vector Storage**: Store embeddings in ChromaDB
7. **Database Update**: Mark document as processed
8. **Availability**: Document becomes available for user queries

## 🔍 Search & Q&A Process

1. **User Query**: User submits question through chat interface
2. **Query Embedding**: Convert question to vector embedding
3. **Vector Search**: Find relevant document chunks in ChromaDB
4. **Context Assembly**: Combine relevant chunks for context
5. **AI Generation**: Generate answer using Azure OpenAI GPT-4
6. **Response Delivery**: Return answer with source citations

## 📁 File & Data Storage

```
project-root/
├── docbot.db              # SQLite database (users, documents metadata)
├── chroma_db/             # ChromaDB vector database
├── uploads/               # Uploaded document files
│   └── [unique-id].pdf    # Documents stored with unique IDs
└── app/                   # Application code
```

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **Role-Based Access**: Strict separation between admin and user capabilities
- **File Validation**: File type and size restrictions
- **CORS Protection**: Configured for frontend domain
- **Input Validation**: Pydantic models for API validation

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Documents (Admin Only)
- `POST /api/documents/upload` - Upload document
- `DELETE /api/documents/{id}` - Delete document
- `GET /api/documents/all` - List all documents (admin)

### Documents (Users)
- `GET /api/documents/available` - List available documents
- `GET /api/documents/` - List user's documents

### Search & Q&A
- `POST /api/search/query` - Ask question and get AI response
- `POST /api/search/search` - Search documents

### System (Admin Only)
- `GET /health` - System health check
- `GET /api/search/health` - Search system health
- `GET /api/search/stats` - System statistics

## 🐛 Troubleshooting

### Common Issues

1. **Azure OpenAI Connection Errors**
   - Verify API key and endpoint in `.env`
   - Check deployment names match your Azure setup
   - Ensure API quota is not exceeded

2. **File Upload Failures**
   - Check file size (max 2MB)
   - Verify supported file types: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX
   - Ensure `uploads/` directory exists and is writable

3. **Frontend Connection Issues**
   - Verify backend is running on port 8000
   - Check CORS settings in backend
   - Ensure `REACT_APP_API_URL` is correct

4. **Database Issues**
   - Delete `docbot.db` to reset database
   - Check file permissions
   - Verify SQLite installation

## 📈 Performance Considerations

- **File Size Limit**: 2MB per document to manage processing time
- **Chunk Size**: Optimized for embedding model context window
- **Vector Search**: ChromaDB provides fast similarity search
- **Caching**: Static file caching for better performance
- **Async Processing**: Document processing happens in background

## 🔮 Future Enhancements

- Multi-language support
- Bulk document upload
- Advanced search filters
- Document versioning
- Export conversation history
- Mobile responsive design improvements
- Real-time collaboration features

## 📄 License

This project is proprietary software. All rights reserved.

## 👥 Support

For technical support or questions, please contact the development team.

---

**Chart Boat** - Navigate your documents with AI intelligence ⚓ 