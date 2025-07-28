// frontend/src/context/AuthContext.tsx

import React, { createContext, useState, useEffect, ReactNode } from 'react';
import jwt_decode from 'jwt-decode';

interface AuthContextType {
  token: string | null;
  userId: number | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

interface DecodedToken {
  sub: number;
  exp: number;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('authToken'));
  const [userId, setUserId] = useState<number | null>(null);

  useEffect(() => {
    if (token) {
      try {
        const decodedToken: DecodedToken = jwt_decode(token);
        if (decodedToken.exp * 1000 > Date.now()) {
          setUserId(decodedToken.sub);
        } else {
          // Token expired
          logout();
        }
      } catch (error) {
        console.error("Invalid token:", error);
        logout();
      }
    }
  }, [token]);

  const login = (newToken: string) => {
    localStorage.setItem('authToken', newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setUserId(null);
  };

  const isAuthenticated = !!token && !!userId;

  const value = {
    token,
    userId,
    isAuthenticated,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
