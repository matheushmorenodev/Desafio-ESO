import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

// --- 1. IMPORTA O MÓDULO CSS ---
// O React magicamente transforma este arquivo em um objeto 'styles'
import styles from './Navbar.module.css';

// --- 2. TODOS OS OBJETOS DE ESTILO (navStyle, linkStyle, etc.) FORAM REMOVIDOS ---

export const Navbar = () => {
  const { user, logout, isLoading } = useAuth();

  const handleLogout = () => {
    logout();
  };

  if (isLoading) {
    return null; 
  }

  // --- 3. USA 'className' EM VEZ DE 'style' ---
  return (
    <nav className={styles.nav}>
      <div>
        <Link to="/" className={styles.link}>
          ESO Fortnite Store
        </Link>
        <Link to="/users" className={styles.link}>
          Usuários
        </Link>
      </div>
      <div>
        {user ? (
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span className={styles.vbucks}>💎 V-Bucks: {user.vbucks}</span>
            <Link to="/profile" className={styles.link}>
              Meu Perfil
            </Link>
            <span className={styles.text}>Olá, {user.email}</span>
            <button onClick={handleLogout} className={styles.button}>
              Logout
            </button>
          </div>
        ) : (
          <div>
            <Link to="/login" className={styles.link}>
              Login
            </Link>
            <Link to="/register" className={styles.link}>
              Registrar
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};