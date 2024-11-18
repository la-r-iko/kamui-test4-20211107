'use client';

import { useState, useEffect } from 'react';
import { Container, Typography, Box, Paper, Grid } from '@mui/material';
import LessonCalendar from '@/components/Lesson/LessonCalendar';
import LessonList from '@/components/Lesson/LessonList';
import Loading from '@/components/Common/Loading';
import Alert from '@/components/Common/Alert';
import { useAuth } from '@/hooks/useAuth';
import { fetchLessons } from '@/services/lessonService';
import { Lesson } from '@/types/lesson';

export default function LessonsPage() {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const loadLessons = async () => {
      try {
        if (!user) return;
        setLoading(true);
        const data = await fetchLessons();
        setLessons(data);
      } catch (err) {
        setError('レッスン情報の取得に失敗しました。');
        console.error('Failed to fetch lessons:', err);
      } finally {
        setLoading(false);
      }
    };

    loadLessons();
  }, [user]);

  if (!user) {
    return (
      <Container maxWidth="lg">
        <Typography variant="h5" align="center" sx={{ mt: 4 }}>
          レッスンの予約にはログインが必要です
        </Typography>
      </Container>
    );
  }

  if (loading) {
    return <Loading />;
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {error && (
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
      <Typography variant="h4" component="h1" gutterBottom>
        レッスン予約
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ p: 2, mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              レッスンカレンダー
            </Typography>
            <LessonCalendar lessons={lessons} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              予約済みレッスン
            </Typography>
            <LessonList 
              lessons={lessons.filter(lesson => lesson.status === 'booked')} 
              onStatusChange={(lessonId, newStatus) => {
                // レッスンステータス更新のロジックを実装
                setLessons(prevLessons =>
                  prevLessons.map(lesson =>
                    lesson.id === lessonId 
                      ? { ...lesson, status: newStatus }
                      : lesson
                  )
                );
              }}
            />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}