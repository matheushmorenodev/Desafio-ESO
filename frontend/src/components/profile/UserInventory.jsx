import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { CosmeticCard } from '../cosmetics/CosmeticCard';
import { useNavigate } from 'react-router-dom'; // <-- 1. IMPORTE O useNavigate

// Estilo do Grid (copiado do CosmeticList)
const gridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
  gap: '1rem',
  padding: '1rem 0',
};

export const UserInventory = () => {
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // <-- 2. INICIALIZE

  useEffect(() => {
    // ... (lógica de fetch não muda)
    const fetchInventory = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await apiClient.get('/profile/me/inventory');
        setItems(response.data);
      } catch (err) {
        setError("Não foi possível carregar seu inventário.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchInventory();
  }, []);

  // --- 3. NOVA FUNÇÃO DE NAVEGAÇÃO ---
  const handleItemSelect = (item) => {
    // Navega para a página de detalhes do item
    navigate(`/cosmetics/${item.id}`);
  };

  if (isLoading) return <div style={{color: 'white'}}>Carregando inventário...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;
  if (items.length === 0) return <div style={{color: 'white'}}>Você não possui nenhum item.</div>;

  return (
    <div style={gridStyle}>
      {items.map(item => (
        <CosmeticCard 
          key={item.id} 
          item={item} 
          onSelect={handleItemSelect} // <-- 4. PASSA A NOVA FUNÇÃO
          isSelected={false} // Não há 'seleção' nesta página
        />
      ))}
    </div>
  );
};