import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';

const pageStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '80vh',
};
const formContainerStyle = {
  backgroundColor: '#1e1e1e', 
  padding: '2rem 3rem',
  borderRadius: '8px',
  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)',
  width: '100%',
  maxWidth: '400px',
  color: 'white',
  textAlign: 'center',
};
const titleStyle = {
  fontSize: '2.5rem',
  fontWeight: 'bold',
  marginBottom: '2rem',
};
const linkStyle = {
  color: '#00bfff',
  textDecoration: 'none',
  fontSize: '0.9rem',
  display: 'block', 
  marginTop: '1rem',
};
const errorStyle = {
  color: '#ff4d4d',
  marginTop: '1rem',
};
// --- Fim dos Estilos ---

export const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.user) {
      navigate('/profile'); 
    }
  }, [auth.user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      await auth.register(email, password);
      navigate('/profile'); 
    } catch (err) {
      const apiError = err.response?.data?.detail || 'Falha ao registrar. Tente novamente.';
      if (Array.isArray(apiError)) {
        setError(apiError[0].msg);
      } else {
        setError(apiError);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={pageStyle}>
      <div style={formContainerStyle}>
        <h1 style={titleStyle}>Registrar</h1>
        <form onSubmit={handleSubmit}>
          
          <Input
            label="Email"
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="seuemail@exemplo.com"
            required
          />
          
          <Input
            label="Password"
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Mín. 6 caracteres, 1 maiúscula, 1 especial"
            required
          />
          
          {error && <p style={errorStyle}>{error}</p>}
          <Button
            type="submit"
            variant="primary"
            disabled={isLoading}
          >
            {isLoading ? 'Registrando...' : 'Criar Conta'}
          </Button>
          
        </form>

        <Link to="/login" style={linkStyle}>
          Já tem uma conta? Faça login
        </Link>
      </div>
    </div>
  );
};