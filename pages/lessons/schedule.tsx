'use client';

import React, { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import { ja } from 'date-fns/locale';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import { Box, Typography, Paper, CircularProgress } from '@mui/material';
import Alert from '@/components/Common/Alert';

// カレンダーのローカライズ設定
const locales = {
  ja: ja,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

// レッスンイベントの型定義
interface LessonEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  teacherId: string;
  studentId: string;
  status: 'scheduled' | 'completed' | 'cancelled';
}

export default function Schedule() {
  const router = useRouter();
  const [events, setEvents] = useState<LessonEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // レッスンデータの取得
  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const response = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/api/lessons`
        );
        
        // APIレスポンスをカレンダーイベント形式に変換
        const formattedEvents = response.data.map((lesson: any) => ({
          id: lesson.id,
          title: lesson.title,
          start: new Date(lesson.startTime),
          end: new Date(lesson.endTime),
          teacherId: lesson.teacherId,
          studentId: lesson.studentId,
          status: lesson.status,
        }));
        
        setEvents(formattedEvents);
        setLoading(false);
      } catch (err) {
        setError('レッスンデータの取得に失敗しました。');
        setLoading(false);
      }
    };

    fetchLessons();
  }, []);

  // イベントクリック時のハンドラー
  const handleEventClick = (event: LessonEvent) => {
    router.push(`/lessons/${event.id}`);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 3, height: '80vh' }}>
      <Typography variant="h4" component="h1" gutterBottom>
        レッスンスケジュール
      </Typography>

      {error && <Alert severity="error" message={error} />}

      <Box height="90%">
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          onSelectEvent={handleEventClick}
          views={['month', 'week', 'day']}
          defaultView="week"
          messages={{
            next: '次へ',
            previous: '前へ',
            today: '今日',
            month: '月',
            week: '週',
            day: '日',
          }}
          eventPropGetter={(event) => ({
            style: {
              backgroundColor: event.status === 'completed' ? '#4caf50' :
                            event.status === 'cancelled' ? '#f44336' : '#2196f3',
            },
          })}
        />
      </Box>
    </Paper>
  );
}