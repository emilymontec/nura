import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
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
import './styles/main.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/console" element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          } />
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
