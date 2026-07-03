import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../styles/main.css';

function Home() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  return (
    <div className="home-container">
      {/* Top Bar */}
      <div className="home-topbar">
        <div className="home-auth-buttons">
          {user ? (
            <>
              <span className="user-email">{user.email}</span>
              <button className="logout-btn" onClick={logout}>Cerrar Sesión</button>
            </>
          ) : (
            <>
              <Link to="/login" className="auth-link-btn">Iniciar Sesión</Link>
              <Link to="/register" className="auth-primary-btn">Crear Cuenta</Link>
            </>
          )}
        </div>
      </div>

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
