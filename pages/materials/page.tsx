'use client';

import { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Card, CardContent, CardMedia, CircularProgress } from '@mui/material';
import { MaterialList } from '@/components/Materials/MaterialList';
import { MaterialDownload } from '@/components/Materials/MaterialDownload';
import { Alert } from '@/components/Common/Alert';
import { useAuth } from '@/hooks/useAuth';
import { fetchMaterials } from '@/services/materialService';

interface Material {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  type: 'pdf' | 'video' | 'audio';
  downloadUrl: string;
  createdAt: string;
}

export default function MaterialsPage() {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const loadMaterials = async () => {
      try {
        setLoading(true);
        const response = await fetchMaterials();
        setMaterials(response.data);
        setError(null);
      } catch (err) {
        setError('教材の読み込み中にエラーが発生しました。');
        console.error('Error loading materials:', err);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      loadMaterials();
    }
  }, [user]);

  if (!user) {
    return (
      <Container>
        <Typography variant="h6" color="error" sx={{ mt: 4 }}>
          このページにアクセスするにはログインが必要です。
        </Typography>
      </Container>
    );
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        教材一覧
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {materials.length > 0 ? (
          <MaterialList
            materials={materials}
            onDownload={(material) => (
              <MaterialDownload
                materialId={material.id}
                downloadUrl={material.downloadUrl}
                title={material.title}
              />
            )}
          />
        ) : (
          <Box width="100%" textAlign="center" py={4}>
            <Typography variant="body1" color="textSecondary">
              利用可能な教材がありません。
            </Typography>
          </Box>
        )}
      </Grid>
    </Container>
  );
}