import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Home from './components/pages/Home';
import DashboardLayout from './components/dashboard/DashboardLayout';
import ChatApp from './components/chat/ChatApp';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import PasswordReset from './components/auth/PasswordReset';
import PasswordResetConfirm from './components/auth/PasswordResetConfirm';
import VerifyEmail from './components/auth/VerifyEmail';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Pricing from './components/pages/Pricing';
import Docs from './components/pages/Docs';
import Contact from './components/pages/Contact';
import About from './components/pages/About';
import Terms from './components/pages/Terms';
import Privacy from './components/pages/Privacy';
import MainViewport from './components/dashboard/MainViewport';
import './styles/main.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/about" element={<About />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/console" element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }>
            <Route index element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard" element={<MainViewport currentView="dashboard" />} />
            <Route path="datasets" element={<MainViewport currentView="datasets" />} />
            <Route path="chat-inteligente" element={<MainViewport currentView="chat-inteligente" />} />
            <Route path="reportes-ia" element={<MainViewport currentView="reportes-ia" />} />
            <Route path="mg-perfil" element={<MainViewport currentView="mg-perfil" />} />
            <Route path="mg-configuracion" element={<MainViewport currentView="mg-configuracion" />} />
            <Route path="mg-suscripcion" element={<MainViewport currentView="mg-suscripcion" />} />
            <Route path="mg-integraciones" element={<MainViewport currentView="mg-integraciones" />} />
            <Route path="ad-usuarios" element={<MainViewport currentView="ad-usuarios" />} />
            <Route path="ad-empresas" element={<MainViewport currentView="ad-empresas" />} />
            <Route path="ad-licencias" element={<MainViewport currentView="ad-licencias" />} />
            <Route path="ad-monitoreo" element={<MainViewport currentView="ad-monitoreo" />} />
          </Route>
          <Route path="/auth/login" element={<Login />} />
          <Route path="/auth/register" element={<Register />} />
          <Route path="/auth/password-reset" element={<PasswordReset />} />
          <Route path="/auth/password-reset/confirm/:uid/:token" element={<PasswordResetConfirm />} />
          <Route path="/auth/verify-email/:key" element={<VerifyEmail />} />
          <Route path="/chat" element={
            <ProtectedRoute>
              <ChatApp />
            </ProtectedRoute>
          } />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
