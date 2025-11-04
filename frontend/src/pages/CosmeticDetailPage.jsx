import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import apiClient from '../services/apiClient';
import { CosmeticDetail } from '../components/cosmetics/CosmeticDetail';

const pageStyle = {
  maxWidth: '700px', 
  margin: '2rem auto',
  color: 'white',
};

const backLinkStyle = {
  color: '#aaa',
  textDecoration: 'none',
  marginBottom: '1rem',
  display: 'inline-block',
};


export const CosmeticDetailPage = () => {
  const [item, setItem] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Pega o :id da URL (ex: /cosmetics/EID_Rhubarb)
  const { cosmeticId } = useParams(); 

  useEffect(() => {
    const fetchItem = async () => {
      setIsLoading(true);
      setError(null);
      if (!cosmeticId) {
        setError("Nenhum ID de item fornecido.");
        setIsLoading(false);
        return;
      }

      try {
        // 1. Busca no endpoint de detalhes do cosmético
        const response = await apiClient.get(`/cosmetics/${cosmeticId}`);
        setItem(response.data);
      } catch (err) {
        setError("Não foi possível carregar o item.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchItem();
  }, [cosmeticId]); // Roda de novo se o ID na URL mudar

  return (
    <div style={pageStyle}>
      <Link to="/" style={backLinkStyle}>&larr; Voltar ao Catálogo</Link>
      
      {isLoading && <div style={{color: 'white'}}>Carregando item...</div>}
      {error && <div style={{color: 'red'}}>{error}</div>}
      
      {/* 2. Reutiliza nosso componente de Detalhe! */}
      {item && (
        <CosmeticDetail item={item} />
      )}
    </div>
  );
};