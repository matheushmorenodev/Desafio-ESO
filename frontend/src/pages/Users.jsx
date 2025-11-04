import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../services/apiClient';
import { Pagination } from '../components/cosmetics/Pagination';

const pageStyle = {
  maxWidth: '960px',
  margin: '0 auto',
  color: 'white',
};
const titleStyle = {
  fontSize: '2.5rem',
  fontWeight: 'bold',
  marginBottom: '2rem',
};
const listContainerStyle = {
  width: '100%',
};
const headerRowStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  padding: '0 1.5rem 0.75rem 1.5rem',
  color: '#aaa',
  textTransform: 'uppercase',
  fontSize: '0.9rem',
  fontWeight: 'bold',
};
const cardStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  backgroundColor: '#1e1e1e',
  padding: '1.5rem',
  borderRadius: '8px',
  marginBottom: '0.75rem',
  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
};
const columnStyle = {
  padding: '0 0.5rem',
};
const emailColStyle = { ...columnStyle, flex: 1, fontWeight: 'bold' };
const dateColStyle = { ...columnStyle, width: '200px', color: '#aaa' };
const linkColStyle = { ...columnStyle, width: '120px', textAlign: 'right' };

const profileLinkStyle = {
  color: '#00bfff',
  fontWeight: 'bold',
  textDecoration: 'none',
};

export const Users = () => {
  const [usersData, setUsersData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchUsers = async () => {
      setIsLoading(true);
      setError(null);
      try {
        // Busca no endpoint público de usuários
        const response = await apiClient.get('/users', {
          params: { page: page, limit: 10 } // Paginação
        });
        setUsersData(response.data);
      } catch (err) {
        setError("Não foi possível carregar a lista de usuários.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUsers();
  }, [page]); // Roda de novo se a 'page' mudar

  if (isLoading) {
    return <div style={{color: 'white'}}>Carregando usuários...</div>;
  }
  if (error) {
    return <div style={{color: 'red'}}>{error}</div>;
  }
  if (!usersData || usersData.items.length === 0) {
    return <div style={{color: 'white'}}>Nenhum usuário encontrado.</div>;
  }

  return (
    <div style={pageStyle}>
      <h1 style={titleStyle}>Usuários</h1>
      
      <div style={listContainerStyle}>
        {/* Cabeçalho da Lista */}
        <div style={headerRowStyle}>
          <span style={emailColStyle}>Usuário (Email)</span>
          <span style={dateColStyle}>Registrado em</span>
          <span style={linkColStyle}>Perfil</span>
        </div>

        {/* Lista de Usuários (Cards) */}
        {usersData.items.map((user) => (
          <div key={user.id} style={cardStyle}>
            <span style={emailColStyle}>{user.email}</span>
            <span style={dateColStyle}>
              {new Date(user.created_at).toLocaleDateString('pt-BR')}
            </span>
            <span style={linkColStyle}>
              {/* Passamos o 'email' para a próxima página */}
              <Link 
                to={`/users/${user.id}`} 
                state={{ userEmail: user.email }}
                style={profileLinkStyle}
              >
                Ver Perfil
              </Link>
            </span>
          </div>
        ))}
      </div>

      {/* Paginação */}
      <Pagination 
        currentPage={page}
        totalPages={usersData.total_pages}
        onPageChange={setPage}
      />
    </div>
  );
};