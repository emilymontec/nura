import { useState } from 'react';

export default function Sidebar({
  sessions,
  currentSessionId,
  datasetContext,
  onNewSession,
  onLoadSession,
  onRenameSession,
  onDeleteSession
}) {
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState('');

  const handleRename = (id) => {
    if (editTitle.trim()) {
      onRenameSession(id, editTitle.trim());
    }
    setEditingId(null);
  };

  const handleDelete = (e, id) => {
    e.stopPropagation();
    if (window.confirm('¿Eliminar esta conversación?')) {
      onDeleteSession(id);
    }
  };

  const formatRelativeTime = (dateStr) => {
    if (!dateStr) return '';
    const d = new Date(dateStr);
    const now = new Date();
    const diff = now - d;
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'ahora';
    if (mins < 60) return `hace ${mins}m`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `hace ${hrs}h`;
    const days = Math.floor(hrs / 24);
    if (days < 7) return `hace ${days}d`;
    return d.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
  };

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
                <div
                  key={session.session_id}
                  className={`history-item ${session.session_id === currentSessionId ? 'active' : ''}`}
                  onClick={() => editingId !== session.session_id && onLoadSession(session.session_id)}
                >
                  {editingId === session.session_id ? (
                    <div className="history-item-edit" onClick={(e) => e.stopPropagation()}>
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') handleRename(session.session_id);
                          if (e.key === 'Escape') setEditingId(null);
                        }}
                        className="history-edit-input"
                        autoFocus
                      />
                    </div>
                  ) : (
                    <>
                      <div className="history-item-content">
                        <span className="history-item-title">{session.title}</span>
                        <span className="history-item-time">{formatRelativeTime(session.updated_at)}</span>
                      </div>
                      <div className="history-item-actions">
                        <button
                          className="history-action-btn"
                          onClick={(e) => {
                            e.stopPropagation();
                            setEditingId(session.session_id);
                            setEditTitle(session.title);
                          }}
                          title="Renombrar"
                        >
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                          </svg>
                        </button>
                        <button
                          className="history-action-btn history-action-delete"
                          onClick={(e) => handleDelete(e, session.session_id)}
                          title="Eliminar"
                        >
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                          </svg>
                        </button>
                      </div>
                    </>
                  )}
                </div>
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
