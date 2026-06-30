# Frontend Setup Guide

Complete setup guide for the IKIP React PWA frontend.

## ✅ What's Been Built

### Core Features
- ✅ **5 Main Tabs/Views**
  - Ingest (Document Upload)
  - Library (Document List)
  - Copilot (AI Chat with RAG)
  - RCA (Root Cause Analysis)
  - Graph (Knowledge Graph Visualization)

- ✅ **Components Created**
  - `ChatInterface.tsx` - Multi-session chat with citations
  - `DocumentUpload.tsx` - Drag-and-drop file upload
  - `DocumentList.tsx` - Document library with status
  - `GraphVisualization.tsx` - Interactive Cytoscape graph
  - `RCADisplay.tsx` - 5-Why and Fishbone diagram display
  - `InstallPrompt.tsx` - PWA install prompt
  - `OfflineIndicator.tsx` - Network status indicator
  - `LoadingScreen.tsx` - App loading screen

- ✅ **State Management**
  - `SessionContext.tsx` - Chat session management
  - LocalStorage persistence
  - React Query for API state

- ✅ **API Integration**
  - `client.ts` - Axios-based API client
  - Complete backend integration
  - Error handling and logging

- ✅ **PWA Features**
  - Service Worker with offline support
  - Web App Manifest
  - Install prompts
  - Offline caching strategy
  - Background sync ready

- ✅ **Styling & UX**
  - Tailwind CSS + custom industrial theme
  - Mobile-first responsive design
  - Touch-friendly interactions
  - Loading states and error handling
  - Toast notifications

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env (already configured for local dev)
# VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at:
- **Local**: http://localhost:3000
- **Network**: http://YOUR_IP:3000 (for mobile testing)

## 📱 Testing on Mobile

1. Ensure your mobile device is on the same network
2. Find your computer's IP address:
   ```bash
   ipconfig  # Windows
   ifconfig  # Mac/Linux
   ```
3. On mobile, navigate to: `http://YOUR_IP:3000`
4. You should see the PWA install prompt on supported browsers

## 🏗️ Build for Production

```bash
# Create production build
npm run build

# Test production build locally
npm run preview
```

The build output will be in the `dist/` folder.

## 🐳 Docker Deployment

### Build Docker Image

```bash
cd frontend
docker build -t ikip-frontend .
```

### Run Container

```bash
docker run -p 3000:3000 ikip-frontend
```

### With Docker Compose

The frontend is already configured in the root `docker-compose.yml`:

```bash
# From project root
docker-compose up frontend
```

## 📋 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start dev server with HMR |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## 🔧 Configuration Files

### `vite.config.ts`
- Development server on port 3000
- Proxy `/api` requests to backend
- Code splitting configuration
- Build optimization settings

### `tailwind.config.js`
- Custom industrial color palette
- Responsive breakpoints
- Custom utilities

### `manifest.json`
- PWA configuration
- App icons and theme
- Shortcuts for quick actions

### `sw.js`
- Service worker implementation
- Offline caching strategy
- Background sync hooks

## 🎨 Customization

### Colors

The app uses a custom "industrial" color palette:

```css
--industrial-50: #eef7ff
--industrial-100: #d8ecff
--industrial-500: #1677c7  (primary)
--industrial-600: #0f609f
--industrial-700: #0b4b7d
```

To change the theme, update these variables in `src/index.css`.

### Logo & Icons

Replace these files in `public/`:
- `favicon.svg` - Browser tab icon
- `icon-192.png` - Small app icon (192x192)
- `icon-512.png` - Large app icon (512x512)

You can generate icons from an SVG using tools like:
- https://realfavicongenerator.net/
- https://www.pwabuilder.com/

## 🐛 Troubleshooting

### Service Worker Not Registering

1. Check browser console for errors
2. Ensure you're on `localhost` or HTTPS
3. Clear browser cache and reload
4. Check DevTools → Application → Service Workers

### API Connection Issues

1. Verify backend is running: `http://localhost:8000/docs`
2. Check `VITE_API_URL` in `.env`
3. Look for CORS errors in browser console
4. Ensure backend CORS is configured to allow `http://localhost:3000`

### Build Errors

1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Clear Vite cache: `rm -rf node_modules/.vite`
4. Try building again: `npm run build`

### Mobile Touch Issues

- Inputs zooming on focus: Ensure `font-size: 16px` on inputs
- Buttons too small: Use `min-height: 44px` for touch targets
- Viewport issues: Check meta viewport tag in `index.html`

## 📊 Performance Tips

### Development
- Use React DevTools Profiler to identify slow components
- Enable source maps for debugging: `vite.config.ts`
- Use network throttling to test on slow connections

### Production
- Analyze bundle size: `npm run build -- --report`
- Use Lighthouse for PWA audit
- Enable gzip compression on server
- Use CDN for static assets

## 🔒 Security Checklist

- [ ] Update dependencies: `npm audit fix`
- [ ] Use HTTPS in production
- [ ] Configure CSP headers
- [ ] Sanitize user inputs (already handled by React)
- [ ] Secure API keys (use environment variables)
- [ ] Enable rate limiting on backend

## 📱 PWA Installation

### Chrome Desktop
1. Click install icon in address bar
2. Or go to menu → Install IKIP

### Chrome Mobile
1. Tap menu (⋮)
2. Select "Add to Home Screen"
3. Confirm installation

### Safari iOS
1. Tap share button
2. Select "Add to Home Screen"
3. Confirm installation

## 🚀 Next Steps

### Planned Features
- [ ] Voice input for queries (Web Speech API)
- [ ] Advanced query filters
- [ ] Document preview modal
- [ ] Batch document upload
- [ ] Export chat history
- [ ] Dark mode
- [ ] Internationalization (i18n)
- [ ] Accessibility improvements (ARIA labels)

### Enhancements
- [ ] Add route-based navigation (React Router)
- [ ] Implement lazy loading for components
- [ ] Add unit tests (Vitest)
- [ ] Add E2E tests (Playwright)
- [ ] Set up CI/CD pipeline
- [ ] Add analytics (optional)
- [ ] Optimize images with WebP

## 📚 Resources

### Documentation
- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [PWA Best Practices](https://web.dev/pwa/)
- [Cytoscape.js](https://js.cytoscape.org)

### Tools
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [PWA Builder](https://www.pwabuilder.com/)

## 💡 Tips

1. **Session Management**: Chat sessions are stored in localStorage. Clear localStorage to reset.

2. **Network Tab**: Use browser DevTools → Network to debug API calls.

3. **Responsive Testing**: Use DevTools device emulation or real devices.

4. **Offline Testing**: Use DevTools → Application → Service Workers → Offline checkbox.

5. **PWA Testing**: Use Lighthouse PWA audit in DevTools.

## ✅ Verification Checklist

- [ ] Dependencies installed (`node_modules/` exists)
- [ ] `.env` file created and configured
- [ ] Dev server starts without errors (`npm run dev`)
- [ ] Backend is running and accessible
- [ ] Can upload a document
- [ ] Can query the copilot
- [ ] Can view knowledge graph
- [ ] Can run RCA analysis
- [ ] Service worker registers in browser
- [ ] PWA install prompt appears (on supported browsers)
- [ ] Offline indicator works (test by disconnecting)
- [ ] Mobile view is responsive

## 🎉 Success!

If all checkboxes above are complete, your frontend is ready to use!

Access the app at: **http://localhost:3000**

---

**Questions or Issues?**
Check the main [README.md](../README.md) or [BACKEND_VERIFICATION_REPORT.md](../BACKEND_VERIFICATION_REPORT.md) for additional help.
