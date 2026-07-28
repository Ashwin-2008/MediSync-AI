import axios from 'axios';

// Create base instance for REST API calls
export const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
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

// Dedicated service for standard CRUD REST operations
export const PatientService = {
  getAll: async () => {
    // Fallback/Mock behavior if backend doesn't have this yet, but we structure it properly
    try {
      const { data } = await api.get('/patients');
      return data;
    } catch (error) {
      console.warn("Using mock patient data because backend endpoint might not exist yet.");
      return [
        { id: 'PT-10492', name: 'Sarah Jenkins', status: 'Triage Complete', department: 'Cardiology', date: '2026-07-28' },
        { id: 'PT-10493', name: 'Michael Chen', status: 'Pending Lab', department: 'Emergency', date: '2026-07-28' },
      ];
    }
  },
  getById: async (id: string) => {
    const { data } = await api.get(`/patients/${id}`);
    return data;
  }
};

export const DoctorService = {
  getAll: async () => {
    try {
      const { data } = await api.get('/doctors');
      return data;
    } catch (error) {
      return [
        { id: 'DR-001', name: 'Dr. Emily Carter', specialty: 'Cardiology', status: 'Available' },
        { id: 'DR-002', name: 'Dr. James Smith', specialty: 'Neurology', status: 'In Surgery' }
      ];
    }
  }
};

export const AppointmentService = {
  getAll: async () => {
    try {
      const { data } = await api.get('/appointments');
      return data;
    } catch (error) {
      return [
        { id: 'APT-912', patientName: 'Sarah Jenkins', doctorName: 'Dr. Emily Carter', time: '10:00 AM', status: 'Confirmed' }
      ];
    }
  }
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
