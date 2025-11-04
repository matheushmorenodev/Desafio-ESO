// hook para acessar o AuthContext)
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

// Este hook é um atalho para facilitar o acesso ao contexto
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};