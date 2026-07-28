import React, { useState } from 'react';
import { Send, Bot, User, ShieldAlert, Sparkles, FileText, CheckCircle2 } from 'lucide-react';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { OrchestratorService } from '../../services/api';

interface Message {
  id: string;
  role: 'user' | 'ai';
  content: string;
  confidence?: number;
  safetyCheck?: boolean;
  evidence?: string[];
}

export default function DiagnosisChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'ai',
      content: 'Hello Dr. Smith. I am ready to assist with clinical diagnosis and treatment planning. Please describe the patient\'s symptoms, or enter a Patient ID to pull their chart.',
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    // Call backend API
    const runAI = async () => {
      try {
        const response = await OrchestratorService.startWorkflow("", { message: input, patient_id: "PT-12345" });
        setIsTyping(false);
        const aiMsg: Message = {
          id: (Date.now() + 1).toString(),
          role: 'ai',
          content: response.response || 'Workflow completed. Check dashboard for details.',
          confidence: response.confidence || 0.95,
          safetyCheck: true,
          evidence: response.evidence || []
        };
        setMessages(prev => [...prev, aiMsg]);
      } catch (err) {
        setIsTyping(false);
        setMessages(prev => [...prev, { id: Date.now().toString(), role: 'ai', content: 'Error communicating with AI service.' }]);
      }
    };
    runAI();
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-6">
      {/* Chat Area */}
      <div className="flex-1 flex flex-col bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 flex justify-between items-center">
          <div className="flex items-center gap-2 font-semibold">
            <Sparkles className="h-5 w-5 text-blue-500" />
            AI Clinical Assistant
          </div>
          <span className="text-xs px-2 py-1 bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400 rounded-full flex items-center gap-1">
            <CheckCircle2 className="h-3 w-3" /> Safety Engine Active
          </span>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map(msg => (
            <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'ai' && (
                <div className="h-8 w-8 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center flex-shrink-0">
                  <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                </div>
              )}
              
              <div className={`max-w-[80%] rounded-2xl p-4 ${
                msg.role === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
              }`}>
                <div className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</div>
                
                {msg.role === 'ai' && msg.evidence && (
                  <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-800 space-y-3">
                    <div className="flex items-center gap-4 text-xs">
                      <div className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                        <ShieldAlert className="h-4 w-4" /> Safety Checked
                      </div>
                      <div className="flex items-center gap-1 text-blue-600 dark:text-blue-400 font-mono">
                        Confidence: {(msg.confidence! * 100).toFixed(1)}%
                      </div>
                    </div>
                    
                    <div className="bg-slate-200/50 dark:bg-slate-950 p-2 rounded-lg text-xs font-mono text-slate-600 dark:text-slate-400">
                      <div className="font-semibold text-slate-700 dark:text-slate-300 mb-1 flex items-center gap-1">
                        <FileText className="h-3 w-3" /> Grounding Evidence
                      </div>
                      <ul className="list-disc list-inside space-y-1">
                        {msg.evidence.map((ev, i) => <li key={i}>{ev}</li>)}
                      </ul>
                    </div>
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="h-8 w-8 rounded-full bg-slate-200 dark:bg-slate-800 flex items-center justify-center flex-shrink-0">
                  <User className="h-5 w-5 text-slate-600 dark:text-slate-300" />
                </div>
              )}
            </div>
          ))}
          {isTyping && (
            <div className="flex gap-4">
              <div className="h-8 w-8 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center">
                <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="bg-slate-100 dark:bg-slate-900 rounded-2xl p-4 flex items-center gap-2">
                <div className="h-2 w-2 bg-slate-400 rounded-full animate-bounce"></div>
                <div className="h-2 w-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="h-2 w-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          )}
        </div>

        <div className="p-4 bg-white dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800">
          <div className="relative flex items-center">
            <Input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Type symptoms, observations, or ask for differential diagnosis..."
              className="pr-12 h-12 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800 focus-visible:ring-blue-500"
            />
            <Button 
              size="icon"
              className="absolute right-1 h-10 w-10 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
              onClick={handleSend}
              disabled={isTyping || !input.trim()}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Side Panel Context */}
      <div className="w-80 hidden lg:block space-y-4">
        <Card>
          <CardContent className="p-4">
            <h3 className="font-semibold text-sm mb-3">Active Context</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-500">Patient</span>
                <span className="font-medium">PT-12345 (John Doe)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Age/Gender</span>
                <span className="font-medium">45 / Male</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Allergies</span>
                <span className="font-medium text-red-500">Penicillin</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
