//(Inclui Navbar e envolve o conteúdo)
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from './Navbar'; // Nossa Navbar

// Este componente garante que a Navbar apareça em todas as páginas
// e o <Outlet> é o espaço onde a página atual (Home, Profile, etc.)
// será renderizada.
export const MainLayout = () => {
  return (
    <div>
      <Navbar />
      <main style={{ 
        padding: '2rem',
        marginTop: '60px'
       }}>
        <Outlet />
      </main>
    </div>
  );
};