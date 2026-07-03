import { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import AmbientBackground from '../landing/AmbientBackground';
import Navigation from '../landing/Navigation';
import '../../styles/landing.css';

function PasswordResetConfirm() {
  const { uid, token } = useParams();
  const [newPassword1, setNewPassword1] = useState('');
  const [newPassword2, setNewPassword2] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const { confirmResetPassword } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    document.body.classList.add('landing-active');
    return () => document.body.classList.remove('landing-active');
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (newPassword1 !== newPassword2) {
      setError('Las contraseñas no coinciden');
      return;
    }

    setLoading(true);

    try {
      await confirmResetPassword(uid, token, newPassword1, newPassword2);
      setSuccess('¡Contraseña restablecida con éxito! Redirigiendo...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
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
              <span>NUEVA CONTRASEÑA</span>
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

            {!success && (
              <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <label style={{
                    fontFamily: 'IBM Plex Mono, monospace',
                    fontSize: '12px',
                    color: 'var(--ink-soft)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.06em'
                  }} htmlFor="newPassword1">
                    Nueva Contraseña
                  </label>
                  <input
                    type="password"
                    id="newPassword1"
                    value={newPassword1}
                    onChange={(e) => setNewPassword1(e.target.value)}
                    required
                    placeholder="Tu nueva contraseña"
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
                  }} htmlFor="newPassword2">
                    Confirmar Nueva Contraseña
                  </label>
                  <input
                    type="password"
                    id="newPassword2"
                    value={newPassword2}
                    onChange={(e) => setNewPassword2(e.target.value)}
                    required
                    placeholder="Confirma tu nueva contraseña"
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
                  {loading ? 'Cargando...' : 'Restablecer Contraseña'}
                </button>
              </form>
            )}

            <div style={{
              display: 'flex',
              gap: '8px',
              marginTop: '24px',
              justifyContent: 'center',
              fontFamily: 'IBM Plex Mono, monospace',
              fontSize: '12px'
            }}>
              <Link to="/login" style={{ color: 'var(--brass)', textDecoration: 'none' }}>Volver a Iniciar Sesión</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PasswordResetConfirm;
