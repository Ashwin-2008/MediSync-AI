import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { useAuth } from './contexts/AuthContext';

const Login = React.lazy(() => import('./pages/Auth/Login'));
const Register = React.lazy(() => import('./pages/Auth/Register'));
const HospitalDashboard = React.lazy(() => import('./pages/Dashboard/HospitalDashboard'));
const PatientList = React.lazy(() => import('./pages/Patients/PatientList'));
const DoctorList = React.lazy(() => import('./pages/Doctors/DoctorList'));
const Calendar = React.lazy(() => import('./pages/Appointments/Calendar'));
const DiagnosisChat = React.lazy(() => import('./pages/AI/DiagnosisChat'));
const PharmacyDash = React.lazy(() => import('./pages/Pharmacy/PharmacyDash'));
const OrchestratorDashboard = React.lazy(() => import('./pages/Admin/OrchestratorDashboard'));

const BillingList = React.lazy(() => import('./pages/Billing/BillingList'));
const LabsList = React.lazy(() => import('./pages/Labs/LabsList'));
const TreatmentsList = React.lazy(() => import('./pages/Treatments/TreatmentsList'));
const InsuranceList = React.lazy(() => import('./pages/Insurance/InsuranceList'));
const NotificationsList = React.lazy(() => import('./pages/Notifications/NotificationsList'));
const Analytics = React.lazy(() => import('./pages/Analytics/Analytics'));
const Settings = React.lazy(() => import('./pages/Settings/Settings'));

// Simple loading fallback
const LoadingFallback = () => (
  <div className="flex h-screen w-full items-center justify-center">
    <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
  </div>
);

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <React.Suspense fallback={<LoadingFallback />}>
      <Routes>
        <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
        <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/" />} />
        
        <Route path="/" element={<MainLayout />}>
          <Route element={<ProtectedRoute allowedRoles={['Admin', 'Doctor', 'Nurse', 'Receptionist']} />}>
            <Route index element={<HospitalDashboard />} />
            <Route path="patients" element={<PatientList />} />
            <Route path="treatments" element={<TreatmentsList />} />
            <Route path="labs" element={<LabsList />} />
            <Route path="notifications" element={<NotificationsList />} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={['Admin', 'Receptionist']} />}>
            <Route path="doctors" element={<DoctorList />} />
            <Route path="billing" element={<BillingList />} />
            <Route path="insurance" element={<InsuranceList />} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={['Admin', 'Doctor', 'Receptionist']} />}>
            <Route path="appointments" element={<Calendar />} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={['Admin', 'Doctor']} />}>
            <Route path="ai-diagnosis" element={<DiagnosisChat />} />
            <Route path="pharmacy" element={<PharmacyDash />} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={['Admin']} />}>
            <Route path="admin/*" element={<OrchestratorDashboard />} />
            <Route path="analytics" element={<Analytics />} />
            <Route path="settings" element={<Settings />} />
          </Route>
          
          {/* Catch-all */}
          <Route path="*" element={
            <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
              <h1 className="text-4xl font-bold mb-4 text-foreground">404</h1>
              <p>Page under construction or not found.</p>
            </div>
          } />
        </Route>
      </Routes>
    </React.Suspense>
  );
}

export default App;
