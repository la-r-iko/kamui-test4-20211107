import axios from 'axios';
import { API_BASE_URL } from '../config';

// 認証関連の型定義
export interface SignInCredentials {
  email: string;
  password: string;
}

export interface SignUpData {
  email: string;
  password: string;
  name: string;
  role?: string;
}

export interface ResetPasswordData {
  email: string;
}

export interface VerifyInvitationData {
  token: string;
  password: string;
}

// API呼び出し関数
export const authApi = {
  /**
   * サインイン処理
   * @param credentials ログイン認証情報
   * @returns トークンと認証情報を含むレスポンス
   */
  signIn: async (credentials: SignInCredentials) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/auth/signin`,
        credentials
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * サインアップ処理
   * @param data ユーザー登録情報
   * @returns 登録結果を含むレスポンス
   */
  signUp: async (data: SignUpData) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/auth/signup`,
        data
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * パスワードリセット要求
   * @param data パスワードリセットに必要なメールアドレス
   * @returns リセット要求の結果
   */
  resetPassword: async (data: ResetPasswordData) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/auth/reset-password`,
        data
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * 招待検証処理
   * @param data 招待トークンと設定するパスワード
   * @returns 検証結果
   */
  verifyInvitation: async (data: VerifyInvitationData) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/auth/verify-invitation`,
        data
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * セッションの検証
   * @returns セッション有効性の確認結果
   */
  verifySession: async () => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/auth/verify-session`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * ログアウト処理
   */
  signOut: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};

// エラーハンドリング用のユーティリティ関数
export const handleAuthError = (error: any) => {
  if (error.response) {
    switch (error.response.status) {
      case 401:
        return 'メールアドレスまたはパスワードが正しくありません。';
      case 403:
        return 'アクセスが拒否されました。';
      case 422:
        return '入力内容に誤りがあります。';
      default:
        return 'エラーが発生しました。しばらく時間をおいて再度お試しください。';
    }
  }
  return 'ネットワークエラーが発生しました。接続を確認してください。';
};

export default authApi;