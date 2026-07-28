import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { useAuth } from './contexts/AuthContext';

const Login = React.lazy(() => import('./pages/Auth/Login'));
const HospitalDashboard = React.lazy(() => import('./pages/Dashboard/HospitalDashboard'));
const PatientList = React.lazy(() => import('./pages/Patients/PatientList'));
const Calendar = React.lazy(() => import('./pages/Appointments/Calendar'));
const DiagnosisChat = React.lazy(() => import('./pages/AI/DiagnosisChat'));
const PharmacyDash = React.lazy(() => import('./pages/Pharmacy/PharmacyDash'));
const OrchestratorDashboard = React.lazy(() => import('./pages/Admin/OrchestratorDashboard'));

// Simple loading fallback
const LoadingFallback = () => (
  <div className="flex h-screen w-full items-center justify-center">
    <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"></div>
  </div>
);

function App() {
  const { isAuthenticated, user } = useAuth();

  return (
    <React.Suspense fallback={<LoadingFallback />}>
      <Routes>
        <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
        
        <Route path="/" element={<MainLayout />}>
          <Route index element={<HospitalDashboard />} />
          <Route path="patients" element={<PatientList />} />
          <Route path="appointments" element={<Calendar />} />
          <Route path="ai-diagnosis" element={<DiagnosisChat />} />
          <Route path="pharmacy" element={<PharmacyDash />} />
          
          {user?.role === 'Admin' && (
            <Route path="admin" element={<OrchestratorDashboard />} />
          )}
          
          {/* Catch-all */}
          <Route path="*" element={
            <div className="flex flex-col items-center justify-center h-full text-slate-500">
              <h1 className="text-4xl font-bold mb-4">404</h1>
              <p>Page under construction or not found.</p>
            </div>
          } />
        </Route>
      </Routes>
    </React.Suspense>
  );
}

export default App;
