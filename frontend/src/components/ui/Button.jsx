import React from 'react';

// Estilo base que TODOS os botões compartilham
const baseStyle = {
  width: '100%',
  padding: '0.75rem',
  border: 'none',
  borderRadius: '4px',
  fontSize: '1.1rem',
  fontWeight: 'bold',
  cursor: 'pointer',
  marginTop: '1rem',
  opacity: 1,
  transition: 'opacity 0.2s',
};

// Estilos de "Variante" que mudam a cor
const variants = {
  primary: { // Botão Ciano (Login, Comprar)
    backgroundColor: '#00bfff',
    color: 'black',
  },
  danger: { // Botão Vermelho (Devolver)
    backgroundColor: '#ff4d4d',
    color: 'white',
  },
  secondary: { // Botão Sutil (Paginação)
    backgroundColor: '#2a2a2a',
    border: '1px solid #444',
    color: 'white',
    fontSize: '1rem',
    width: 'auto', // Paginação não é 100%
  },
};

const disabledStyle = {
  ...baseStyle,
  backgroundColor: '#444',
  color: '#888',
  cursor: 'not-allowed',
};

export const Button = ({ 
  children, 
  onClick, 
  type = "button",    // Padrão é 'button'
  variant = "primary", // Padrão é 'primary' (ciano)
  disabled = false,
  style = {}           // Para estilos extras (ex: width)
}) => {

  // Combina o estilo base + a variante + estilos customizados
  const computedStyle = {
    ...baseStyle,
    ...variants[variant],
    ...style,
  };

  return (
    <button
      type={type}
      style={disabled ? disabledStyle : computedStyle}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};