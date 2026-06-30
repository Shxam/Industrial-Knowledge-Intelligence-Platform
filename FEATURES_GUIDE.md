# 🎯 Features Guide - Complete Reference

**Last Updated**: June 29, 2026 (Day 5)  
**Version**: 2.0 - Advanced Features

---

## 🗺️ Application Overview

### 5 Main Sections (Tabs)

1. **Upload Documents** - Drag-and-drop file upload
2. **Document Library** - View & manage all documents
3. **Ask Questions** - AI-powered Q&A with session management
4. **Root Cause Analysis** - 5-Why & Fishbone diagrams
5. **Knowledge Graph** - Interactive graph visualization

---

## 📤 1. Upload Documents

### Features
- Drag-and-drop file upload
- Click to select files
- Multi-file upload support
- Real-time progress tracking
- Success/error feedback
- Toast notifications
- File size limit (50MB)
- Format validation

### Supported Formats
- PDF (.pdf)
- Text (.txt)
- Word (.docx)
- Markdown (.md)

### How to Use
1. Navigate to "Upload Documents" tab
2. Drag files onto upload area OR click to select
3. Watch upload progress in real-time
4. See success notification when complete
5. Files are automatically processed

### Feedback
- ✅ Green checkmark = Success
- 🔄 Spinning loader = Uploading
- ❌ Red X = Error
- 🎊 Toast notification on success/error

---

## 📚 2. Document Library

### Features
- List all uploaded documents
- View document status
- See metadata (size, date, chunks)
- Delete documents
- Refresh list
- Empty state handling
- Status color coding

### Document Statuses
- ✅ **Completed** (green) - Ready to query
- ⏳ **Processing** (yellow, pulsing) - Being processed
- ❌ **Failed** (red) - Processing error

### How to Use
1. Navigate to "Document Library" tab
2. See all uploaded documents
3. Click trash icon to delete (with confirmation)
4. Click "Refresh" to update list

### Information Displayed
- Filename
- Upload date & time
- File size
- Number of chunks (if processed)
- Current status

---

## 💬 3. Ask Questions (Chat Interface)

### Features
- Multiple chat sessions
- Session sidebar
- Session persistence (localStorage)
- Auto-generated titles
- Edit session titles
- Delete sessions
- Message history
- Citation display
- Markdown rendering
- Real-time responses

### Session Management
- **Create New Chat**: Click "New Chat" button
- **Switch Sessions**: Click on session in sidebar
- **Edit Title**: Click edit icon, type new title, press Enter
- **Delete Session**: Click trash icon (cannot delete last session)
- **Auto-Save**: All changes saved automatically

### Chat Features
- User messages (right side, blue)
- AI responses (left side, gray)
- Citations below AI answers
- Relevance scores for sources
- Auto-scroll to latest message
- Loading indicator during processing

### How to Use
1. Navigate to "Ask Questions" tab
2. Select or create a chat session
3. Type your question in input field
4. Press Enter or click "Send"
5. View AI response with citations
6. Continue conversation

### Tips
- Sessions persist across page refreshes
- First message becomes session title
- Edit titles for better organization
- Delete old sessions to declutter

---

## 🔍 4. Root Cause Analysis

### Features
- AI-powered RCA
- 5-Why analysis
- Fishbone diagram (6 categories)
- Actionable recommendations
- Evidence summary
- Confidence scoring

### How to Use
1. Navigate to "Root Cause Analysis" tab
2. Describe failure/incident in text area
3. Click "Analyze Root Cause"
4. Wait for AI analysis (10-30 seconds)
5. Review results

### Output Sections

#### Confidence Score
- Shows analysis completion
- Displays confidence percentage
- Green banner at top

#### 5-Why Analysis
- 5 numbered steps
- Each "why" digs deeper
- Leads to root cause

#### Fishbone Diagram
- **People**: Human factors
- **Process**: Procedural issues
- **Equipment**: Machinery problems
- **Materials**: Supply/quality issues
- **Environment**: External conditions
- **Management**: Organizational factors

#### Recommendations
- Numbered action items
- Improvement suggestions
- Prevention measures

#### Evidence Summary
- Supporting information
- Document references
- Confidence basis

---

## 🕸️ 5. Knowledge Graph

### Features
- Interactive graph visualization
- Node dragging & exploration
- Zoom & pan controls
- Node search with highlighting
- Color-coded by type
- Relationship labels
- Statistics dashboard
- Legend

### Graph Controls

#### Visualization Button
- Click "Visualize Graph" to load
- Only available if documents processed
- Loads up to 100 nodes initially

#### Toolbar
- **Search Box**: Type to search nodes
- **Search Button**: Highlight matching nodes
- **Zoom In** (+): Enlarge view
- **Zoom Out** (-): Shrink view
- **Fit to Screen**: Auto-fit all nodes
- **Reset Layout**: Recalculate positions

### Node Colors
- 🔵 **Blue**: Equipment
- 🟢 **Green**: Process
- 🟠 **Orange**: Material
- 🟣 **Purple**: Person
- 🔴 **Red**: Location
- ⚫ **Gray**: Document

### How to Use
1. Navigate to "Knowledge Graph" tab
2. Review statistics (nodes, relationships)
3. Click "Visualize Graph" button
4. Interact with graph:
   - Drag nodes to reposition
   - Scroll to zoom
   - Click nodes to select
   - Search for specific entities
   - Use controls to navigate

