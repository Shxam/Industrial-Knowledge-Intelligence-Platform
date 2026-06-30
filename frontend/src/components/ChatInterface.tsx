import { useState, useRef, useEffect } from 'react';
import {
  Send,
  Loader,
  User,
  Bot,
  Plus,
  Trash2,
  Edit2,
  PanelLeftClose,
  PanelLeftOpen,
  Eraser,
} from 'lucide-react';
import { query } from '../api/client';
import ReactMarkdown from 'react-markdown';
import { useSession } from '../context/SessionContext';
import { toast } from 'react-toastify';

export function ChatInterface() {
  const {
    sessions,
    currentSession,
    createSession,
    switchSession,
    deleteSession,
    addMessage,
    updateSessionTitle,
    clearCurrentSession,
  } = useSession();
  
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);
  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentSession?.messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message
    addMessage({
      role: 'user',
      content: userMessage,
      timestamp: Date.now(),
    });
    
    setIsLoading(true);

    try {
      const response = await query.ask(userMessage);
      const data = response.data;
      const citations = (data.citations || []).map((citation: any) => ({
        text: citation.text || '',
        source: citation.source || citation.document_title || citation.document_id || 'Source document',
        score: citation.score ?? citation.relevance_score ?? 0,
      }));

      // Add assistant message with citations
      addMessage({
        role: 'assistant',
        content: data.answer,
        citations,
        timestamp: Date.now(),
      });
    } catch (error: any) {
      addMessage({
        role: 'assistant',
        content: `Sorry, I encountered an error: ${
          error.response?.data?.detail || error.message
        }`,
        timestamp: Date.now(),
      });
      toast.error('Failed to get response');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    createSession();
    toast.success('New chat created');
  };

  const handleDeleteSession = (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (sessions.length === 1) {
      toast.warning('Cannot delete the last session');
      return;
    }
    deleteSession(sessionId);
    toast.success('Chat deleted');
  };

  const handleEditSession = (sessionId: string, currentTitle: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingSessionId(sessionId);
    setEditTitle(currentTitle);
  };

  const handleSaveTitle = () => {
    if (editingSessionId && editTitle.trim()) {
      updateSessionTitle(editingSessionId, editTitle.trim());
      setEditingSessionId(null);
      setEditTitle('');
    }
  };

  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (hours < 1) return 'Just now';
    if (hours < 24) return `${hours}h ago`;
    if (hours < 48) return 'Yesterday';
    return date.toLocaleDateString();
  };

  return (
    <div className="flex h-full overflow-hidden rounded-lg border border-gray-200 bg-white">
      {/* Sidebar */}
      {showSidebar && (
        <div className="w-72 max-w-[82vw] border-r border-gray-200 bg-gray-50 flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <button
              onClick={handleNewChat}
              className="w-full px-4 py-2 bg-industrial-600 text-white rounded-md hover:bg-industrial-700 transition-colors flex items-center justify-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>New Chat</span>
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto p-2">
            {sessions.map((session) => (
              <div
                key={session.id}
                onClick={() => switchSession(session.id)}
                className={`p-3 mb-2 rounded-lg cursor-pointer transition-colors group ${
                  currentSession?.id === session.id
                    ? 'bg-industrial-100 border border-industrial-300'
                    : 'hover:bg-gray-100 border border-transparent'
                }`}
              >
                {editingSessionId === session.id ? (
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    onBlur={handleSaveTitle}
                    onKeyPress={(e) => e.key === 'Enter' && handleSaveTitle()}
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-industrial-500"
                    autoFocus
                    onClick={(e) => e.stopPropagation()}
                  />
                ) : (
                  <>
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-sm font-medium text-gray-900 truncate flex-1">
                        {session.title}
                      </h4>
                      <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={(e) => handleEditSession(session.id, session.title, e)}
                          className="p-1 hover:bg-gray-200 rounded"
                        >
                          <Edit2 className="w-3 h-3 text-gray-600" />
                        </button>
                        <button
                          onClick={(e) => handleDeleteSession(session.id, e)}
                          className="p-1 hover:bg-red-100 rounded"
                        >
                          <Trash2 className="w-3 h-3 text-red-600" />
                        </button>
                      </div>
                    </div>
                    <p className="text-xs text-gray-500">
                      {formatTime(session.updatedAt)} • {session.messages.length} messages
                    </p>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex min-w-0 flex-col">
        <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3">
          <button
            type="button"
            onClick={() => setShowSidebar((value) => !value)}
            className="rounded-md border border-gray-300 p-2 text-gray-600 hover:bg-gray-50"
            title={showSidebar ? 'Hide chats' : 'Show chats'}
          >
            {showSidebar ? (
              <PanelLeftClose className="h-5 w-5" />
            ) : (
              <PanelLeftOpen className="h-5 w-5" />
            )}
          </button>
          <div className="min-w-0 px-3 text-center">
            <p className="truncate text-sm font-semibold text-gray-900">
              {currentSession?.title || 'Ask Questions'}
            </p>
            <p className="text-xs text-gray-500">Cited answers from uploaded plant documents</p>
          </div>
          <button
            type="button"
            onClick={clearCurrentSession}
            disabled={!currentSession || currentSession.messages.length === 0}
            className="rounded-md border border-gray-300 p-2 text-gray-600 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
            title="Clear current chat"
          >
            <Eraser className="h-5 w-5" />
          </button>
        </div>
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {!currentSession || currentSession.messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-20">
              <Bot className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p className="text-lg">Ask a question about your documents</p>
              <p className="text-sm mt-2">
                I'll search through your uploaded documents to find answers
              </p>
            </div>
          ) : (
            currentSession.messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`flex items-start space-x-3 max-w-3xl ${
                    message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                  }`}
                >
                  <div
                    className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                      message.role === 'user'
                        ? 'bg-industrial-500'
                        : 'bg-gray-300'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <User className="w-5 h-5 text-white" />
                    ) : (
                      <Bot className="w-5 h-5 text-gray-700" />
                    )}
                  </div>
                  <div>
                    <div
                      className={`rounded-lg p-4 text-sm leading-6 ${
                        message.role === 'user'
                          ? 'bg-industrial-500 text-white'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      <ReactMarkdown
                        components={{
                          p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                          ul: ({ children }) => <ul className="ml-4 list-disc space-y-1">{children}</ul>,
                          ol: ({ children }) => <ol className="ml-4 list-decimal space-y-1">{children}</ol>,
                          strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                    {message.citations && message.citations.length > 0 && (
                      <div className="mt-2 space-y-2">
                        <p className="text-xs font-semibold text-gray-600">
                          Sources:
                        </p>
                        {message.citations.map((citation, idx) => (
                          <div
                            key={idx}
                            className="text-xs bg-white border border-gray-200 rounded p-2"
                          >
                            <p className="text-gray-700 mb-1">{citation.text}</p>
                            <p className="text-gray-500">
                              Source: {citation.source} | Relevance:{' '}
                              {(citation.score * 100).toFixed(1)}%
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-gray-700" />
                </div>
                <div className="bg-gray-100 p-4 rounded-lg">
                  <Loader className="w-5 h-5 text-gray-500 animate-spin" />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              disabled={isLoading}
              className="min-w-0 flex-1 px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-industrial-500 disabled:bg-gray-100"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="px-5 py-3 bg-industrial-600 text-white rounded-md hover:bg-industrial-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              <Send className="w-5 h-5" />
              <span>Send</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
