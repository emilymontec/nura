
export default function ChatHeader({ showAnalytics, onToggleAnalytics }) {
  return (
    <header className="chat-header">
      <div className="header-info">
        <h2>NURA</h2>
        <span className="header-status-dot"></span>
        <span className="header-status-text">Listo</span>
      </div>
      <div className="header-actions">
        <button className="analytics-toggle-btn" onClick={onToggleAnalytics}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"></line>
            <line x1="12" y1="20" x2="12" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="14"></line>
          </svg>
          <span>Resumen</span>
        </button>
      </div>
    </header>
  );
}
