import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import AmbientBackground from '../landing/AmbientBackground';
import Navigation from '../landing/Navigation';
import '../../styles/landing.css';

function Register() {
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    document.body.classList.add('landing-active');
    return () => document.body.classList.remove('landing-active');
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (password1 !== password2) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (password1.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    setLoading(true);

    try {
      const data = await register(email, password1, password2);
      // If JWT tokens were returned, user is auto-logged in
      if (data.access || data.access_token) {
        navigate('/chat');
      } else {
        setSuccess('¡Registro exitoso! Por favor verifica tu correo electrónico.');
        setTimeout(() => {
          navigate('/login');
        }, 5173);
      }
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
              <span>CREAR CUENTA</span>
            </div>
          </div>
          <div className="ticket-body">


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
            {success && (
              <div style={{
                fontFamily: 'IBM Plex Mono, monospace',
                fontSize: '12px',
                color: 'var(--signal)',
                marginBottom: '20px',
                padding: '10px 16px',
                background: 'rgba(74, 222, 128, 0.1)',
                borderLeft: '2px solid var(--signal)'
              }}>
                {success}
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
                }} htmlFor="password1">
                  Contraseña
                </label>
                <input
                  type="password"
                  id="password1"
                  value={password1}
                  onChange={(e) => setPassword1(e.target.value)}
                  required
                  placeholder="Tu contraseña (mínimo 8 caracteres)"
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
                }} htmlFor="password2">
                  Confirmar Contraseña
                </label>
                <input
                  type="password"
                  id="password2"
                  value={password2}
                  onChange={(e) => setPassword2(e.target.value)}
                  required
                  placeholder="Confirma tu contraseña"
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
                {loading ? 'Cargando...' : 'Crear Cuenta'}
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
              <span style={{ color: 'var(--ink-soft)' }}>¿Ya tienes cuenta?</span>
              <Link to="/login" style={{ color: 'var(--brass)', textDecoration: 'none' }}>Iniciar Sesión</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
