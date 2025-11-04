import React, { useState, useEffect } from 'react';
import apiClient from '../services/apiClient';
import { CosmeticList } from '../components/cosmetics/CosmeticList';
import { CosmeticDetail } from '../components/cosmetics/CosmeticDetail';
import { Filters } from '../components/cosmetics/Filters';
import { Pagination } from '../components/cosmetics/Pagination';

const homeStyle = {
  display: 'grid',
  gridTemplateColumns: '2fr 1fr', 
  gap: '2rem',
  backgroundColor: '#121212',
  color: 'white',
};

const listContainerStyle = {
  overflowY: 'auto', // scroll na coluna esquerda
  maxHeight: 'calc(100vh - 100px)', // altura da navbar
  paddingRight: '1rem', // Espaço para a barra de scroll
};
const detailContainerStyle = {
  position: 'sticky', 
  top: '2rem',
  alignSelf: 'start', 
};

export const Home = () => {
  // Estado principal da página
  const [selectedItem, setSelectedItem] = useState(null);
  
  const [filters, setFilters] = useState({
    name: '', type: '', rarity: '',
    is_new: false, is_on_sale: false, is_on_promotion: false,
    date_from: '', date_to: '',
  });
  
  // Estado da Paginação
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  
  // Estado dos Dados
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Lógica de busca de dados
  useEffect(() => {
    const fetchCosmetics = async () => {
      setIsLoading(true);
      setError(null);
      setSelectedItem(null); // Limpa a seleção ao buscar
      
      const params = new URLSearchParams();
      params.append('page', page);
      params.append('limit', 20); // Limite por página

      // Adicionando filtros
      if (filters.name) params.append('name', filters.name);
      if (filters.type) params.append('type', filters.type);
      if (filters.rarity) params.append('rarity', filters.rarity);
      if (filters.is_new) params.append('is_new', true);
      if (filters.is_on_sale) params.append('is_on_sale', true);
      if (filters.is_on_promotion) params.append('is_on_promotion', true);
      if (filters.date_from) params.append('date_from', filters.date_from);
      if (filters.date_to) params.append('date_to', filters.date_to);
      
      try {
        const response = await apiClient.get(`/cosmetics`, { params });
        // Salva os dados no estado
        setItems(response.data.items);
        setTotalPages(response.data.total_pages);
      } catch (err) {
        setError("Não foi possível carregar os cosméticos.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    // espera 500ms quando o usuario para de digitar
    const delayDebounceFn = setTimeout(() => {
      fetchCosmetics();
    }, 500); 

    return () => clearTimeout(delayDebounceFn);

  }, [filters, page]); //roda de novo se os filtros ou a página mudar

  // Função para atualizar os filtros
  const handleFilterChange = (filterName, value) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [filterName]: value
    }));
    setPage(1); // Reseta a página para 1 toda vez que um filtro muda
  };

  return (
    <div style={homeStyle}>
      {/* Coluna da Esquerda: Lista */}
      <div style={listContainerStyle}>
        <h2>Catálogo</h2>
        
        <Filters 
          filters={filters} 
          onFilterChange={handleFilterChange} 
        />
        
        {/* dados da cosmeticlist */}
        <CosmeticList 
          onSelectItem={setSelectedItem}
          selectedItem={selectedItem}
          items={items}
          isLoading={isLoading}
          error={error}
        />
        
        {/* renderizando a pagina */}
        <Pagination 
          currentPage={page}
          totalPages={totalPages}
          onPageChange={setPage} // Passa a função de mudar a página
        />
      </div>

      {/* coluna da direita: itens detalhados */}
      <div style={detailContainerStyle}>
        {selectedItem ? (
          <CosmeticDetail item={selectedItem} />
        ) : (
          <div style={{
            backgroundColor: '#1e1e1e', 
            padding: '1.5rem', 
            borderRadius: '8px',
            textAlign: 'center',
          }}>
            <h3>Selecione um item</h3>
            <p>Clique em um item da lista para ver os detalhes e comprar.</p>
          </div>
        )}
      </div>
    </div>
  );
};