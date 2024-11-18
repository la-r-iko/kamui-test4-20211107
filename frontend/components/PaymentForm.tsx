'use client';

import React, { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import {
  Box,
  TextField,
  Button,
  Typography,
  Card,
  CardContent,
  Grid,
  Alert,
  CircularProgress
} from '@mui/material';
import { styled } from '@mui/material/styles';
import axios from 'axios';

// Stripe の初期化
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY!);

// スタイル付きコンポーネント
const StyledCard = styled(Card)(({ theme }) => ({
  maxWidth: 600,
  margin: '0 auto',
  padding: theme.spacing(3),
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
  },
}));

interface PaymentFormProps {
  amount: number;
  lessonId?: string;
  onSuccess?: (paymentIntentId: string) => void;
  onError?: (error: Error) => void;
}

const PaymentForm: React.FC<PaymentFormProps> = ({
  amount,
  lessonId,
  onSuccess,
  onError,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cardDetails, setCardDetails] = useState({
    number: '',
    expiry: '',
    cvc: '',
    name: '',
  });

  // カード情報の検証
  const validateCard = (): boolean => {
    if (!cardDetails.number || cardDetails.number.length < 16) return false;
    if (!cardDetails.expiry || cardDetails.expiry.length < 5) return false;
    if (!cardDetails.cvc || cardDetails.cvc.length < 3) return false;
    if (!cardDetails.name) return false;
    return true;
  };

  // 支払い処理の実行
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateCard()) {
      setError('Please fill in all card details correctly');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 支払いインテントの作成
      const { data: { clientSecret } } = await axios.post('/api/payments/create-intent', {
        amount,
        lessonId,
      });

      const stripe = await stripePromise;
      if (!stripe) throw new Error('Stripe failed to initialize');

      // 支払いの確認
      const { error: stripeError, paymentIntent } = await stripe.confirmCardPayment(
        clientSecret,
        {
          payment_method: {
            card: {
              number: cardDetails.number,
              exp_month: parseInt(cardDetails.expiry.split('/')[0]),
              exp_year: parseInt(cardDetails.expiry.split('/')[1]),
              cvc: cardDetails.cvc,
            },
            billing_details: {
              name: cardDetails.name,
            },
          },
        }
      );

      if (stripeError) {
        throw new Error(stripeError.message);
      }

      if (paymentIntent?.status === 'succeeded') {
        onSuccess?.(paymentIntent.id);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Payment failed';
      setError(errorMessage);
      onError?.(err as Error);
    } finally {
      setLoading(false);
    }
  };

  // カード情報の入力ハンドラー
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCardDetails(prev => ({ ...prev, [name]: value }));
  };

  return (
    <StyledCard>
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
          Payment Details
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Card Number"
                name="number"
                value={cardDetails.number}
                onChange={handleChange}
                inputProps={{ maxLength: 16 }}
                required
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Expiry (MM/YY)"
                name="expiry"
                value={cardDetails.expiry}
                onChange={handleChange}
                inputProps={{ maxLength: 5 }}
                required
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="CVC"
                name="cvc"
                value={cardDetails.cvc}
                onChange={handleChange}
                inputProps={{ maxLength: 4 }}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Cardholder Name"
                name="name"
                value={cardDetails.name}
                onChange={handleChange}
                required
              />
            </Grid>
            {error && (
              <Grid item xs={12}>
                <Alert severity="error">{error}</Alert>
              </Grid>
            )}
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                disabled={loading}
              >
                {loading ? (
                  <CircularProgress size={24} />
                ) : (
                  `Pay ${new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD'
                  }).format(amount / 100)}`
                )}
              </Button>
            </Grid>
          </Grid>
        </form>
      </CardContent>
    </StyledCard>
  );
};

export default PaymentForm;