import React from 'react';
import { Link } from 'react-router-dom';

const pageStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '80vh',
  backgroundColor: '#121212',
};

const containerStyle = {
  backgroundColor: '#1e1e1e',
  padding: '2rem 3rem',
  borderRadius: '8px',
  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)',
  width: '100%',
  maxWidth: '450px',
  color: 'white',
  textAlign: 'center',
};

const titleStyle = {
  fontSize: '2rem',
  fontWeight: 'bold',
  marginBottom: '1rem',
};

const textStyle = {
  color: '#aaa',
  marginBottom: '2rem',
};

const linkStyle = {
  color: '#00bfff',
  textDecoration: 'none',
  fontSize: '1rem',
  display: 'block',
  marginTop: '1rem',
};

export const ForgotPassword = () => {
  return (
    <div style={pageStyle}>
      <div style={containerStyle}>
        <h1 style={titleStyle}>Recuperação de Senha</h1>
        <p style={textStyle}>
          EM MANUTENÇÃO
        </p>
        <Link to="/login" style={linkStyle}>
          &larr; Voltar para o Login
        </Link>
      </div>
    </div>
  );
};