import axios from 'axios';
import { getAuthToken } from '../utils/auth';

// APIのベースURL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

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

// レッスンAPI関連の関数をまとめたオブジェクト
export const lessonsApi = {
  // レッスン一覧を取得
  async getLessons(): Promise<Lesson[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/lessons`, {
        headers: {
          Authorization: `Bearer ${getAuthToken()}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch lessons:', error);
      throw error;
    }
  },

  // 特定のレッスンの詳細を取得
  async getLessonById(lessonId: string): Promise<Lesson> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/lessons/${lessonId}`, {
        headers: {
          Authorization: `Bearer ${getAuthToken()}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch lesson ${lessonId}:`, error);
      throw error;
    }
  },

  // レッスンを予約
  async bookLesson(params: BookLessonParams): Promise<Lesson> {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/lessons/book`,
        params,
        {
          headers: {
            Authorization: `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Failed to book lesson:', error);
      throw error;
    }
  },

  // レッスンの予定を変更
  async rescheduleLesson(
    lessonId: string,
    newStartTime: string,
    newEndTime: string
  ): Promise<Lesson> {
    try {
      const response = await axios.put(
        `${API_BASE_URL}/api/lessons/reschedule`,
        {
          lessonId,
          startTime: newStartTime,
          endTime: newEndTime,
        },
        {
          headers: {
            Authorization: `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Failed to reschedule lesson:', error);
      throw error;
    }
  },

  // レッスンをキャンセル
  async cancelLesson(lessonId: string): Promise<void> {
    try {
      await axios.delete(`${API_BASE_URL}/api/lessons/cancel`, {
        data: { lessonId },
        headers: {
          Authorization: `Bearer ${getAuthToken()}`,
          'Content-Type': 'application/json',
        },
      });
    } catch (error) {
      console.error('Failed to cancel lesson:', error);
      throw error;
    }
  },

  // 特定の期間のレッスンを取得
  async getLessonsByDateRange(startDate: string, endDate: string): Promise<Lesson[]> {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/lessons/schedule`,
        {
          params: { startDate, endDate },
          headers: {
            Authorization: `Bearer ${getAuthToken()}`,
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Failed to fetch lessons by date range:', error);
      throw error;
    }
  },
};

export default lessonsApi;
// 使用例
import { lessonsApi } from '../lib/api/lessons';

// レッスン一覧を取得
const lessons = await lessonsApi.getLessons();

// レッスンを予約
const newLesson = await lessonsApi.bookLesson({
  teacherId: "teacher123",
  startTime: "2023-12-01T10:00:00Z",
  endTime: "2023-12-01T11:00:00Z"
});