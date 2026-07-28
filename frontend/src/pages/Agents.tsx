import { motion } from 'framer-motion';
import { Bot, Zap, Clock, CheckCircle } from 'lucide-react';

const AGENTS = [
  { name: 'Patient Intake', status: 'active', load: '45%', tasks: 12 },
  { name: 'Diagnosis', status: 'active', load: '82%', tasks: 8 },
  { name: 'Treatment Planning', status: 'idle', load: '10%', tasks: 0 },
  { name: 'Pharmacy', status: 'active', load: '65%', tasks: 24 },
  { name: 'Billing', status: 'error', load: '--', tasks: 3 },
  { name: 'Discharge', status: 'active', load: '20%', tasks: 4 },
];

export default function Agents() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">AI Agents Swarm</h2>
          <p className="text-textMuted mt-1">Manage and monitor specialized medical AI agents.</p>
        </div>
        <button className="btn-secondary flex items-center gap-2">
          <Zap className="w-4 h-4 text-amber-400" />
          <span>Wake All Agents</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {AGENTS.map((agent, i) => (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05 }}
            key={agent.name} 
            className="glass-panel p-6 relative overflow-hidden group hover:border-primary/30 transition-colors"
          >
            {/* Status Indicator Bar */}
            <div className={`absolute top-0 left-0 w-full h-1 ${
              agent.status === 'active' ? 'bg-primary shadow-[0_0_10px_rgba(59,130,246,0.8)]' : 
              agent.status === 'idle' ? 'bg-emerald-400' : 'bg-red-500'
            }`} />

            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-black/40 border border-white/10 flex items-center justify-center">
                  <Bot className={`w-5 h-5 ${agent.status === 'active' ? 'text-primary' : 'text-textMuted'}`} />
                </div>
                <div>
                  <h3 className="font-semibold text-white">{agent.name}</h3>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className={`w-1.5 h-1.5 rounded-full ${
                      agent.status === 'active' ? 'bg-primary animate-pulse' : 
                      agent.status === 'idle' ? 'bg-emerald-400' : 'bg-red-500'
                    }`}></span>
                    <span className="text-xs text-textMuted capitalize">{agent.status}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-6 p-4 rounded-xl bg-black/20 border border-white/5">
              <div>
                <div className="text-xs text-textMuted mb-1 flex items-center gap-1">
                  <Zap className="w-3 h-3" /> Load
                </div>
                <div className="font-medium text-white">{agent.load}</div>
              </div>
              <div>
                <div className="text-xs text-textMuted mb-1 flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" /> Queued
                </div>
                <div className="font-medium text-white">{agent.tasks}</div>
              </div>
            </div>
            
            <div className="mt-4 flex gap-2">
               <button className="flex-1 btn-secondary py-1.5 text-sm">Configure</button>
               <button className="flex-1 bg-white/5 hover:bg-white/10 text-white font-medium py-1.5 rounded-xl border border-white/10 text-sm transition-colors">Logs</button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
