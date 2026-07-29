import React, { useEffect, useState } from 'react';

interface WorkflowEvent {
  agent: string;
  workflow_state: string;
  confidence: number;
  risk_level: string;
  requires_human_review: boolean;
}

const OrchestratorDashboard = () => {
  const [events, setEvents] = useState<WorkflowEvent[]>([]);
  const [wsStatus, setWsStatus] = useState('Connecting...');

  useEffect(() => {
    // Backend WebSocket: /api/v1/ws/{workflow_id}
    const wsBase = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000')
      .replace('http://', 'ws://')
      .replace('https://', 'wss://')
      .replace('/api/v1', '');
    const ws = new WebSocket(`${wsBase}/api/v1/ws/global`);

    ws.onopen  = () => setWsStatus('Live');
    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        setEvents(prev => [data, ...prev].slice(0, 10));
      } catch { /* ignore non-JSON pings */ }
    };
    ws.onclose = () => setWsStatus('Disconnected');
    return () => ws.close();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <header className="mb-10 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
            Hospital AI Orchestrator
          </h1>
          <p className="text-slate-400 mt-2">Enterprise Multi-Agent Coordination Platform</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 rounded-full">
          <div className={`w-2 h-2 rounded-full ${wsStatus === 'Live' ? 'bg-emerald-400 animate-pulse' : 'bg-red-500'}`} />
          <span className="text-sm font-mono text-slate-300">{wsStatus}</span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        {['Active Workflows', 'Agents Online', 'Avg Response Time', 'API Cost (MTD)'].map((metric, i) => (
          <div key={metric} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl shadow-blue-900/10">
            <h3 className="text-slate-400 text-sm font-medium">{metric}</h3>
            <p className="text-3xl font-bold mt-2 text-slate-100">{['24', '9', '1.2s', '$0.00'][i]}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <span className="text-emerald-400">⚡</span> Registered Agents
          </h2>
          <div className="space-y-2">
            {['intake_agent','diagnosis_agent','treatment_agent','emergency_agent',
              'lab_agent','pharmacy_agent','billing_agent','appointment_agent','insurance_agent'
            ].map(name => (
              <div key={name} className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-xl">
                <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-sm font-mono text-slate-300">{name}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-xl font-semibold mb-6">Live Workflow Timeline</h2>
          <div className="space-y-4">
            {events.length === 0 ? (
              <p className="text-slate-500 text-sm">Waiting for orchestrator events via WebSocket...</p>
            ) : events.map((ev, idx) => (
              <div key={idx} className="flex gap-4 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                <div className="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold flex-shrink-0">
                  {ev.agent.substring(0, 2).toUpperCase()}
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-medium text-slate-200">{ev.agent}</h4>
                      <p className="text-xs text-slate-400 mt-1">State: <span className="text-blue-400">{ev.workflow_state}</span></p>
                    </div>
                    <span className={`text-xs font-mono px-2 py-1 rounded ${ev.requires_human_review ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                      Risk: {ev.risk_level}
                    </span>
                  </div>
                  <div className="mt-3 flex items-center gap-2">
                    <div className="text-xs text-slate-400">Confidence</div>
                    <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-blue-500 to-emerald-400" style={{ width: `${(ev.confidence || 0) * 100}%` }} />
                    </div>
                    <div className="text-xs font-mono text-slate-300">{((ev.confidence || 0) * 100).toFixed(0)}%</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrchestratorDashboard;
