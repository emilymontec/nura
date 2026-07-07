import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import AmbientBackground from '../landing/AmbientBackground';
import Navigation from '../landing/Navigation';
import '../../styles/landing.css';

const API_BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api';

function VerifyEmail() {
  const { key } = useParams();
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  useEffect(() => {
    document.body.classList.add('landing-active');
    return () => document.body.classList.remove('landing-active');
  }, []);

  useEffect(() => {
    if (!key) {
      setStatus('error');
      setError('Enlace de verificación inválido.');
      return;
    }

    const verifyEmail = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/registration/verify-email/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ key }),
        });

        const data = await response.json();

        if (response.ok) {
          setStatus('success');
        } else {
          setStatus('error');
          setError(data.detail || data.key?.[0] || 'Error al verificar el correo electrónico.');
        }
      } catch {
        setStatus('error');
        setError('Error de conexión. Intenta de nuevo más tarde.');
      }
    };

    verifyEmail();
  }, [key]);

  return (
    <div className="nura-landing">
      <AmbientBackground />
      <Navigation />
      <div className="container" style={{ paddingTop: '150px' }}>
        <div className="ticket" style={{ maxWidth: '500px', margin: '0 auto' }}>
          <div className="ticket-head">
            <div className="ticket-head-l">
              <span className="rec-dot"></span>
              <span>VERIFICACIÓN DE CORREO</span>
            </div>
          </div>
          <div className="ticket-body">


            {status === 'loading' && (
              <div style={{
                fontFamily: 'IBM Plex Mono, monospace',
                fontSize: '12px',
                color: 'var(--ink-soft)',
                textAlign: 'center'
              }}>
                Verificando tu correo electrónico...
              </div>
            )}

            {status === 'success' && (
              <>
                <div style={{
                  fontFamily: 'IBM Plex Mono, monospace',
                  fontSize: '12px',
                  color: 'var(--signal)',
                  marginBottom: '20px',
                  padding: '10px 16px',
                  background: 'rgba(74, 222, 128, 0.1)',
                  borderLeft: '2px solid var(--signal)'
                }}>
                  ¡Correo electrónico verificado con éxito! Ya puedes iniciar sesión.
                </div>
                <div style={{
                  display: 'flex',
                  gap: '8px',
                  marginTop: '24px',
                  justifyContent: 'center',
                  fontFamily: 'IBM Plex Mono, monospace',
                  fontSize: '12px'
                }}>
                  <Link to="/login" style={{ color: 'var(--brass)', textDecoration: 'none' }}>Iniciar Sesión</Link>
                </div>
              </>
            )}

            {status === 'error' && (
              <>
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
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default VerifyEmail;
