# IKIP Frontend - React PWA

Progressive Web Application (PWA) frontend for the Industrial Knowledge Intelligence Platform (IKIP).

## 🚀 Features

- ✅ **React 19** with TypeScript
- ✅ **Progressive Web App** with offline support
- ✅ **Mobile-First Design** with responsive layouts
- ✅ **Real-time Chat Interface** with session management
- ✅ **Document Management** with drag-and-drop upload
- ✅ **Knowledge Graph Visualization** with Cytoscape
- ✅ **Root Cause Analysis (RCA)** interface
- ✅ **Tailwind CSS** for styling
- ✅ **Vite** for fast development and builds

## 📋 Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

## 🛠️ Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Edit .env with your backend URL if needed
# VITE_API_URL=http://localhost:8000/api/v1
```

## 🏃 Development

```bash
# Start development server
npm run dev

# Access at http://localhost:3000
```

The dev server includes:
- Hot Module Replacement (HMR)
- Automatic proxy to backend API
- PWA features (service worker)

## 🏗️ Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 📱 PWA Features

### Service Worker
- Offline support for static assets
- API response caching (GET requests)
- Background sync (future)
- Push notifications (future)

### Installation
- Custom install prompt
- Desktop and mobile support
- App shortcuts for quick actions

### Manifest
- Standalone display mode
- Custom icons and theme colors
- Home screen installation

## 📁 Project Structure

```
frontend/
├── public/
│   ├── manifest.json      # PWA manifest
│   ├── sw.js             # Service worker
│   ├── favicon.svg       # App icon
│   └── icons.svg         # Icon sprite
├── src/
│   ├── api/
│   │   └── client.ts     # API client with axios
│   ├── components/
│   │   ├── ChatInterface.tsx
│   │   ├── DocumentUpload.tsx
│   │   ├── DocumentList.tsx
│   │   ├── GraphVisualization.tsx
│   │   ├── RCADisplay.tsx
│   │   ├── InstallPrompt.tsx
│   │   ├── OfflineIndicator.tsx
│   │   └── LoadingScreen.tsx
│   ├── context/
│   │   └── SessionContext.tsx
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # App entry point
│   ├── index.css         # Global styles
│   └── App.css           # Component styles
├── index.html            # HTML entry point
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind configuration
└── package.json          # Dependencies
```

## 🎨 Components

### ChatInterface
Multi-session chat interface with:
- Session management (create, switch, delete)
- Message history with citations
- Markdown rendering
- Auto-scroll to latest message

### DocumentUpload
Drag-and-drop file upload with:
- Multiple file support
- Upload progress tracking
- File type validation
- Size limits (50MB)

### DocumentList
Document library with:
- Status indicators (processing, completed, failed)
- Delete functionality
- Refresh capability
- Metadata display

### GraphVisualization
Interactive knowledge graph with:
- Cytoscape.js visualization
- Node search and filtering
- Zoom and pan controls
- Custom layouts

### RCADisplay
Root Cause Analysis interface with:
- 5-Why analysis display
- Fishbone diagram
- Recommendations list
- Evidence summary

## 🔧 Configuration

### Environment Variables

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000/api/v1

# Feature flags
VITE_ENABLE_OFFLINE_MODE=true
VITE_ENABLE_NOTIFICATIONS=false
```

### Vite Config
- Port: 3000
- Proxy: `/api` → `http://localhost:8000`
- Code splitting for vendors
- Source maps disabled in production

## 🌐 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android 90+)

## 📱 Mobile Testing

```bash
# Start dev server accessible on network
npm run dev

# Access from mobile device:
# http://YOUR_IP:3000
```

## 🐛 Debugging

### Check Service Worker
Open DevTools → Application → Service Workers

### View PWA Status
Chrome DevTools → Lighthouse → PWA Audit

### Network Issues
Check DevTools → Network tab for API calls

## 🚀 Deployment

### Static Hosting (Netlify, Vercel)
```bash
npm run build
# Deploy the dist/ folder
```

### Docker
```bash
docker build -t ikip-frontend .
docker run -p 3000:3000 ikip-frontend
```

### Nginx Configuration
```nginx
location /api/ {
    proxy_pass http://backend:8000/api/;
}

location / {
    root /usr/share/nginx/html;
    try_files $uri $uri/ /index.html;
}
```

## 📊 Performance

### Optimization Techniques
- Code splitting by vendor
- Lazy loading for routes (future)
- Image optimization
- Gzip compression
- Service worker caching

### Lighthouse Scores (Target)
- Performance: 90+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 90+
- PWA: 100

## 🔒 Security

- HTTPS required for PWA features
- CORS configured for backend
- Input sanitization
- XSS protection via React
- CSP headers (configure in deployment)

## 🧪 Testing

```bash
# Run linter
npm run lint

# Type check
npx tsc --noEmit
```

## 📝 Notes

### Session Management
- Chat sessions stored in localStorage
- Persists across page refreshes
- Automatic session creation
- Max session storage: ~5MB

### Offline Support
- Static assets cached on install
- API responses cached (GET only)
- Fallback for offline queries
- Background sync for uploads (future)

## 🤝 Contributing

1. Follow existing code structure
2. Use TypeScript for new components
3. Add proper prop types and interfaces
4. Test on both desktop and mobile
5. Ensure PWA features work

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ for the Industrial AI Hackathon**
