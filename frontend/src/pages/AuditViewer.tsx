import React from 'react';

const AuditViewer = () => {
  // Mock data for the audit log
  const auditLogs = [
    {
      id: "LOG-9921",
      timestamp: "2026-07-27 10:45:12 UTC",
      agent: "DiagnosisAgent",
      action: "Differential Diagnosis Generated",
      promptVersion: "v1.4",
      model: "gemini-1.5-pro",
      confidence: "High",
      hash: "8f4e3a2b...d91c",
      details: {
        symptoms: ["chest pain", "shortness of breath"],
        top_match: "Myocardial Infarction",
        safety_checks_passed: true
      }
    },
    {
      id: "LOG-9922",
      timestamp: "2026-07-27 10:46:01 UTC",
      agent: "SafetyAgent",
      action: "Drug Interaction Check",
      promptVersion: "v1.2",
      model: "gemini-1.5-flash",
      confidence: "Critical",
      hash: "7a1b9c8d...e23f",
      details: {
        drugs: ["Warfarin", "Aspirin"],
        result: "DDI Detected - High Bleed Risk",
        action_taken: "Escalated to Human Review"
      }
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <header className="mb-10">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-red-400 to-orange-400">
          Immutable Audit Log
        </h1>
        <p className="text-slate-400 mt-2">Cryptographically verifiable trace of all AI decisions.</p>
      </header>

      <div className="space-y-6">
        {auditLogs.map((log) => (
          <div key={log.id} className="p-6 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg">
            <div className="flex justify-between items-start mb-4 border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-slate-200">{log.action}</h3>
                <div className="text-sm text-slate-400 mt-1 flex gap-4">
                  <span><span className="text-slate-500">Agent:</span> {log.agent}</span>
                  <span><span className="text-slate-500">Time:</span> {log.timestamp}</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs font-mono bg-slate-950 px-2 py-1 rounded text-slate-500 mb-1">
                  SHA256: {log.hash}
                </div>
                <span className={`text-xs px-2 py-1 rounded ${log.confidence === 'Critical' ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                  Confidence: {log.confidence}
                </span>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm mb-4">
              <div><span className="text-slate-500">Model:</span> <span className="font-mono text-blue-400">{log.model}</span></div>
              <div><span className="text-slate-500">Prompt Config:</span> <span className="font-mono text-purple-400">{log.promptVersion}</span></div>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/50">
              <div className="text-xs text-slate-500 mb-2 font-semibold uppercase tracking-wider">Payload Details</div>
              <pre className="text-xs font-mono text-slate-300 whitespace-pre-wrap">
                {JSON.stringify(log.details, null, 2)}
              </pre>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AuditViewer;
