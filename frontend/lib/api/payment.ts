import axios from 'axios';
import { loadStripe } from '@stripe/stripe-js';

// Stripeの公開キーを環境変数から取得
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY!);

// APIのベースURL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

// 支払い情報の型定義
export interface PaymentIntent {
  clientSecret: string;
  id: string;
  amount: number;
  status: string;
}

export interface PaymentHistory {
  id: string;
  date: string;
  amount: number;
  status: string;
  description: string;
}

/**
 * 決済インテントを作成する
 * @param amount 支払い金額（円）
 * @param description 支払いの説明
 */
export const createPaymentIntent = async (
  amount: number,
  description: string
): Promise<PaymentIntent> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/payments/create-intent`, {
      amount,
      description,
    });
    return response.data;
  } catch (error) {
    console.error('Payment intent creation failed:', error);
    throw error;
  }
};

/**
 * 決済を確定する
 * @param paymentIntentId 決済インテントID
 * @param paymentMethodId 支払い方法ID
 */
export const confirmPayment = async (
  paymentIntentId: string,
  paymentMethodId: string
): Promise<PaymentIntent> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/payments/confirm`, {
      paymentIntentId,
      paymentMethodId,
    });
    return response.data;
  } catch (error) {
    console.error('Payment confirmation failed:', error);
    throw error;
  }
};

/**
 * 支払い履歴を取得する
 * @param page ページ番号
 * @param limit 1ページあたりの件数
 */
export const getPaymentHistory = async (
  page: number = 1,
  limit: number = 10
): Promise<{
  items: PaymentHistory[];
  total: number;
}> => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/payments/history`,
      {
        params: { page, limit },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Failed to fetch payment history:', error);
    throw error;
  }
};

/**
 * Stripeの支払いフォームをマウントする要素を初期化する
 * @param clientSecret クライアントシークレット
 * @param options Stripeエレメントのオプション
 */
export const initializeStripeElement = async (
  clientSecret: string,
  options = {}
) => {
  const stripe = await stripePromise;
  if (!stripe) throw new Error('Failed to load Stripe');

  const elements = stripe.elements({
    clientSecret,
    ...options,
  });

  return {
    stripe,
    elements,
  };
};

/**
 * 支払いをキャンセルする
 * @param paymentIntentId 決済インテントID
 */
export const cancelPayment = async (
  paymentIntentId: string
): Promise<void> => {
  try {
    await axios.post(`${API_BASE_URL}/api/payments/cancel`, {
      paymentIntentId,
    });
  } catch (error) {
    console.error('Payment cancellation failed:', error);
    throw error;
  }
};

// エラーレスポンスの型定義
export interface PaymentError {
  code: string;
  message: string;
}

// 支払い状態の定数
export const PaymentStatus = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  SUCCEEDED: 'succeeded',
  FAILED: 'failed',
  CANCELED: 'canceled',
} as const;