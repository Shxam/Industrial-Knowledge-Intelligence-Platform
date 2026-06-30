# 🚀 Quick Start Guide - Frontend

## Step 1: Install Dependencies (if not already done)

Open PowerShell in the frontend directory:

```powershell
cd frontend
npm install
```

## Step 2: Start the Development Server

```powershell
npm run dev
```

Expected output:
```
VITE v8.1.0  ready in XXX ms

➜  Local:   http://localhost:3000/
➜  Network: http://192.168.X.X:3000/
➜  press h to show help
```

## Step 3: Access the Application

Open your browser and navigate to:
- **Local**: http://localhost:3000
- **Mobile**: Use the Network URL shown in the terminal

## Step 4: Test the Features

### Upload Documents
1. Click on the "Ingest" tab
2. Drag and drop a PDF, TXT, DOCX, or MD file
3. Wait for upload to complete

### Ask Questions
1. Click on the "Copilot" tab
2. Type a question about your documents
3. Get AI-powered answers with citations

### View Documents
1. Click on the "Library" tab
2. See all uploaded documents
3. Check processing status

### Root Cause Analysis
1. Click on the "RCA" tab
2. Describe a failure or incident
3. Get 5-Why analysis and recommendations

### Knowledge Graph
1. Click on the "Graph" tab
2. View entity relationships
3. Interact with the visualization

## 🎉 That's It!

Your frontend is now running and connected to the backend API.

## ⚠️ Troubleshooting

### Backend Not Running?
Make sure the backend is started first:
```powershell
cd backend
.\venv\Scripts\activate
python app\main.py
```

### Port Already in Use?
Change the port in `vite.config.ts`:
```typescript
server: {
  port: 3001,  // Change to any available port
}
```

### Dependencies Issues?
Delete and reinstall:
```powershell
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```
