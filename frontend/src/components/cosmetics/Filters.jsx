import React from 'react';

const filterBarStyle = {
  display: 'flex',
  gap: '1rem',
  alignItems: 'center',
  padding: '1rem',
  backgroundColor: '#1e1e1e', 
  borderRadius: '8px',
  marginBottom: '1.5rem',
  flexWrap: 'wrap', //permitindo que os filtros quebrem linha em telas menores
};

const inputStyle = {
  flex: 1, // Faz a barra de busca ocupar mais espaço
  minWidth: '200px',
  padding: '0.75rem 1rem',
  backgroundColor: '#2a2a2a',
  border: '1px solid #444',
  borderRadius: '4px',
  color: 'white',
  fontSize: '1rem',
};

const selectStyle = {
  ...inputStyle,
  flex: 'none', // Dropdowns têm tamanho fixo
  minWidth: '120px',
  appearance: 'none', 
  cursor: 'pointer',
};

const checkboxContainerStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '0.5rem',
  color: 'white',
  cursor: 'pointer',
};

const dateGroupStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '0.5rem',
  color: '#aaa',
};
const dateInputStyle = {
  ...inputStyle,
  minWidth: '150px',
  flex: 'none',
  colorScheme: 'dark', 
};

export const Filters = ({ filters, onFilterChange }) => {

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    onFilterChange(name, newValue);
  };

  return (
    <div style={filterBarStyle}>
      {/* 1. Busca por Nome */}
      <input
        type="text"
        name="name"
        style={inputStyle}
        placeholder="Search..."
        value={filters.name}
        onChange={handleChange}
      />
      
      {/* 2. Filtro por Tipo */}
      <select 
        name="type" 
        style={selectStyle} 
        value={filters.type} 
        onChange={handleChange}
      >
        <option value="">Todos os Tipos</option>
        <option value="outfit">Outfit (Skin)</option>
        <option value="backpack">Backpack</option>
        <option value="pickaxe">Pickaxe</option>
        <option value="emote">Emote</option>
      </select>
      
      {/* 3. Filtro por Raridade */}
      <select 
        name="rarity" 
        style={selectStyle} 
        value={filters.rarity} 
        onChange={handleChange}
      >
        <option value="">Todas as Raridades</option>
        <option value="common">Comum</option>
        <option value="uncommon">Incomum</option>
        <option value="rare">Raro</option>
        <option value="epic">Épico</option>
        <option value="legendary">Lendário</option>
      </select>
      
      {/* 4. Checkboxes */}
      <label style={checkboxContainerStyle}>
        <input 
          type="checkbox" 
          name="is_new"
          checked={filters.is_new}
          onChange={handleChange}
        />
        Novos
      </label>
      
      <label style={checkboxContainerStyle}>
        <input 
          type="checkbox" 
          name="is_on_sale"
          checked={filters.is_on_sale}
          onChange={handleChange}
        />
        Á Venda
      </label>

      {/*promoção*/}
      <label style={checkboxContainerStyle}>
        <input 
          type="checkbox" 
          name="is_on_promotion"
          checked={filters.is_on_promotion}
          onChange={handleChange}
        />
        Promoção
      </label>

      {/* --- 6. FILTRO NOVO: INTERVALO DE DATAS  --- */}
      <div style={dateGroupStyle}>
        <span>De:</span>
        <input 
          type="date"
          name="date_from"
          style={dateInputStyle}
          value={filters.date_from}
          onChange={handleChange}
        />
        <span>Até:</span>
        <input 
          type="date"
          name="date_to"
          style={dateInputStyle}
          value={filters.date_to}
          onChange={handleChange}
        />
      </div>
    </div>
  );
};