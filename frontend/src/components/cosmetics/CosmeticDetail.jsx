import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import apiClient from '../../services/apiClient';
import { Button } from '../ui/Button'; // <-- Importa o botão reutilizável

// --- Estilos para o painel de detalhes ---
const detailStyle = {
  backgroundColor: '#1e1e1e',
  padding: '2rem',
  borderRadius: '8px',
  color: 'white',
};
const imageStyle = {
  width: '100%',
  borderRadius: '8px',
  backgroundColor: '#2a2a2a',
  marginBottom: '1rem',
};
const titleStyle = {
  fontSize: '1.8rem',
  fontWeight: 'bold',
  lineHeight: 1.2,
};
const descriptionStyle = {
  color: '#b3b3b3', // 3. Cor secundária
  lineHeight: 1.6, // 1. Line-height
  maxWidth: '75ch', // 4. Limita a largura da linha
  margin: '1rem 0',
};
const infoRowStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  margin: '0.5rem 0',
};
const priceStyle = {
  fontSize: '1.5rem',
  fontWeight: 'bold',
  color: '#00bfff', // Ciano
};
const statusTagStyle = {
  fontSize: '0.9rem',
  padding: '4px 8px',
  borderRadius: '4px',
  fontWeight: 'bold',
  color: 'black',
};
const errorStyle = {
  color: '#ff4d4d',
  marginTop: '1rem',
  textAlign: 'center',
};
// --- Fim dos Estilos ---

export const CosmeticDetail = ({ item }) => {
  // Pega as novas funções do contexto
  const { 
    user, 
    updateUser, 
    inventory, // O Set() de IDs
    addItemToInventory, 
    removeItemFromInventory 
  } = useAuth();
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // 'isAcquired' agora é calculado pelo 'inventory' global
  const isAcquired = inventory.has(item.id);
  const isOnSale = item.is_on_sale;
  
  const handleBuy = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.post(`/cosmetics/${item.id}/buy`);
      
      // ATUALIZAÇÃO INSTANTÂNEA
      updateUser(response.data);      // Atualiza V-Bucks na Navbar
      addItemToInventory(item.id);  // Atualiza o inventário local (corrige o bug)

    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao comprar item.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReturn = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.post(`/cosmetics/${item.id}/return`);
      
      // ATUALIZAÇÃO INSTANTÂNEA
      updateUser(response.data);        // Atualiza V-Bucks na Navbar
      removeItemFromInventory(item.id); // Atualiza o inventário local (corrige o bug)
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao devolver item.');
    } finally {
      setIsLoading(false);
    }
  };

  // Lógica para renderizar botões (agora usa o componente <Button />)
  const renderButtons = () => {
    if (!user) {
      return (
        <Button variant="primary" disabled={true}>
          Faça login para comprar
        </Button>
      );
    }
    if (isAcquired) {
      return (
        <Button 
          variant="danger" // <-- Usa a variante "perigo" (vermelho)
          onClick={handleReturn}
          disabled={isLoading}
        >
          {isLoading ? 'Devolvendo...' : 'Devolver Item'}
        </Button>
      );
    }
    if (isOnSale) {
      return (
        <Button 
          variant="primary" // <-- Usa a variante "primária" (ciano)
          onClick={handleBuy}
          disabled={isLoading}
        >
          {isLoading ? 'Comprando...' : 'Comprar'}
        </Button>
      );
    }
    return (
      <Button variant="primary" disabled={true}>
        Indisponível na Loja
      </Button>
    );
  };

  return (
    <div style={detailStyle}>
      <img src={item.image_url} alt={item.name} style={imageStyle} />
      
      <h2 style={titleStyle}>{item.name}</h2>

      <div style={infoRowStyle}>
        <span style={{color: '#aaa'}}>{item.type}</span>
        <span style={{...statusTagStyle, backgroundColor: '#555', color: 'white'}}>
          {item.rarity}
        </span>
      </div>

      <div style={infoRowStyle}>
        <span>Status:</span>
        <div>
          {isOnSale && (
            <span style={{...statusTagStyle, backgroundColor: '#007bff'}}>
              À Venda
            </span>
          )}
          {item.is_new && (
            <span style={{...statusTagStyle, marginLeft: '4px', backgroundColor: '#FFC107'}}>
              Novo
            </span>
          )}
        </div>
      </div>
      
      <div style={infoRowStyle}>
        <span>Preço:</span>
        <span style={priceStyle}>
          {isOnSale ? `💎 ${item.price} VB` : '---'}
        </span>
      </div>

      <div style={{marginTop: '2rem'}}>
        {renderButtons()}
      </div>

      {error && (
        <p style={errorStyle}>{error}</p>
      )}
    </div>
  );
};