import React, { useState, useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import apiClient from '../services/apiClient';
import { CosmeticList } from '../components/cosmetics/CosmeticList';

const pageStyle = {
  maxWidth: '960px',
  margin: '0 auto',
  color: 'white',
};
const titleStyle = {
  fontSize: '2rem',
  fontWeight: 'bold',
  marginBottom: '2rem',
};
const backLinkStyle = {
  color: '#aaa',
  textDecoration: 'none',
  marginBottom: '1rem',
  display: 'inline-block',
};

export const UserDetail = () => {
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Pega o :userId da URL (ex: /users/1)
  const { userId } = useParams(); 
  
  // Pega o 'userEmail' que passamos via <Link> 
  const location = useLocation();
  const userEmail = location.state?.userEmail || `Usuário ${userId}`;

  useEffect(() => {
    const fetchUserInventory = async () => {
      setIsLoading(true);
      setError(null);
      try {
        // Busca no endpoint de inventário PÚBLICO
        const response = await apiClient.get(`/users/${userId}/inventory`);
        setItems(response.data);
      } catch (err) {
        setError("Não foi possível carregar o inventário deste usuário.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUserInventory();
  }, [userId]); // Roda de novo se o ID do usuário na URL mudar

  return (
    <div style={pageStyle}>
      <Link to="/users" style={backLinkStyle}>&larr; Voltar para Usuários</Link>
      <h1 style={titleStyle}>Inventário de: {userEmail}</h1>

      <CosmeticList
        items={items}
        isLoading={isLoading}
        error={error}
        onSelectItem={() => {}} 
        selectedItem={null}
      />
    </div>
  );
};