import useSWR from 'swr';
import axios from 'axios';
import { useState } from 'react';

// レッスンの型定義
export interface Lesson {
  id: string;
  title: string;
  startTime: string;
  endTime: string;
  teacherId: string;
  studentId: string;
  status: 'scheduled' | 'completed' | 'cancelled';
  zoomLink?: string;
  materials?: string[];
}

// レッスン予約のパラメータ型
export interface BookLessonParams {
  teacherId: string;
  startTime: string;
  endTime: string;
}

// APIのベースURL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

/**
 * レッスン関連の操作を提供するカスタムフック
 */
export const useLessons = () => {
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // レッスン一覧を取得
  const { data: lessons, mutate } = useSWR<Lesson[]>(
    `${API_BASE_URL}/api/lessons`,
    async (url) => {
      const response = await axios.get(url);
      return response.data;
    }
  );

  // 特定のレッスンを取得
  const getLesson = async (lessonId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/lessons/${lessonId}`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      throw err;
    }
  };

  // レッスンを予約
  const bookLesson = async (params: BookLessonParams) => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/lessons/book`, params);
      await mutate(); // レッスン一覧を再取得
      return response.data;
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // レッスンをキャンセル
  const cancelLesson = async (lessonId: string) => {
    setIsLoading(true);
    try {
      await axios.delete(`${API_BASE_URL}/api/lessons/cancel/${lessonId}`);
      await mutate(); // レッスン一覧を再取得
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // レッスンを再スケジュール
  const rescheduleLesson = async (lessonId: string, newStartTime: string, newEndTime: string) => {
    setIsLoading(true);
    try {
      const response = await axios.put(`${API_BASE_URL}/api/lessons/reschedule/${lessonId}`, {
        startTime: newStartTime,
        endTime: newEndTime,
      });
      await mutate(); // レッスン一覧を再取得
      return response.data;
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // 指定期間のレッスンを取得
  const getLessonsByDateRange = async (startDate: string, endDate: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/lessons/range`, {
        params: { startDate, endDate },
      });
      return response.data;
    } catch (err) {
      setError(err as Error);
      throw err;
    }
  };

  return {
    lessons,
    error,
    isLoading,
    getLesson,
    bookLesson,
    cancelLesson,
    rescheduleLesson,
    getLessonsByDateRange,
    refreshLessons: mutate,
  };
};

export default useLessons;