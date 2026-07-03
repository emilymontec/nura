import { useState, useEffect, useRef } from 'react';
import Sidebar from './Sidebar';
import ChatHeader from './ChatHeader';
import ChatContainer from './ChatContainer';
import Composer from './Composer';
import AnalyticsPanel from './AnalyticsPanel';

const API_BASE = import.meta.env.VITE_API_URL || '';

function ChatApp() {
  const [sessionId, setSessionId] = useState('default');
  const [messages, setMessages] = useState([]);
  const [datasetContext, setDatasetContext] = useState(null);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatContainerRef = useRef(null);

  const fetchSessions = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/sessions`);
      const data = await response.json();
      setSessions(data.sessions || []);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const startNewSession = () => {
    const newId = `session_${Date.now()}`;
    setSessionId(newId);
    setMessages([]);
    setDatasetContext(null);
    setShowAnalytics(false);
  };

  const loadSession = async (id) => {
    setSessionId(id);
    try {
      const response = await fetch(`${API_BASE}/api/sessions/${id}`);
      const data = await response.json();
      setMessages(data.messages || []);
      setDatasetContext(data.dataset_context || null);
    } catch (error) {
      console.error('Error loading session:', error);
    }
  };

  const handleSendMessage = async (text) => {
    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: sessionId
        })
      });

      const data = await response.json();
      const aiMsg = { role: 'assistant', content: data.response };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', sessionId);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();

      setDatasetContext(data);
      const aiMsg = { role: 'assistant', content: data.response };
      setMessages([aiMsg]);
      setShowAnalytics(true);
      fetchSessions();
    } catch (error) {
      console.error('Error analyzing file:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePromptClick = (prompt) => {
    if (!datasetContext) {
      handleSendMessage(prompt);
    } else {
      handleSendMessage(prompt);
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, loading]);

  useEffect(() => {
    fetchSessions();
  }, []);

  return (
    <div className="app-shell">
      <div className="void-fog" aria-hidden="true">
        <div className="fog-node fn-1"></div>
        <div className="fog-node fn-2"></div>
        <div className="fog-node fn-3"></div>
      </div>

      <div className={`app-container ${showAnalytics ? 'show-analytics' : ''}`}>
        <Sidebar
          sessions={sessions}
          currentSessionId={sessionId}
          datasetContext={datasetContext}
          onNewSession={startNewSession}
          onLoadSession={loadSession}
        />

        <main className="chat-main">
          <ChatHeader
            showAnalytics={showAnalytics}
            onToggleAnalytics={() => setShowAnalytics(!showAnalytics)}
          />

          <div className="chat-stage">
            <div className="chat-container" ref={chatContainerRef}>
              <ChatContainer
                messages={messages}
                loading={loading}
                datasetContext={datasetContext}
                onPromptClick={handlePromptClick}
              />
            </div>
          </div>

          <Composer
            onSendMessage={handleSendMessage}
            onFileUpload={handleFileUpload}
          />
        </main>

        {showAnalytics && datasetContext && (
          <AnalyticsPanel
            datasetContext={datasetContext}
            onClose={() => setShowAnalytics(false)}
          />
        )}
      </div>
    </div>
  );
}

export default ChatApp;
