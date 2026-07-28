import axios from 'axios';

// Create base instance for REST API calls
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add interceptor for auth tokens
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      // Clear token and redirect to login if unauthorized
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Dedicated service for standard CRUD REST operations
export const PatientService = {
  getAll: async () => {
    const { data } = await api.get('/patients/');
    return data;
  },
  getById: async (id: string) => {
    const { data } = await api.get(`/patients/${id}`);
    return data;
  }
};

export const DoctorService = {
  getAll: async () => {
    const { data } = await api.get('/doctors/');
    return data;
  }
};

export const AppointmentService = {
  getAll: async () => {
    const { data } = await api.get('/appointments/');
    return data;
  }
};

export const TreatmentService = {
  getAll: async () => { const { data } = await api.get('/treatments/'); return data; }
};

export const LabsService = {
  getAll: async () => { const { data } = await api.get('/labs/'); return data; }
};

export const BillingService = {
  getAll: async () => { const { data } = await api.get('/billing/'); return data; }
};

export const InsuranceService = {
  getAll: async () => { const { data } = await api.get('/insurance/'); return data; }
};

export const NotificationsService = {
  getAll: async () => { const { data } = await api.get('/notifications/'); return data; }
};

export const AnalyticsService = {
  getAll: async () => { const { data } = await api.get('/analytics/'); return data; }
};

export const SettingsService = {
  getAll: async () => { const { data } = await api.get('/settings/'); return data; }
};

export const AdminService = {
  getAll: async () => { const { data } = await api.get('/admin/'); return data; }
};

// Dedicated service for Workflow Orchestrator API (Multi-agent AI tasks)
export const OrchestratorService = {
  startWorkflow: async (workflowId: string, payload: any) => {
    const { data } = await api.post('/workflow/start', {
      workflow_id: workflowId,
      payload
    });
    return data;
  },
  resumeWorkflow: async (workflowId: string, approved: boolean, payload: any) => {
    const { data } = await api.post('/workflow/resume', {
      workflow_id: workflowId,
      approved,
      payload
    });
    return data;
  }
};

export const AuthService = {
  login: async (credentials: { email: string; password: string }) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    
    const { data } = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return data; // { access_token: string, token_type: string }
  },
  register: async (userData: any) => {
    const { data } = await api.post('/auth/register', userData);
    return data;
  },
  getCurrentUser: async () => {
    const { data } = await api.get('/auth/me');
    return data; // User object from backend
  }
};
