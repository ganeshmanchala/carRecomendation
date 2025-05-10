import { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  console.log(user)
  const checkAuth = async () => {
    try {
      const { data } = await axios.get(`${apiUrl}/checkAuth`, {
        withCredentials: true
      });
      if (data.isAuthenticated) {
        setUser(data.user);
      }
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    const { data } = await axios.post(`${apiUrl}/login`, credentials, {
      withCredentials: true
    });
    await checkAuth();
    return data;
  };

  const logout = async () => {
    await axios.post(`${apiUrl}/logout`, {}, {
      withCredentials: true
    });
    setUser(null);
  };

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);