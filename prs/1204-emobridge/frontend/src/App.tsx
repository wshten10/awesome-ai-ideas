import React, { useState, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout, ConfigProvider, notification } from 'antd'
import { useAuth } from './hooks/useAuth'
import { useTheme } from './hooks/useTheme'
import { useWebSocket } from './hooks/useWebSocket'
import { Header } from './components/Header'
import { Sidebar } from './components/Sidebar'
import { LoadingSpinner } from './components/common/LoadingSpinner'

// 页面组件
const Dashboard = React.lazy(() => import('./pages/Dashboard'))
const EmotionRecognition = React.lazy(() => import('./pages/EmotionRecognition'))
const DigitalTwin = React.lazy(() => import('./pages/DigitalTwin'))
const TherapyEnvironment = React.lazy(() => import('./pages/TherapyEnvironment'))
const PatientManagement = React.lazy(() => import('./pages/PatientManagement'))
const Analytics = React.lazy(() => import('./pages/Analytics'))
const Settings = React.lazy(() => import('./pages/Settings'))
const Login = React.lazy(() => import('./pages/Login'))

const App: React.FC = () => {
  const { user, loading: authLoading } = useAuth()
  const { isDark, toggleTheme } = useTheme()
  const { connectionStatus } = useWebSocket()
  
  // 系统通知
  useEffect(() => {
    if (connectionStatus === 'disconnected') {
      notification.warning({
        message: '连接状态',
        description: '与后端服务连接已断开，部分功能可能无法正常使用',
        duration: 0,
      })
    } else if (connectionStatus === 'connected') {
      notification.success({
        message: '连接状态',
        description: '后端服务连接正常',
        duration: 3,
      })
    }
  }, [connectionStatus])

  // 主题配置
  const themeConfig = {
    token: {
      colorPrimary: '#1890ff',
      borderRadius: 6,
      fontFamily: 'Inter, sans-serif',
    },
    algorithm: isDark ? 'dark' : undefined,
  }

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="text-center">
          <LoadingSpinner size="large" />
          <p className="mt-4 text-gray-600">正在初始化系统...</p>
        </div>
      </div>
    )
  }

  return (
    <ConfigProvider theme={themeConfig}>
      <Layout className={`min-h-screen ${isDark ? 'dark' : ''}`}>
        <Header 
          onThemeToggle={toggleTheme}
          user={user}
        />
        
        <Layout>
          <Sidebar user={user} />
          
          <Layout.Content className="p-6 bg-gray-50 dark:bg-gray-900">
            <React.Suspense 
              fallback={
                <div className="flex items-center justify-center h-64">
                  <div className="text-center">
                    <LoadingSpinner />
                    <p className="mt-4 text-gray-600">正在加载页面...</p>
                  </div>
                </div>
              }
            >
              <Routes>
                {/* 公开路由 */}
                <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
                
                {/* 需要认证的路由 */}
                {user ? (
                  <>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/emotion-recognition" element={<EmotionRecognition />} />
                    <Route path="/digital-twin" element={<DigitalTwin />} />
                    <Route path="/therapy-environment" element={<TherapyEnvironment />} />
                    <Route path="/patients" element={<PatientManagement />} />
                    <Route path="/analytics" element={<Analytics />} />
                    <Route path="/settings" element={<Settings />} />
                    <Route path="*" element={<Navigate to="/" />} />
                  </>
                ) : (
                  <Route path="*" element={<Navigate to="/login" />} />
                )}
              </Routes>
            </React.Suspense>
          </Layout.Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  )
}

export default App