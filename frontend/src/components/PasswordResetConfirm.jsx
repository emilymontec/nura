import { useState } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../styles/main.css';

function PasswordResetConfirm() {
  const { uid, token } = useParams();
  const [newPassword1, setNewPassword1] = useState('');
  const [newPassword2, setNewPassword2] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const { confirmResetPassword } = useAuth();
  const navigate = useNavigate();

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
    <div className="auth-container">
      <div className="auth-card">
        <Link to="/" className="auth-logo">NURA</Link>
        <h2 className="auth-title">Nueva Contraseña</h2>
        
        {error && <div className="auth-error">{error}</div>}
        {success && <div className="auth-success">{success}</div>}

        {!success && (
          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="newPassword1">Nueva Contraseña</label>
              <input
                type="password"
                id="newPassword1"
                value={newPassword1}
                onChange={(e) => setNewPassword1(e.target.value)}
                required
                placeholder="Tu nueva contraseña"
              />
            </div>

            <div className="form-group">
              <label htmlFor="newPassword2">Confirmar Nueva Contraseña</label>
              <input
                type="password"
                id="newPassword2"
                value={newPassword2}
                onChange={(e) => setNewPassword2(e.target.value)}
                required
                placeholder="Confirma tu nueva contraseña"
              />
            </div>

            <button 
              type="submit" 
              className="auth-btn"
              disabled={loading}
            >
              {loading ? 'Cargando...' : 'Restablecer Contraseña'}
            </button>
          </form>
        )}

        <div className="auth-links">
          <Link to="/login" className="auth-link">Volver a Iniciar Sesión</Link>
        </div>
      </div>
    </div>
  );
}

export default PasswordResetConfirm;
