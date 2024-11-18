import axios from 'axios';
import { getAuthToken } from '../auth/token';

// 教材の型定義
export interface Material {
  id: string;
  title: string;
  description: string;
  fileUrl: string;
  fileType: string;
  createdAt: string;
  updatedAt: string;
  size: number;
  category: string;
  downloadCount: number;
}

// APIのベースURL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * 教材一覧を取得する
 * @param page ページ番号
 * @param limit 1ページあたりの件数
 * @param category カテゴリーでフィルター（オプション）
 */
export const getMaterials = async (
  page: number = 1,
  limit: number = 10,
  category?: string
): Promise<{ materials: Material[]; total: number }> => {
  try {
    const token = getAuthToken();
    const response = await axios.get(`${API_BASE_URL}/api/materials`, {
      params: { page, limit, category },
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch materials:', error);
    throw error;
  }
};

/**
 * 教材の詳細情報を取得する
 * @param id 教材ID
 */
export const getMaterialById = async (id: string): Promise<Material> => {
  try {
    const token = getAuthToken();
    const response = await axios.get(`${API_BASE_URL}/api/materials/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch material with id ${id}:`, error);
    throw error;
  }
};

/**
 * 教材をダウンロードする
 * @param id 教材ID
 */
export const downloadMaterial = async (id: string): Promise<Blob> => {
  try {
    const token = getAuthToken();
    const response = await axios.get(
      `${API_BASE_URL}/api/materials/download/${id}`,
      {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      }
    );
    return response.data;
  } catch (error) {
    console.error(`Failed to download material with id ${id}:`, error);
    throw error;
  }
};

/**
 * 教材の検索を行う
 * @param query 検索クエリ
 * @param page ページ番号
 * @param limit 1ページあたりの件数
 */
export const searchMaterials = async (
  query: string,
  page: number = 1,
  limit: number = 10
): Promise<{ materials: Material[]; total: number }> => {
  try {
    const token = getAuthToken();
    const response = await axios.get(`${API_BASE_URL}/api/materials/search`, {
      params: { query, page, limit },
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to search materials:', error);
    throw error;
  }
};

/**
 * 最近追加された教材を取得する
 * @param limit 取得する件数
 */
export const getRecentMaterials = async (
  limit: number = 5
): Promise<Material[]> => {
  try {
    const token = getAuthToken();
    const response = await axios.get(`${API_BASE_URL}/api/materials/recent`, {
      params: { limit },
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch recent materials:', error);
    throw error;
  }
};

// エラー型定義
export interface MaterialApiError {
  message: string;
  code: string;
  status: number;
}