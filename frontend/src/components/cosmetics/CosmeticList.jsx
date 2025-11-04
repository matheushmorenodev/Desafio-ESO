import React from 'react';
import { CosmeticCard } from './CosmeticCard';

// --- Estilos ---
const gridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
  gap: '1rem',
  padding: '1rem 0', // Ajustado o padding
};
// --- Fim dos Estilos ---

// Este componente agora é "burro". Ele recebe os dados prontos.
export const CosmeticList = ({ 
  items, 
  isLoading, 
  error, 
  onSelectItem, 
  selectedItem 
}) => {

  if (isLoading) {
    return <div style={{color: 'white', padding: '2rem 0'}}>Buscando...</div>;
  }
  if (error) {
    return <div style={{color: 'red', padding: '2rem 0'}}>{error}</div>;
  }
  if (!items || items.length === 0) {
    return <div style={{color: 'white', padding: '2rem 0'}}>Nenhum cosmético encontrado para estes filtros.</div>;
  }

  // Renderiza o Grid
  return (
    <div style={gridStyle}>
      {items.map(item => (
        <CosmeticCard 
          key={item.id} 
          item={item} 
          onSelect={onSelectItem}
          isSelected={selectedItem?.id === item.id}
        />
      ))}
    </div>
  );
};