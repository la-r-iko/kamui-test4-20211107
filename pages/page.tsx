// frontend/app/page.tsx

import { Metadata } from 'next'
import { Suspense } from 'react'
import dynamic from 'next/dynamic'

// Client Components
const LessonCalendar = dynamic(() => import('@/components/Lesson/LessonCalendar'), {
  ssr: false,
  loading: () => <Loading />
})
const MaterialList = dynamic(() => import('@/components/Materials/MaterialList'), {
  loading: () => <Loading />
})

// Server Components
import Loading from '@/components/Common/Loading'
import Alert from '@/components/Common/Alert'
import { Button } from '@/components/Common/Button'

// メタデータの設定
export const metadata: Metadata = {
  title: 'SpeakPro - オンライン英会話レッスン',
  description: 'プロフェッショナルな講師陣による、高品質なオンライン英会話レッスンを提供します。',
  keywords: 'オンライン英会話, 英語学習, 語学学習, スピーキング',
  openGraph: {
    title: 'SpeakPro - オンライン英会話レッスン',
    description: 'プロフェッショナルな講師陣による、高品質なオンライン英会話レッスンを提供します。',
    images: ['/images/og-image.jpg'],
  },
}

// メインページコンポーネント
export default async function HomePage() {
  return (
    <main className="min-h-screen">
      {/* ヒーローセクション */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20 px-4 md:px-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            英語学習の新しいスタンダード
          </h1>
          <p className="text-xl md:text-2xl mb-8">
            プロフェッショナルな講師陣と共に、あなたの英語力を次のレベルへ
          </p>
          <Button
            href="/auth/signup"
            variant="contained"
            size="large"
            className="bg-white text-blue-800 hover:bg-blue-50"
          >
            無料で始める
          </Button>
        </div>
      </section>

      {/* レッスンカレンダーセクション */}
      <section className="py-16 px-4 md:px-8 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold mb-8 text-center">
            今週のレッスンスケジュール
          </h2>
          <Suspense fallback={<Loading />}>
            <LessonCalendar />
          </Suspense>
        </div>
      </section>

      {/* 教材セクション */}
      <section className="py-16 px-4 md:px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold mb-8 text-center">
            充実の学習教材
          </h2>
          <Suspense fallback={<Loading />}>
            <MaterialList limit={6} />
          </Suspense>
        </div>
      </section>

      {/* 特徴セクション */}
      <section className="py-16 px-4 md:px-8 bg-gray-50">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center p-6">
            <h3 className="text-xl font-bold mb-4">プロフェッショナルな講師陣</h3>
            <p>厳選された経験豊富な講師による質の高いレッスン</p>
          </div>
          <div className="text-center p-6">
            <h3 className="text-xl font-bold mb-4">柔軟なスケジュール</h3>
            <p>24時間いつでも予約可能な便利なシステム</p>
          </div>
          <div className="text-center p-6">
            <h3 className="text-xl font-bold mb-4">豊富な教材</h3>
            <p>レベルに合わせた教材で効率的な学習をサポート</p>
          </div>
        </div>
      </section>

      {/* CTA セクション */}
      <section className="bg-blue-900 text-white py-16 px-4 md:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">
            今すぐ英語学習を始めましょう
          </h2>
          <Button
            href="/auth/signup"
            variant="contained"
            size="large"
            className="bg-white text-blue-900 hover:bg-blue-50"
          >
            無料トライアルに申し込む
          </Button>
        </div>
      </section>
    </main>
  )
}