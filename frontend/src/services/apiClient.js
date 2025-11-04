import axios from 'axios';

// 1. Cria a instância base do Axios com a URL do nosso .env
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// 2. O "Interceptor" Mágico
// Esta função roda ANTES de qualquer requisição ser enviada
apiClient.interceptors.request.use(
  (config) => {
    // Pega o token salvo no armazenamento local do navegador
    const token = localStorage.getItem('authToken');
    
    if (token) {
      // Se o token existir, adiciona ele no cabeçalho 'Authorization'
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;