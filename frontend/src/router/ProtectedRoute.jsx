import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { Navigate, Outlet } from 'react-router-dom';

export const ProtectedRoute = () => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <div>Carregando...</div>; // Ou um componente <Spinner />
  }

  if (!user) {
    // Se não estiver logado, redireciona para a página de login
    return <Navigate to="/" replace />;
  }

  // Se estiver logado, renderiza a página filha (ex: <Profile />)
  return <Outlet />;
};