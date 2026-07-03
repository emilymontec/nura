import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

function Navigation() {
  const { user, logout } = useAuth();

  return (
    <nav>
      <Link to="/" className="logo">
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
          <path d="M1 11H5L7.5 4L11.5 18L14 11H21" stroke="#191B14" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <span className="logo-t">NURA<span>.AI</span></span>
      </Link>
      <div className="rec-indicator">
        <span className="rec-dot"></span>
        <span>ESCUCHA ACTIVA</span>
      </div>
      <div className="nav-links">
        <a href="#panel" className="active">Plataforma</a>
        <a href="#instrumento">Instrumento</a>
        {user ? (
          <>
            <span className="user-email">{user.email}</span>
            <button onClick={logout}>Cerrar Sesión</button>
            <Link to="/chat" className="cta">Ir al Chat</Link>
          </>
        ) : (
          <>
            <Link to="/login">Iniciar Sesión</Link>
            <Link to="/register" className="cta">Crear Cuenta</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navigation;
