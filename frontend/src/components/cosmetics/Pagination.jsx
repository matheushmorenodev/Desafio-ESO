import React from 'react';
import { Button } from '../ui/Button'; // <-- 1. IMPORTA O BOTÃO

// --- Estilos (agora sem os estilos de botão) ---
const paginationStyle = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  gap: '1rem',
  padding: '2rem 0',
  color: 'white',
};
// --- Fim dos Estilos ---

export const Pagination = ({ currentPage, totalPages, onPageChange }) => {

  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  if (totalPages <= 1) {
    return null;
  }

  return (
    <div style={paginationStyle}>
      {/* --- 2. BOTÕES REATORADOS --- */}
      <Button
        variant="secondary"
        style={{ width: 'auto', marginTop: 0 }} // <-- Estilo customizado
        onClick={handlePrevious}
        disabled={currentPage === 1}
      >
        Anterior
      </Button>
      
      <span>
        Página {currentPage} de {totalPages}
      </span>
      
      <Button
        variant="secondary"
        style={{ width: 'auto', marginTop: 0 }} // <-- Estilo customizado
        onClick={handleNext}
        disabled={currentPage === totalPages}
      >
        Próxima
      </Button>
      {/* --- FIM DA REATORAÇÃO --- */}
    </div>
  );
};