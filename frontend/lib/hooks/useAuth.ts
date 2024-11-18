import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import { User } from '@/types/user';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

interface UseAuthReturn extends AuthState {
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name: string) => Promise<void>;
  signOut: () => void;
  resetPassword: (email: string) => Promise<void>;
  verifyInvitation: (token: string) => Promise<void>;
}

export const useAuth = (): UseAuthReturn => {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    error: null,
  });

  // トークンの検証
  const verifyToken = useCallback((token: string) => {
    try {
      const decoded = jwt_decode(token);
      const currentTime = Date.now() / 1000;
      return (decoded as any).exp > currentTime;
    } catch {
      return false;
    }
  }, []);

  // 初期化時の認証状態チェック
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token && verifyToken(token)) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUserData();
    } else {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  }, [verifyToken]);

  // ユーザーデータの取得
  const fetchUserData = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/me`);
      setState({
        user: response.data,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      setState({
        user: null,
        isLoading: false,
        error: 'Failed to fetch user data',
      });
      localStorage.removeItem('token');
    }
  };

  // サインイン
  const signIn = async (email: string, password: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signin`, {
        email,
        password,
      });
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setState({
        user,
        isLoading: false,
        error: null,
      });
      router.push('/');
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: 'Invalid credentials',
      }));
    }
  };

  // サインアップ
  const signUp = async (email: string, password: string, name: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
        email,
        password,
        name,
      });
      await signIn(email, password);
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: 'Registration failed',
      }));
    }
  };

  // サインアウト
  const signOut = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setState({
      user: null,
      isLoading: false,
      error: null,
    });
    router.push('/auth/signin');
  };

  // パスワードリセット
  const resetPassword = async (email: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/reset-password`, {
        email,
      });
      setState(prev => ({ ...prev, isLoading: false }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: 'Password reset failed',
      }));
    }
  };

  // 招待の検証
  const verifyInvitation = async (token: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/verify-invitation`, {
        token,
      });
      setState(prev => ({ ...prev, isLoading: false }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: 'Invalid invitation token',
      }));
    }
  };

  return {
    ...state,
    signIn,
    signUp,
    signOut,
    resetPassword,
    verifyInvitation,
  };
};

export default useAuth;