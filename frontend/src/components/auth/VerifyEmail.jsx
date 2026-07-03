import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import '../../styles/main.css';

const API_BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api';

function VerifyEmail() {
  const { key } = useParams();
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

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
    <div className="auth-container">
      <div className="auth-card">
        <Link to="/" className="auth-logo">NURA</Link>
        <h2 className="auth-title">Verificación de Correo</h2>

        {status === 'loading' && (
          <div className="auth-loading">Verificando tu correo electrónico...</div>
        )}

        {status === 'success' && (
          <>
            <div className="auth-success">
              ¡Correo electrónico verificado con éxito! Ya puedes iniciar sesión.
            </div>
            <div className="auth-links" style={{ marginTop: '1rem' }}>
              <Link to="/login" className="auth-link">Iniciar Sesión</Link>
            </div>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="auth-error">{error}</div>
            <div className="auth-links" style={{ marginTop: '1rem' }}>
              <Link to="/login" className="auth-link">Volver a Iniciar Sesión</Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default VerifyEmail;
