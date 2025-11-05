import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';

// --- Estilos para o novo layout de lista (baseado no seu design) ---
const listContainerStyle = {
  width: '100%',
  color: 'white',
  marginTop: '1.5rem',
};

const headerRowStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  padding: '0 0 0.75rem 0', // Padding alinhado com os cards
  color: '#b3b3b3',
  textTransform: 'uppercase',
  fontSize: '0.9rem',
  fontWeight: 'bold',
};

const cardStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  backgroundColor: '#1e1e1e', // Cor de fundo do card
  padding: '1.5rem 0',
  borderRadius: '8px',
  marginBottom: '0.75rem',
  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
};

// --- Estilos para as colunas (para alinhamento) ---
const columnStyle = {
    padding: '0 1.5rem',
    boxSizing: 'border-box',
};

const dateColStyle = { ...columnStyle, width: '120px' };
const itemColStyle = { ...columnStyle, flex: 1, fontWeight: 'bold' }; // flex: 1 faz esta coluna crescer
const typeColStyle = { ...columnStyle, width: '120px', color: '#aaa' };
const valueColStyle = { ...columnStyle, width: '120px', textAlign: 'right' };

const purchaseStyle = { // Valor negativo
  color: '#ff4d4d',
  fontWeight: 'bold',
};
const returnStyle = { // Valor positivo
  color: '#4CAF50',
  fontWeight: 'bold',
};
// --- Fim dos Estilos ---

export const UserHistory = () => {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await apiClient.get('/profile/me/history');
        setHistory(response.data);
      } catch (err) {
        setError("Não foi possível carregar seu histórico.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []);

  if (isLoading) {
    return <div style={{color: 'white'}}>Carregando histórico...</div>;
  }
  if (error) {
    return <div style={{color: 'red'}}>{error}</div>;
  }
  if (history.length === 0) {
    return <div style={{color: 'white'}}>Você ainda não fez nenhuma transação.</div>;
  }

  // --- RENDERIZAÇÃO ATUALIZADA (SEM <table>) ---
return (
    <div style={listContainerStyle}>
      {/* 1. O Cabeçalho */}
      <div style={headerRowStyle}>
        <span style={dateColStyle}>Data</span>
        <span style={itemColStyle}>Item</span>
        <span style={typeColStyle}>Tipo</span>
        <span style={valueColStyle}>Valor</span>
      </div>

      {/* 2. A Lista de Transações (Cards) */}
      {history.map((tx, index) => (
        <div key={index} style={cardStyle}>
          
          <span style={dateColStyle}>
            {new Date(tx.created_at).toLocaleDateString('pt-BR')}
          </span>
          
          <span style={itemColStyle}>
            {tx.cosmetic ? tx.cosmetic.name : `Pacote (Bundle)`}
          </span>
          
          <span style={typeColStyle}>
            {tx.type === 'purchase' ? '💰 Compra' : '🔁 Devolução'}
          </span>
          
          <span style={{
            ...valueColStyle, 
            ...(tx.type === 'purchase' ? purchaseStyle : returnStyle)
          }}>
            {tx.value.toLocaleString('pt-BR')} VB
          </span>

        </div>
      ))}
    </div>
  );
};