### Statistics Display
- Total nodes count
- Total relationships count
- Node types breakdown
- Relationship types breakdown

---

## 🔔 Toast Notifications

### Types
- ✅ **Success** (green) - Operations completed
- ❌ **Error** (red) - Operations failed
- ⚠️ **Warning** (yellow) - Attention needed

### When They Appear
- Document uploaded successfully
- Document upload failed
- Document deleted
- New chat session created
- Session deleted
- Cannot delete last session
- API errors

### Features
- Auto-dismiss after 3 seconds
- Manual close with X button
- Progress bar showing time left
- Stack multiple notifications
- Bottom-right positioning
- Smooth animations

---

## ⌨️ Keyboard Shortcuts

### Chat Interface
- **Enter**: Send message
- **Enter** (in title edit): Save title

### Graph Visualization
- **Enter** (in search): Search nodes

### Document Upload
- **Click**: Select files
- **Drag & Drop**: Upload files

---

## 💡 Pro Tips

### General
1. Keep backend running for all features to work
2. Upload documents before asking questions
3. Wait for "Completed" status before querying
4. Use descriptive failure descriptions for better RCA

### Session Management
1. Create separate sessions for different topics
2. Edit titles for easy identification
3. Delete old sessions to stay organized
4. Sessions auto-save - no manual save needed

### Graph Visualization
1. Use search to find specific entities
2. Drag nodes to see connections better
3. Zoom in for detailed view
4. Fit to screen after rearranging
5. Reset layout if graph gets messy

### Document Management
1. Upload related documents together
2. Check status before querying
3. Delete old documents to save space
4. Refresh list after backend changes

---

## 🐛 Troubleshooting

### Problem: Upload fails
**Solutions**:
- Check file format (PDF, TXT, DOCX, MD only)
- Verify file size < 50MB
- Ensure backend is running
- Check internet connection

### Problem: No graph visualization
**Solutions**:
- Upload documents first
- Wait for documents to process
- Check if Neo4j is running
- Verify backend connection
- Refresh the page

### Problem: Sessions not saving
**Solutions**:
- Check browser localStorage not disabled
- Try different browser
- Clear browser cache
- Check console for errors

### Problem: Chat not responding
**Solutions**:
- Verify documents are processed
- Check backend is running
- Look at backend logs
- Try refreshing page
- Create new session

### Problem: Toasts not showing
**Solutions**:
- Check if blocked by browser
- Look for console errors
- Verify ToastContainer is rendered
- Try refreshing page

---

## 📊 Feature Status

| Feature | Status | Completeness |
|---------|--------|--------------|
| Document Upload | ✅ | 100% |
| Document Library | ✅ | 100% |
| Chat Interface | ✅ | 100% |
| Session Management | ✅ | 100% |
| RCA Analysis | ✅ | 95% |
| Knowledge Graph | ✅ | 100% |
| Interactive Graph | ✅ | 100% |
| Toast Notifications | ✅ | 100% |

---

## 🎯 Best Practices

### For Best Results

#### Document Upload
1. Upload all related documents together
2. Use clear, descriptive filenames
3. Ensure documents are well-formatted
4. Wait for processing to complete

#### Asking Questions
1. Be specific in your questions
2. Reference document topics
3. Use natural language
4. Review citations for context

#### Root Cause Analysis
1. Provide detailed failure descriptions
2. Include context (when, where, what)
3. Mention any evidence you have
4. Review all output sections

#### Knowledge Graph
1. Process multiple documents for better graph
2. Use search to explore specific topics
3. Look for connection patterns
4. Note relationship types

---

## 🚀 Quick Start Workflow

### First Time User
1. Upload 2-3 documents
2. Wait for "Completed" status (Document Library)
3. Go to Ask Questions
4. Ask general question about docs
5. Review answer and citations
6. Try RCA with sample failure
7. Explore Knowledge Graph

### Regular Use
1. Check Document Library
2. Create new chat session if needed
3. Ask specific questions
4. Use RCA for incidents
5. Explore graph connections
6. Manage old sessions

---

## 📞 Need Help?

### Resources
- **Testing Guide**: TESTING_GUIDE.md
- **Documentation Index**: DOCS_INDEX.md
- **API Docs**: http://localhost:8000/docs
- **Backend Logs**: Check terminal running backend

### Common Questions

**Q: How long does document processing take?**
A: Usually 10-30 seconds depending on size.

**Q: Can I ask questions about multiple documents?**
A: Yes! The system searches across all uploaded documents.

**Q: Do sessions sync across devices?**
A: No, sessions are stored in browser localStorage only.

**Q: Can I export RCA results?**
A: Not yet - coming in future update.

**Q: What if graph is too crowded?**
A: Use search to focus on specific nodes, or limit results.

---

## 🎉 Advanced Features

### Coming Soon
- [ ] Export RCA to PDF
- [ ] Dark mode
- [ ] Advanced keyboard shortcuts
- [ ] Graph filtering
- [ ] Document preview
- [ ] Real-time collaboration

### Currently Available
- [x] Interactive graph visualization
- [x] Multi-session management
- [x] Session persistence
- [x] Document library
- [x] Toast notifications
- [x] Drag-and-drop upload
- [x] Citation display
- [x] Status tracking

---

**Remember**: All features work together to provide a comprehensive industrial AI assistant experience!

**Quick Access**: http://localhost:5173

**Status**: All core features working! 🚀
