# Industrial AI Assistant - Frontend

Modern React + TypeScript frontend for the Industrial AI Assistant platform.

## 🚀 Features

- **Document Upload**: Drag-and-drop interface for uploading PDF, TXT, DOCX, and MD files
- **Chat Interface**: Ask questions about uploaded documents with AI-powered responses and citations
- **Root Cause Analysis**: AI agent for 5-Why analysis and fishbone diagrams
- **Knowledge Graph**: Visualize entities and relationships extracted from documents

## 🛠️ Tech Stack

- **React 18** with TypeScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **React Query** - Server state management
- **Axios** - HTTP client
- **react-dropzone** - File upload
- **react-markdown** - Markdown rendering
- **lucide-react** - Icon library

## 📦 Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## 🔧 Configuration

Edit `.env` to configure the backend API URL:

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

## 📁 Project Structure

```
src/
├── api/
│   └── client.ts              # API client and endpoints
├── components/
│   ├── DocumentUpload.tsx     # File upload component
│   ├── ChatInterface.tsx      # Q&A chat interface
│   ├── RCADisplay.tsx         # Root cause analysis display
│   └── GraphVisualization.tsx # Knowledge graph viewer
├── App.tsx                     # Main app with tab navigation
├── main.tsx                    # Entry point
└── index.css                   # Global styles with Tailwind
```

## 🎨 Features in Detail

### Document Upload
- Drag-and-drop file upload
- Support for PDF, TXT, DOCX, MD formats
- Real-time upload progress
- Success/error feedback

### Chat Interface
- Chat-style Q&A interface
- Display AI responses with markdown support
- Show source citations with relevance scores
- Auto-scroll to latest messages

### Root Cause Analysis
- Input form for failure description
- 5-Why analysis visualization
- Fishbone diagram (6 categories)
- Actionable recommendations
- Evidence summary
- Confidence score

### Knowledge Graph
- Display graph statistics
- Node and relationship type breakdown
- (Coming soon: Interactive Cytoscape.js visualization)

## 🧪 Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🎯 Usage

1. **Upload Documents**: Navigate to "Upload Documents" tab and upload your files
2. **Ask Questions**: Go to "Ask Questions" tab and chat with the AI about your documents
3. **Run RCA**: Use "Root Cause Analysis" tab to analyze failures and incidents
4. **Explore Graph**: View the knowledge graph in "Knowledge Graph" tab

## 🌐 API Integration

The frontend connects to the backend API at `http://localhost:8000/api/v1` by default.

API endpoints used:
- `POST /documents/upload` - Upload documents
- `GET /documents/{id}/status` - Check document processing status
- `POST /query` - Ask questions about documents
- `POST /rca/analyze` - Perform root cause analysis
- `GET /graph/stats` - Get knowledge graph statistics
- `GET /graph/visualize` - Get graph data for visualization

## 🎨 Styling

The app uses Tailwind CSS with a custom industrial theme:
- Primary color: Industrial Blue (#0ea5e9)
- Clean, professional design
- Fully responsive
- Dark mode ready (coming soon)

## 🔮 Upcoming Features

- [ ] Interactive graph visualization with Cytoscape.js
- [ ] Session management
- [ ] User authentication
- [ ] Document preview
- [ ] Export RCA reports to PDF
- [ ] Advanced graph filters
- [ ] Real-time updates via WebSocket
- [ ] Dark mode
- [ ] Keyboard shortcuts

## 🐛 Troubleshooting

**Issue**: Can't connect to backend
- Ensure backend is running at `http://localhost:8000`
- Check `.env` file has correct `VITE_API_URL`

**Issue**: Upload fails
- Check file format is supported (PDF, TXT, DOCX, MD)
- Ensure backend has proper CORS configuration

**Issue**: Query returns no results
- Upload documents first
- Wait for documents to be processed (check status)

## 📄 License

MIT
