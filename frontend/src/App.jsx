import { Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { ProtectedRoute } from './router/ProtectedRoute';

// --- Nossas Páginas ---
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Profile } from './pages/Profile';
import { Users } from './pages/Users';          
import { UserDetail } from './pages/UserDetail'; 
import { ForgotPassword } from './pages/ForgotPassword';
import { CosmeticDetailPage } from './pages/CosmeticDetailPage';

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        
        {/* --- Rotas Públicas --- */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/users" element={<Users />} />
        <Route path="/users/:userId" element={<UserDetail />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/cosmetics/:cosmeticId" element={<CosmeticDetailPage />} />
        
        {/* --- Rotas Privadas --- */}
        <Route element={<ProtectedRoute />}>
          <Route path="/profile" element={<Profile />} />
        </Route>

      </Route>
    </Routes>
  );
}

export default App;