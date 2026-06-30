import { useState } from 'react';
import { FileText, MessageSquare, GitBranch, Upload, FolderOpen, ShieldCheck } from 'lucide-react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { SessionProvider } from './context/SessionContext';
import { DocumentUpload } from './components/DocumentUpload';
import { DocumentList } from './components/DocumentList';
import { ChatInterface } from './components/ChatInterface';
import { RCADisplay } from './components/RCADisplay';
import { GraphVisualization } from './components/GraphVisualization';

type Tab = 'upload' | 'documents' | 'query' | 'rca' | 'graph';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('upload');

  const tabs = [
    { id: 'upload' as Tab, label: 'Ingest', icon: Upload },
    { id: 'documents' as Tab, label: 'Library', icon: FolderOpen },
    { id: 'query' as Tab, label: 'Copilot', icon: MessageSquare },
    { id: 'rca' as Tab, label: 'RCA', icon: FileText },
    { id: 'graph' as Tab, label: 'Graph', icon: GitBranch },
  ];

  return (
    <SessionProvider>
      <div className="app-shell">
        <header className="app-header">
          <div className="app-header-inner">
            <div className="app-kicker">
              <span className="app-status-dot" />
              Live operations intelligence
            </div>
            <div className="app-title-row">
              <div>
                <h1 className="app-title">Pragya Industrial Copilot</h1>
                <p className="app-subtitle">
                  Search plant knowledge, analyze failures, and inspect document-backed
                  relationships from one operations workspace.
                </p>
              </div>
              <div className="app-metrics" aria-label="System summary">
                <div className="app-metric">
                  <span className="app-metric-value">&lt;10s</span>
                  <span className="app-metric-label">Target answer</span>
                </div>
                <div className="app-metric">
                  <span className="app-metric-value">RAG</span>
                  <span className="app-metric-label">Cited retrieval</span>
                </div>
                <div className="app-metric">
                  <span className="app-metric-value">
                    <ShieldCheck className="inline h-4 w-4 align-[-2px]" /> Local
                  </span>
                  <span className="app-metric-label">Data option</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        <nav className="app-nav" aria-label="Primary workspace">
          <div className="app-nav-inner">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`app-tab ${activeTab === tab.id ? 'app-tab-active' : ''}`}
                >
                  <Icon className="app-tab-icon" />
                  <span className="app-tab-label">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </nav>

        <main className="app-main">
          {activeTab === 'upload' && (
            <section className="app-panel">
              <DocumentUpload />
            </section>
          )}
          {activeTab === 'documents' && (
            <section className="app-panel">
              <DocumentList />
            </section>
          )}
          {activeTab === 'query' && (
            <div className="app-chat-panel">
              <ChatInterface />
            </div>
          )}
          {activeTab === 'rca' && (
            <section className="app-panel">
              <RCADisplay />
            </section>
          )}
          {activeTab === 'graph' && (
            <section className="app-panel">
              <GraphVisualization />
            </section>
          )}
        </main>

        <ToastContainer
          position="bottom-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
      </div>
    </SessionProvider>
  );
}

export default App;
