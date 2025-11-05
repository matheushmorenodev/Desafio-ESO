import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

// --- Estilos ---
const navStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  padding: '1rem 2rem',
  backgroundColor: '#1a1a1a',
  color: 'white',
  position: 'fixed', // Fixa a navbar no topo
  top: 0,
  left: 0,
  width: '100%',
  zIndex: 1000, // Garante que ela fique na frente de todo o conteúdo
  boxSizing: 'border-box',
  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.4)',
};
const linkStyle = {
  color: 'white',
  textDecoration: 'none',
  margin: '0 0.5rem',
};
const vbucksStyle = {
  color: '#00bfff',
  fontWeight: 'bold',
  marginRight: '1rem',
};
const buttonStyle = {
  ...linkStyle,
  background: 'none',
  border: 'none',
  cursor: 'pointer',
  fontSize: 'inherit',
  fontFamily: 'inherit',
};
const textStyle = {
  ...linkStyle,
  color: '#aaa',
  cursor: 'default',
};
// --- Fim dos Estilos ---

export const Navbar = () => {
  const { user, logout, isLoading } = useAuth();

  const handleLogout = () => {
    logout(); // O AuthContext cuida da navegação
  };

  if (isLoading) {
    return null; // Não mostra nada até o auth estar pronto
  }

  return (
    <nav style={navStyle}>
      <div>
        <Link to="/" style={linkStyle}>ESO Fortnite Store</Link>
        
        {/* --- ADIÇÃO AQUI --- */}
        <Link to="/users" style={linkStyle}>Usuários</Link>
        {/* --- FIM DA ADIÇÃO --- */}
      </div>
      <div>
        {user ? (
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span style={vbucksStyle}>💎 V-Bucks: {user.vbucks}</span>
            <Link to="/profile" style={linkStyle}>Meu Perfil</Link>
            <span style={textStyle}>Olá, {user.email}</span>
            <button onClick={handleLogout} style={buttonStyle}>
              Logout
            </button>
          </div>
        ) : (
          <div>
            <Link to="/login" style={linkStyle}>Login</Link>
            <Link to="/register" style={linkStyle}>Registrar</Link>
          </div>
        )}
      </div>
    </nav>
  );
};