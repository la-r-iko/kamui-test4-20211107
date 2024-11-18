import { useState, useCallback } from 'react';
import useSWR from 'swr';
import axios from 'axios';

// 教材の型定義
interface Material {
  id: string;
  title: string;
  description: string;
  fileUrl: string;
  fileType: string;
  createdAt: string;
  updatedAt: string;
  downloadCount: number;
}

// APIレスポンスの型定義
interface MaterialsResponse {
  materials: Material[];
  totalCount: number;
}

// フックのオプション型定義
interface UseMaterialsOptions {
  page?: number;
  limit?: number;
  searchQuery?: string;
  fileType?: string;
}

// カスタムフックの戻り値の型定義
interface UseMaterialsReturn {
  materials: Material[];
  isLoading: boolean;
  error: any;
  totalCount: number;
  downloadMaterial: (materialId: string) => Promise<string>;
  searchMaterials: (query: string) => void;
  refreshMaterials: () => void;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

/**
 * 教材関連のカスタムフック
 * @param options - 取得オプション（ページネーション、検索クエリなど）
 * @returns 教材データと操作関数
 */
export const useMaterials = (options: UseMaterialsOptions = {}): UseMaterialsReturn => {
  const { page = 1, limit = 10, searchQuery = '', fileType = '' } = options;
  const [search, setSearch] = useState(searchQuery);

  // APIエンドポイントの構築
  const apiUrl = `${API_URL}/api/materials?page=${page}&limit=${limit}&search=${search}&fileType=${fileType}`;

  // SWRを使用してデータフェッチ
  const { data, error, mutate } = useSWR<MaterialsResponse>(
    apiUrl,
    async (url) => {
      const response = await axios.get(url);
      return response.data;
    }
  );

  /**
   * 教材のダウンロード処理
   * @param materialId - ダウンロードする教材のID
   * @returns ダウンロードURL
   */
  const downloadMaterial = useCallback(async (materialId: string): Promise<string> => {
    try {
      const response = await axios.post(`${API_URL}/api/materials/download`, {
        materialId,
      });
      return response.data.downloadUrl;
    } catch (error) {
      console.error('Failed to download material:', error);
      throw error;
    }
  }, []);

  /**
   * 教材の検索処理
   * @param query - 検索クエリ
   */
  const searchMaterials = useCallback((query: string) => {
    setSearch(query);
  }, []);

  /**
   * 教材データの再取得
   */
  const refreshMaterials = useCallback(() => {
    mutate();
  }, [mutate]);

  return {
    materials: data?.materials || [],
    isLoading: !error && !data,
    error,
    totalCount: data?.totalCount || 0,
    downloadMaterial,
    searchMaterials,
    refreshMaterials,
  };
};

export default useMaterials;
// コンポーネント内での使用例
const MaterialList = () => {
  const { 
    materials, 
    isLoading, 
    error, 
    downloadMaterial,
    searchMaterials 
  } = useMaterials({
    page: 1,
    limit: 10,
    fileType: 'pdf'
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading materials</div>;

  return (
    <div>
      <input
        type="text"
        onChange={(e) => searchMaterials(e.target.value)}
        placeholder="Search materials..."
      />
      {materials.map((material) => (
        <div key={material.id}>
          <h3>{material.title}</h3>
          <button onClick={() => downloadMaterial(material.id)}>
            Download
          </button>
        </div>
      ))}
    </div>
  );
};