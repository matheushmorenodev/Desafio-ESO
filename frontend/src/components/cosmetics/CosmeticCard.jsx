import React from 'react';
import { useAuth } from '../../hooks/useAuth';

// --- Estilos para o Card ---
const cardStyle = {
  backgroundColor: '#1e1e1e',
  borderRadius: '8px',
  overflow: 'hidden',
  color: 'white',
  textDecoration: 'none',
  display: 'block',
  border: '2px solid transparent',
  cursor: 'pointer', // Adiciona cursor de clique
};
const selectedCardStyle = {
  ...cardStyle,
  borderColor: '#00bfff',
};
const imageStyle = {
  width: '100%',
  height: '180px',
  objectFit: 'cover',
  backgroundColor: '#2a2a2a',
};
const infoStyle = {
  padding: '1rem',
};
const nameStyle = {
  fontSize: '1.1rem',
  fontWeight: 'bold',
  marginBottom: '0.25rem',
  whiteSpace: 'nowrap',
  overflow: 'hidden',
  textOverflow: 'ellipsis',
};
const typeStyle = {
  fontSize: '0.9rem',
  color: '#aaa',
  marginBottom: '0.5rem',
};
const priceStyle = {
  fontSize: '1rem',
  fontWeight: 'bold',
  color: '#00bfff',
};
const statusIconStyle = {
  fontSize: '0.8rem',
  padding: '2px 6px',
  borderRadius: '4px',
  marginLeft: '4px',
  color: 'black', // Melhor legibilidade
  fontWeight: 'bold',
};
// --- Fim dos Estilos ---

export const CosmeticCard = ({ item, onSelect, isSelected }) => {
  // Pega o inventário global
  const { inventory } = useAuth(); 

  // 'isAcquired' é calculado pelo inventário global
  const isAcquired = inventory.has(item.id);
  const isOnSale = item.is_on_sale;
  const isNew = item.is_new;

  return (
    <div 
      style={isSelected ? selectedCardStyle : cardStyle}
      onClick={() => onSelect(item)}
    >
      <img src={item.image_url} alt={item.name} style={imageStyle} />
      <div style={infoStyle}>
        <h3 style={nameStyle}>{item.name}</h3>
        <p style={typeStyle}>{item.type}</p>
        
        {isOnSale ? (
          <span style={priceStyle}>💎 {item.price} VB</span>
        ) : (
          <span style={{...typeStyle, fontSize: '1rem'}}>Não está à venda</span>
        )}

        {/* Esta seção agora também atualizará instantaneamente */}
        <div>
          {isAcquired && (
            <span style={{...statusIconStyle, backgroundColor: '#4CAF50'}}>
              Adquirido
            </span>
          )}
          {isNew && !isAcquired && (
            <span style={{...statusIconStyle, backgroundColor: '#FFC107'}}>
              Novo
            </span>
          )}
        </div>
      </div>
    </div>
  );
};