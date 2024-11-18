'use client';

import { useEffect, useState } from 'react';
import { Box, Grid, Paper, Typography, Container } from '@mui/material';
import UserManagement from '@/components/Admin/UserManagement';
import LessonManagement from '@/components/Admin/LessonManagement';
import MaterialManagement from '@/components/Admin/MaterialManagement';
import Loading from '@/components/Common/Loading';
import Alert from '@/components/Common/Alert';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';

// ダッシュボードの統計情報の型定義
interface DashboardStats {
  totalUsers: number;
  totalLessons: number;
  totalMaterials: number;
  activeUsers: number;
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user, isAdmin } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // 管理者権限チェック
    if (!isAdmin) {
      router.push('/');
      return;
    }

    // 統計情報の取得
    const fetchDashboardStats = async () => {
      try {
        const response = await fetch('/api/admin/stats');
        if (!response.ok) throw new Error('Failed to fetch dashboard stats');
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError('Failed to load dashboard statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardStats();
  }, [isAdmin, router]);

  if (loading) return <Loading />;
  if (error) return <Alert severity="error" message={error} />;
  if (!stats) return null;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Admin Dashboard
      </Typography>

      {/* 統計情報カード */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography variant="h6">Total Users</Typography>
            <Typography variant="h4">{stats.totalUsers}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography variant="h6">Active Users</Typography>
            <Typography variant="h4">{stats.activeUsers}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography variant="h6">Total Lessons</Typography>
            <Typography variant="h4">{stats.totalLessons}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography variant="h6">Total Materials</Typography>
            <Typography variant="h4">{stats.totalMaterials}</Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* 管理セクション */}
      <Box sx={{ mt: 4 }}>
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <UserManagement />
          </Grid>
          <Grid item xs={12}>
            <LessonManagement />
          </Grid>
          <Grid item xs={12}>
            <MaterialManagement />
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}