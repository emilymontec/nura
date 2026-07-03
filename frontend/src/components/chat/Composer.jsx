
import { useRef } from 'react';

export default function Composer({ onSendMessage, onFileUpload }) {
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = () => {
    const text = textareaRef.current.value.trim();
    if (text) {
      onSendMessage(text);
      textareaRef.current.value = '';
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  };

  return (
    <div className="composer-container">
      <div className="composer-box">
        <button
          className="attach-btn"
          onClick={() => fileInputRef.current.click()}
          title="Adjuntar dataset (.csv, .xlsx)"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
          </svg>
        </button>
        <textarea
          id="user-input"
          ref={textareaRef}
          placeholder="Escribe tu mensaje aquí..."
          onKeyDown={handleKeyDown}
          rows="1"
        ></textarea>
        <button
          className="send-btn"
          onClick={sendMessage}
          title="Enviar"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
      <input
        type="file"
        id="data-upload"
        accept=".csv,.xlsx,.xls,.pdf,.docx"
        hidden
        ref={fileInputRef}
        onChange={handleFileChange}
      />
      <div className="composer-footer">
        <span>Enter para enviar · Shift + Enter para nueva línea</span>
        <span>Verifica siempre la información clave antes de decidir.</span>
      </div>
    </div>
  );
}
