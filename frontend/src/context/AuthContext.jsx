import { createContext, useState, useEffect } from 'react';
import apiClient from '../services/apiClient';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken') || null);
  
  // Um 'Set' é a forma mais rápida de checar se um item existe.
  const [inventory, setInventory] = useState(new Set());
  
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      localStorage.setItem('authToken', token);
      fetchProfileAndInventory(); //busca perfil e inventário
    } else {
      // Limpa tudo no logout
      localStorage.removeItem('authToken');
      setUser(null);
      setInventory(new Set()); 
      setIsLoading(false);
    }
  }, [token]); 

  const fetchProfileAndInventory = async () => {
    try {
      setIsLoading(true);
      
      //Busca o perfil (V-Bucks)
      const profilePromise = apiClient.get('/profile/me');
      //Busca o inventário (Lista de IDs)
      const inventoryPromise = apiClient.get('/profile/me/inventory');

      // Espera ambas as chamadas terminarem
      const [profileResponse, inventoryResponse] = await Promise.all([
        profilePromise,
        inventoryPromise,
      ]);

      // Salva o usuário
      setUser(profileResponse.data);
      
      // Salva o inventário como um Set 
      const inventoryIds = inventoryResponse.data.map(item => item.id);
      setInventory(new Set(inventoryIds));

    } catch (error) {
      console.error("Token inválido. Fazendo logout.", error);
      setToken(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await apiClient.post(
      '/auth/login', 
      formData,
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    setToken(response.data.access_token);
  };

  const register = async (email, password) => {
    await apiClient.post('/auth/register', { email, password });
    await login(email, password);
  };

  const logout = () => {
    navigate('/');
    setToken(null);
  };
  
  const updateUser = (updatedUserData) => {
    setUser(updatedUserData);
  };

  const addItemToInventory = (itemId) => {
    setInventory(prevInventory => new Set(prevInventory).add(itemId));
  };

  const removeItemFromInventory = (itemId) => {
    setInventory(prevInventory => {
      const newInventory = new Set(prevInventory);
      newInventory.delete(itemId);
      return newInventory;
    });
  };

  // Expõe o inventário e funcoes
  const value = {
    user,
    token,
    inventory,
    isLoading,
    login,
    register,
    logout,
    updateUser,
    addItemToInventory, 
    removeItemFromInventory 
  };

  return (
    <AuthContext.Provider value={value}>
      {!isLoading && children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };