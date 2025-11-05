import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
// --- 1. IMPORTA NOSSOS NOVOS COMPONENTES ---
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';

// --- Estilos da PÁGINA (ainda ficam aqui) ---
const pageStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '80vh',
  // backgroundColor foi movido para o index.css global
};
const formContainerStyle = {
  backgroundColor: '#1e1e1e', 
  padding: '4rem',
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
// --- FIM DOS ESTILOS ---

export const Login = () => {
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
      await auth.login(email, password);
      navigate('/profile'); 
    } catch (err) {
      const apiError = err.response?.data?.detail || 'Falha ao fazer login. Tente novamente.';
      setError(apiError);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={pageStyle}>
      <div style={formContainerStyle}>
        <h1 style={titleStyle}>Log in</h1>
        <form onSubmit={handleSubmit}>
          
          {/* --- 2. CÓDIGO REATORADO --- */}
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
            placeholder="Sua senha"
            required
          />
          {/* --- FIM DA REATORAÇÃO --- */}

          <Link to="/forgot-password" style={{...linkStyle, textAlign: 'right'}}>
            Esqueceu a senha?
          </Link>
          
          {error && <p style={errorStyle}>{error}</p>}

          {/* --- 3. BOTÃO REATORADO --- */}
          <Button
            type="submit"
            variant="primary"
            disabled={isLoading}
          >
            {isLoading ? 'Carregando...' : 'Log in'}
          </Button>
          {/* --- FIM DA REATORAÇÃO --- */}
        </form>

        <Link to="/register" style={linkStyle}>
          Não tem uma conta? Registre-se
        </Link>
      </div>
    </div>
  );
};