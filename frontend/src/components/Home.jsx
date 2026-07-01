import { useNavigate } from 'react-router-dom';
import '../styles/main.css';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1 className="home-logo">NURA</h1>
      <h2 className="home-subtitle">Inteligencia Conversacional para Análisis Empresarial</h2>
      <p className="home-description">
        Transforma tus datos estructurados en información accionable a través de conversaciones naturales.
        Analiza tendencias, detecta riesgos y recibe recomendaciones estratégicas sin necesidad de conocimientos técnicos.
      </p>
      <button className="home-btn" onClick={() => navigate('/chat')}>Comenzar Ahora</button>
      
      <div className="features">
        <div className="feature">
          <h3>📊 Análisis Automático</h3>
          <p>Carga tu dataset y recibe un análisis completo en segundos.</p>
        </div>
        <div className="feature">
          <h3>🤖 Multi-Agente</h3>
          <p>Especialistas virtuales para riesgos, oportunidades y estrategia.</p>
        </div>
        <div className="feature">
          <h3>💬 Lenguaje Natural</h3>
          <p>Pregunta lo que necesites como si hablaras con un analista.</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
