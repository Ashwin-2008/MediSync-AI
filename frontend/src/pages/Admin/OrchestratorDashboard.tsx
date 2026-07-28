import React, { useEffect, useState } from 'react';

// Mock types based on AgentOutput
interface WorkflowEvent {
  agent: string;
  workflow_state: string;
  confidence: number;
  risk_level: string;
  requires_human_review: boolean;
  next_agent: string;
}

const Dashboard = () => {
  const [events, setEvents] = useState<WorkflowEvent[]>([]);
  const [wsStatus, setWsStatus] = useState('Connecting...');

  useEffect(() => {
    // In production, connect to VITE_API_URL /ws/workflow
    const ws = new WebSocket('ws://localhost:8000/ws/workflow');
    
    ws.onopen = () => setWsStatus('Live');
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setEvents(prev => [data, ...prev].slice(0, 10)); // Keep last 10
      } catch (e) {
        console.error('Invalid WS message');
      }
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
          <div className={`w-2 h-2 rounded-full ${wsStatus === 'Live' ? 'bg-emerald-400 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="text-sm font-mono text-slate-300">{wsStatus}</span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        {['Active Workflows', 'Agents Online', 'Avg Response Time', 'API Cost (MTD)'].map((metric, i) => (
          <div key={metric} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl shadow-blue-900/10">
            <h3 className="text-slate-400 text-sm font-medium">{metric}</h3>
            <p className="text-3xl font-bold mt-2 text-slate-100">{[24, 13, '1.2s', '$1,245.80'][i]}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Token Usage & Cost Panel */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <span className="text-emerald-400">⚡</span> Resource Usage
          </h2>
          <div className="space-y-4">
            <div className="p-4 bg-slate-800/50 rounded-xl">
              <div className="text-xs text-slate-400 mb-1">Total Tokens Processed</div>
              <div className="text-2xl font-bold text-slate-200">2.4M</div>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl">
              <div className="text-xs text-slate-400 mb-1">RAG Cache Hit Rate</div>
              <div className="text-2xl font-bold text-slate-200">68%</div>
            </div>
          </div>
        </div>

        {/* Live Timeline */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-xl font-semibold mb-6">Live Workflow Timeline</h2>
          <div className="space-y-4">
            {events.length === 0 ? (
              <p className="text-slate-500 text-sm">Waiting for orchestrator events...</p>
            ) : events.map((ev, idx) => (
              <div key={idx} className="flex gap-4 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                <div className="flex flex-col items-center">
                  <div className="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold">
                    {ev.agent.substring(0,2).toUpperCase()}
                  </div>
                  {idx !== events.length - 1 && <div className="w-0.5 h-full bg-slate-700 mt-2"></div>}
                </div>
                <div className="flex-1 pb-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-medium text-slate-200">{ev.agent}</h4>
                      <p className="text-xs text-slate-400 mt-1">State: <span className="text-blue-400">{ev.workflow_state}</span></p>
                    </div>
                    <div className="text-right">
                      <span className={`text-xs font-mono px-2 py-1 rounded ${ev.requires_human_review ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                        Risk: {ev.risk_level}
                      </span>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center gap-2">
                    <div className="text-xs text-slate-400">Confidence</div>
                    <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-blue-500 to-emerald-400" style={{width: `${ev.confidence * 100}%`}}></div>
                    </div>
                    <div className="text-xs font-mono text-slate-300">{(ev.confidence * 100).toFixed(0)}%</div>
                  </div>
                  {/* AI Explainability Snippet */}
                  <div className="mt-3 p-2 bg-slate-950 rounded text-xs text-slate-500 font-mono italic">
                    Reasoning: Decision matched clinical guideline PR-7432. No DDI detected.
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Human Review Queue */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
           <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
             <span className="text-red-400">●</span> Human Review Queue
           </h2>
           <div className="space-y-3">
             <div className="p-4 rounded-xl bg-red-950/30 border border-red-900/50">
                <div className="flex justify-between">
                  <span className="font-medium text-slate-200">PT-88392</span>
                  <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded">High Risk</span>
                </div>
                <p className="text-sm text-slate-400 mt-2">Diagnosis agent detected conflicting allergies in history.</p>
                <button className="mt-3 w-full py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg text-sm transition-colors border border-red-500/20">
                  Review Case
                </button>
             </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
