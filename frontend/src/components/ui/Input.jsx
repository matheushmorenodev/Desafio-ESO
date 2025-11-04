import React from 'react';

// Estilos que eram do Login.jsx e Filters.jsx
const inputGroupStyle = {
  textAlign: 'left',
  marginBottom: '1.5rem',
  width: '100%',
};

const labelStyle = {
  display: 'block',
  marginBottom: '0.5rem',
  fontWeight: '500',
  color: '#aaa', 
};

const inputStyle = {
  width: '100%',
  padding: '0.75rem 1rem',
  backgroundColor: '#2a2a2a', 
  border: '1px solid #444',
  borderRadius: '4px',
  color: 'white',
  fontSize: '1rem',
  boxSizing: 'border-box',
};

// Componente "wrapper" que inclui o label e o input
export const Input = ({ label, id, ...props }) => {
  return (
    <div style={inputGroupStyle}>
      {/* Só mostra o label se ele for fornecido */}
      {label && <label style={labelStyle} htmlFor={id}>{label}</label>}
      
      <input
        id={id}
        style={inputStyle}
        {...props} // Passa todas as outras props (type, value, onChange, placeholder, etc.)
      />
    </div>
  );
};