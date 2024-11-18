'use client';

import { useEffect, useState } from 'react';
import { Box, Grid, Typography, Card, CardContent, CardMedia, Pagination } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import axios from 'axios';
import { MaterialDownload } from './MaterialDownload';
import { Loading } from '../Common/Loading';
import { Alert } from '../Common/Alert';

// 教材のインターフェース定義
interface Material {
  id: string;
  title: string;
  description: string;
  thumbnailUrl: string;
  type: 'pdf' | 'video' | 'audio';
  downloadUrl: string;
  createdAt: string;
  level: 'beginner' | 'intermediate' | 'advanced';
}

// ページネーションの設定
const ITEMS_PER_PAGE = 12;

export default function MaterialList() {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  // 教材データの取得
  useEffect(() => {
    const fetchMaterials = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/api/materials?page=${page}&limit=${ITEMS_PER_PAGE}`
        );
        setMaterials(response.data.materials);
        setTotalPages(Math.ceil(response.data.total / ITEMS_PER_PAGE));
      } catch (err) {
        setError('教材の読み込み中にエラーが発生しました。');
        console.error('Error fetching materials:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMaterials();
  }, [page]);

  // ページ変更ハンドラー
  const handlePageChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading) return <Loading />;
  if (error) return <Alert severity="error" message={error} />;

  return (
    <Box sx={{ padding: theme.spacing(3) }}>
      <Typography variant="h4" component="h1" gutterBottom>
        学習教材一覧
      </Typography>
      
      <Grid container spacing={3}>
        {materials.map((material) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={material.id}>
            <Card 
              sx={{ 
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: theme.shadows[4]
                }
              }}
            >
              <CardMedia
                component="img"
                height="140"
                image={material.thumbnailUrl}
                alt={material.title}
                sx={{ objectFit: 'cover' }}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h6" component="h2">
                  {material.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {material.description}
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  レベル: {material.level}
                </Typography>
              </CardContent>
              <MaterialDownload 
                materialId={material.id}
                downloadUrl={material.downloadUrl}
              />
            </Card>
          </Grid>
        ))}
      </Grid>

      {totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={handlePageChange}
            color="primary"
            size={isMobile ? 'small' : 'medium'}
          />
        </Box>
      )}
    </Box>
  );
}

// SEO最適化のためのメタデータ
export const metadata = {
  title: '学習教材一覧 | SpeakPro',
  description: '語学学習のための教材一覧です。PDF、動画、音声など様々な形式の教材をご利用いただけます。',
  keywords: '語学学習, 教材, オンライン学習, PDF, 動画教材, 音声教材',
};