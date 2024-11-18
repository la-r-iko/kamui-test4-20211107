// app/layout.tsx
import { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { AuthProvider } from '@/contexts/AuthContext'
import Layout from '@/components/Layout'
import '@/styles/globals.css'

// フォントの設定
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

// メタデータの設定
export const metadata: Metadata = {
  title: {
    default: 'SpeakPro - Online Language Learning Platform',
    template: '%s | SpeakPro',
  },
  description: 'Professional language learning platform with native speakers',
  keywords: [
    'language learning',
    'online lessons',
    'language tutoring',
    'professional development',
  ],
  authors: [{ name: 'SpeakPro Team' }],
  creator: 'SpeakPro',
  metadataBase: new URL(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000'),
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: '/',
    title: 'SpeakPro - Online Language Learning Platform',
    description: 'Professional language learning platform with native speakers',
    siteName: 'SpeakPro',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SpeakPro',
    description: 'Professional language learning platform with native speakers',
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
  },
  robots: {
    index: true,
    follow: true,
  },
}

// レイアウトの型定義
interface RootLayoutProps {
  children: React.ReactNode
}

// ルートレイアウトコンポーネント
export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen bg-gray-50">
        <AuthProvider>
          <Layout>
            {/* アプリケーションの主要コンテンツ */}
            <main className="flex-1">
              {children}
            </main>
          </Layout>
        </AuthProvider>

        {/* サードパーティスクリプトの遅延読み込み */}
        <script
          defer
          src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
        />
        <script
          defer
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
            `,
          }}
        />
      </body>
    </html>
  )
}

// フォントやスクリプトの最適化設定
export const fontOptimization = {
  optimizeFonts: true,
  preload: true,
}

// キャッシュ設定
export const revalidate = 3600 // 1時間

// 動的メタデータの生成
export async function generateMetadata({ params }: { params: any }) {
  return {
    alternates: {
      canonical: '/',
      languages: {
        'en-US': '/en-US',
        'ja-JP': '/ja-JP',
      },
    },
  }
}