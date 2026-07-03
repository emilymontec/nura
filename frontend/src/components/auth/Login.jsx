import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import AmbientBackground from '../landing/AmbientBackground';
import Navigation from '../landing/Navigation';
import '../../styles/landing.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    document.body.classList.add('landing-active');
    return () => document.body.classList.remove('landing-active');
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      navigate('/chat');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="nura-landing">
      <AmbientBackground />
      <Navigation />
      <div className="container" style={{ paddingTop: '150px' }}>
        <div className="ticket" style={{ maxWidth: '500px', margin: '0 auto' }}>
          <div className="ticket-head">
            <div className="ticket-head-l">
              <span className="rec-dot"></span>
              <span>INICIAR SESIÓN</span>
            </div>
          </div>
          <div className="ticket-body">
            <Link to="/" style={{ textDecoration: 'none' }}>
              <h2 style={{
                fontFamily: 'Fraunces, serif',
                fontWeight: '400',
                fontSize: '24px',
                color: 'var(--ink)',
                marginBottom: '28px',
                textAlign: 'center'
              }}>
                NURA
              </h2>
            </Link>

            {error && (
              <div style={{
                fontFamily: 'IBM Plex Mono, monospace',
                fontSize: '12px',
                color: 'var(--rust)',
                marginBottom: '20px',
                padding: '10px 16px',
                background: 'rgba(248, 113, 113, 0.1)',
                borderLeft: '2px solid var(--rust)'
              }}>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <label style={{
                  fontFamily: 'IBM Plex Mono, monospace',
                  fontSize: '12px',
                  color: 'var(--ink-soft)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.06em'
                }} htmlFor="email">
                  Correo Electrónico
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="tu@email.com"
                  style={{
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid var(--line)',
                    borderRadius: 'var(--radius)',
                    padding: '12px 16px',
                    color: 'var(--ink)',
                    fontFamily: 'IBM Plex Sans, sans-serif',
                    fontSize: '14px',
                    outline: 'none',
                    transition: 'border-color 0.2s'
                  }}
                  onFocus={(e) => e.target.style.borderColor = 'var(--brass)'}
                  onBlur={(e) => e.target.style.borderColor = 'var(--line)'}
                />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <label style={{
                  fontFamily: 'IBM Plex Mono, monospace',
                  fontSize: '12px',
                  color: 'var(--ink-soft)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.06em'
                }} htmlFor="password">
                  Contraseña
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="Tu contraseña"
                  style={{
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid var(--line)',
                    borderRadius: 'var(--radius)',
                    padding: '12px 16px',
                    color: 'var(--ink)',
                    fontFamily: 'IBM Plex Sans, sans-serif',
                    fontSize: '14px',
                    outline: 'none',
                    transition: 'border-color 0.2s'
                  }}
                  onFocus={(e) => e.target.style.borderColor = 'var(--brass)'}
                  onBlur={(e) => e.target.style.borderColor = 'var(--line)'}
                />
              </div>

              <button
                type="submit"
                className="btn-primary"
                disabled={loading}
                style={{
                  width: '100%',
                  display: 'flex',
                  justifyContent: 'center',
                  marginTop: '8px'
                }}
              >
                {loading ? 'Cargando...' : 'Iniciar Sesión'}
              </button>
            </form>

            <div style={{
              display: 'flex',
              gap: '8px',
              marginTop: '24px',
              justifyContent: 'center',
              fontFamily: 'IBM Plex Mono, monospace',
              fontSize: '12px'
            }}>
              <Link to="/password-reset" style={{ color: 'var(--brass)', textDecoration: 'none' }}>¿Olvidaste tu contraseña?</Link>
              <span style={{ color: 'var(--ink-faint)' }}>·</span>
              <Link to="/register" style={{ color: 'var(--brass)', textDecoration: 'none' }}>Crear una cuenta</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
