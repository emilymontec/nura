import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

const API_BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for stored tokens on mount
  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    const userData = localStorage.getItem('user');
    if (accessToken && userData) {
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  const register = async (email, password1, password2) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/registration/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password1, password2 }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || data.email?.[0] || data.password1?.[0] || 'Error al registrarse');
      }

      return data;
    } catch (error) {
      throw error;
    }
  };

  const login = async (email, password) => {
    try {
      // First try to get the JWT tokens
      const tokenResponse = await fetch(`${API_BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const tokenData = await tokenResponse.json();
      if (!tokenResponse.ok) {
        throw new Error(tokenData.detail || 'Credenciales incorrectas');
      }

      // Store tokens
      localStorage.setItem('accessToken', tokenData.access);
      localStorage.setItem('refreshToken', tokenData.refresh);

      // Get user details
      const userResponse = await fetch(`${API_BASE_URL}/auth/user/`, {
        headers: {
          'Authorization': `Bearer ${tokenData.access}`,
        },
      });

      const userData = await userResponse.json();
      if (userResponse.ok) {
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
      }

      return userData;
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    setUser(null);
  };

  const resetPassword = async (email) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/password/reset/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Error al enviar el correo de recuperación');
      }

      return true;
    } catch (error) {
      throw error;
    }
  };

  const confirmResetPassword = async (uid, token, new_password1, new_password2) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/password/reset/confirm/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ uid, token, new_password1, new_password2 }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Error al restablecer la contraseña');
      }

      return true;
    } catch (error) {
      throw error;
    }
  };

  const getProfile = async () => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      const response = await fetch(`${API_BASE_URL}/profile/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Error getting profile:', error);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      const response = await fetch(`${API_BASE_URL}/profile/`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
      });

      if (response.ok) {
        const updatedProfile = await response.json();
        // Update user in state and localStorage
        setUser(updatedProfile.user);
        localStorage.setItem('user', JSON.stringify(updatedProfile.user));
        return updatedProfile;
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      throw error;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        resetPassword,
        confirmResetPassword,
        getProfile,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
