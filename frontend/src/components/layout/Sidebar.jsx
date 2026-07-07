
export default function Sidebar({
  sessions,
  currentSessionId,
  datasetContext,
  onNewSession,
  onLoadSession
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
      </div>

      <div className="sidebar-content">
        <button className="btn-new-chat" onClick={onNewSession}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Nuevo Mensaje
        </button>

        <section className="sidebar-section">
          <div className="section-title">Historial de Chats</div>
          <div className="chat-history-list">
            {sessions.length === 0 ? (
              <div className="history-empty">Aun no hay conversaciones guardadas.</div>
            ) : (
              sessions.map(session => (
                <button
                  key={session.session_id}
                  className={`history-item ${session.session_id === currentSessionId ? 'active' : ''}`}
                  onClick={() => onLoadSession(session.session_id)}
                >
                  <span className="history-item-title">{session.title}</span>
                </button>
              ))
            )}
          </div>
        </section>
      </div>

      <div className="sidebar-footer">
        <div className="sidebar-section sidebar-section-compact">
          <div className="section-title section-title-small">Contexto Activo</div>
          <div className="active-dataset-card active-dataset-card-compact">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="file-icon">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <div className="dataset-meta">
              <span className="mini-badge neutral">
                {datasetContext ? 'Dataset Cargado' : 'Sin archivo'}
              </span>
              <strong style={{ fontSize: '0.8rem', fontWeight: '600' }}>
                {datasetContext?.file_name || 'Sin archivo'}
              </strong>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
