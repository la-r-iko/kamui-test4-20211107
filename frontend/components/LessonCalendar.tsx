'use client';

import React, { useState, useCallback } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import { ja } from 'date-fns/locale';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { useTheme } from '@mui/material/styles';
import {
  Box,
  Typography,
  Paper,
  useMediaQuery,
  CircularProgress,
  Alert,
} from '@mui/material';
import useSWR from 'swr';

// カレンダーのローカライゼーション設定
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

// データフェッチャー関数
const fetcher = (url: string) => 
  fetch(url, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  }).then(res => res.json());

const LessonCalendar: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [selectedEvent, setSelectedEvent] = useState<LessonEvent | null>(null);

  // レッスンデータの取得
  const { data: lessons, error, isLoading } = useSWR<LessonEvent[]>(
    `${process.env.NEXT_PUBLIC_API_URL}/api/lessons`,
    fetcher
  );

  // イベントクリックハンドラー
  const handleEventSelect = useCallback((event: LessonEvent) => {
    setSelectedEvent(event);
  }, []);

  // カレンダーのカスタムスタイル
  const calendarStyle = {
    height: isMobile ? '500px' : '700px',
    padding: theme.spacing(2),
  };

  // イベントのカスタムスタイル
  const eventStyleGetter = (event: LessonEvent) => {
    let backgroundColor = theme.palette.primary.main;
    
    switch (event.status) {
      case 'completed':
        backgroundColor = theme.palette.success.main;
        break;
      case 'cancelled':
        backgroundColor = theme.palette.error.main;
        break;
    }

    return {
      style: {
        backgroundColor,
        borderRadius: '4px',
        opacity: 0.8,
        color: 'white',
        border: 'none',
        display: 'block',
      },
    };
  };

  if (error) {
    return (
      <Alert severity="error">
        レッスンデータの取得に失敗しました。
      </Alert>
    );
  }

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="500px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper elevation={3}>
      <Box p={2}>
        <Typography variant="h5" gutterBottom>
          レッスンスケジュール
        </Typography>
        <Calendar
          localizer={localizer}
          events={lessons || []}
          startAccessor="start"
          endAccessor="end"
          style={calendarStyle}
          eventPropGetter={eventStyleGetter}
          onSelectEvent={handleEventSelect}
          views={['month', 'week', 'day']}
          defaultView={isMobile ? 'day' : 'month'}
          tooltipAccessor={(event: LessonEvent) => event.title}
          messages={{
            next: '次へ',
            previous: '前へ',
            today: '今日',
            month: '月',
            week: '週',
            day: '日',
          }}
        />
      </Box>
      
      {selectedEvent && (
        <Box p={2} borderTop={1} borderColor="divider">
          <Typography variant="h6">
            {selectedEvent.title}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            開始: {format(new Date(selectedEvent.start), 'yyyy/MM/dd HH:mm')}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            終了: {format(new Date(selectedEvent.end), 'yyyy/MM/dd HH:mm')}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            ステータス: {selectedEvent.status}
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default LessonCalendar;