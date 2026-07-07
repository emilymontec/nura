
import Message from './Message';

export default function ChatContainer({ messages, loading, datasetContext, onPromptClick }) {
  const welcomePrompts = [
    {
      title: 'Presentación',
      text: 'Hola, preséntate y dime brevemente cómo puedes ayudarme.'
    },
    {
      title: 'KPIs',
      text: '¿Qué KPIs recomiendas revisar para un negocio de servicios?'
    },
    {
      title: 'Riesgos',
      text: '¿Cómo estructurar un análisis de riesgos financieros?'
    },
    {
      title: 'Resumen',
      text: '¿Me puedes dar un resumen de la información que acabo de subir?'
    }
  ];

  return (
    <>
      {messages.length === 0 && !datasetContext && (
        <div className="welcome-screen">
          <div className="welcome-core">
            <div className="terminal-stream">
              <p className="ai-thought">
                ¡Hola! Sube un archivo con tu información (Excel o CSV) y te ayudaré a entender qué significan tus números de forma sencilla.
              </p>
            </div>
          </div>
          <div className="welcome-prompts">
            {welcomePrompts.map((prompt, index) => (
              <button
                key={index}
                className="welcome-prompt-card"
                onClick={() => onPromptClick(prompt.text)}
              >
                <h3>{prompt.title}</h3>
                <p>{prompt.text}</p>
              </button>
            ))}
          </div>
        </div>
      )}

      {messages.map((msg, index) => (
        <Message key={index} message={msg} />
      ))}

      {loading && (
        <div className="message bot-msg loading">
          <div className="avatar nura-avatar">
          </div>
          <div className="msg-content">
            <span>Analizando...</span>
          </div>
        </div>
      )}
    </>
  );
}
