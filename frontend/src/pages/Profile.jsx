import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { UserInventory } from '../components/profile/UserInventory';
import { UserHistory } from '../components/profile/UserHistory';


const profilePageStyle = {
  maxWidth: '960px',
  margin: '0 auto',
  color: 'white',
};
const profileHeaderStyle = {
  backgroundColor: '#1e1e1e',
  padding: '2rem',
  borderRadius: '8px',
  marginBottom: '2rem',
  display: 'flex',
  alignItems: 'center',
  gap: '1.5rem',
};
const vbucksBalanceStyle = {
  fontSize: '1.8rem',
  fontWeight: 'bold',
  color: '#00bfff',
};
const tabContainerStyle = {
  display: 'flex',
  gap: '0.5rem',
  marginBottom: '1.5rem',
  borderBottom: '2px solid #2a2a2a',
};

const tabStyle = {
  background: 'none',
  border: 'none',
  fontFamily: 'inherit',
  
  padding: '0.75rem 1.5rem',
  cursor: 'pointer',
  fontSize: '1.1rem',
  fontWeight: '500',
  color: '#aaa',
  borderBottom: '3px solid transparent', 
};

const activeTabStyle = {
  ...tabStyle,
  color: 'white',
  borderColor: '#00bfff', 
};


export const Profile = () => {
  const [activeTab, setActiveTab] = useState('inventory'); 
  const { user } = useAuth(); 

  if (!user) {
    return <div>Carregando...</div>; 
  }

  return (
    <div style={profilePageStyle}>
      {/* 1. O Cabeçalho (do seu design) */}
      <div style={profileHeaderStyle}>
        <div>
          <h2>Olá, {user.email}</h2>
          <div style={vbucksBalanceStyle}>
            💎 {user.vbucks.toLocaleString('pt-BR')} VB
          </div>
        </div>
      </div>

      {/* 2. As Abas */}
      <div style={tabContainerStyle}>
        <button
          style={activeTab === 'inventory' ? activeTabStyle : tabStyle}
          onClick={() => setActiveTab('inventory')}
        >
          My Cosmetics
        </button>
        <button
          style={activeTab === 'history' ? activeTabStyle : tabStyle}
          onClick={() => setActiveTab('history')}
        >
          History
        </button>
      </div>

      {/* 3. O Conteúdo Condicional da Aba */}
      <div>
        {activeTab === 'inventory' ? (
          <UserInventory /> 
        ) : (
          <UserHistory />
        )}
      </div>
    </div>
  );
};