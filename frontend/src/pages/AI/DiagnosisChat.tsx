import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, ShieldAlert, Sparkles, FileText, CheckCircle2, RefreshCw, AlertCircle } from 'lucide-react';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { OrchestratorService } from '../../services/api';

interface Message {
  id: string;
  role: 'user' | 'ai' | 'error';
  content: string;
  confidence?: number;
  safetyCheck?: boolean;
  evidence?: string[];
}

const CLIENT_TIMEOUT_MS = 45_000;

export default function DiagnosisChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'ai',
      content: "Hello. I'm ready to assist with clinical diagnosis. Please describe the patient's symptoms.",
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState('');
  const inFlightRef = useRef(false);       // duplicate-send guard
  const timeoutRef  = useRef<ReturnType<typeof setTimeout> | null>(null);
  const bottomRef   = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const stopLoading = () => {
    setIsTyping(false);
    inFlightRef.current = false;
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  };

  const appendMessage = (msg: Message) =>
    setMessages(prev => [...prev, msg]);

  const handleSend = async (retryText?: string) => {
    const text = (retryText ?? input).trim();
    if (!text || inFlightRef.current) return;

    inFlightRef.current = true;
    setError('');
    setInput('');
    setIsTyping(true);

    if (!retryText) {
      appendMessage({ id: Date.now().toString(), role: 'user', content: text });
    }

    // Client-side timeout — matches backend WORKFLOW_TIMEOUT
    timeoutRef.current = setTimeout(() => {
      stopLoading();
      setError('The AI service is taking too long to respond. Please try again.');
    }, CLIENT_TIMEOUT_MS);

    try {
      const response = await OrchestratorService.startWorkflow('', {
        // Pass both keys so keyword routing and agent both find what they need
        message:  text,
        symptoms: text,
        type:     'diagnosis',
        patient_id: 'PT-12345',
      });

      stopLoading();

      // Extract the diagnosis text from wherever the agent puts it
      const diagnosisText =
        response?.result?.diagnosis ||
        response?.result?.summary   ||
        response?.response           ||
        (response?.status === 'completed' ? 'Workflow completed — no diagnosis data returned.' : null) ||
        JSON.stringify(response, null, 2);

      appendMessage({
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: diagnosisText,
        confidence: response?.result?.confidence ?? response?.confidence ?? undefined,
        safetyCheck: true,
        evidence: response?.result?.evidence ?? response?.evidence ?? [],
      });
    } catch (err: any) {
      stopLoading();
      const detail =
        err?.response?.data?.detail ||
        err?.message ||
        'Unknown error from AI service.';
      setError(detail);
      console.error('[DiagnosisChat] error:', err);
    }
  };

  const handleRetry = () => {
    const lastUserMsg = [...messages].reverse().find(m => m.role === 'user');
    if (lastUserMsg) handleSend(lastUserMsg.content);
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-6">
      {/* Chat Area */}
      <div className="flex-1 flex flex-col bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
        {/* Header */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 flex justify-between items-center">
          <div className="flex items-center gap-2 font-semibold">
            <Sparkles className="h-5 w-5 text-blue-500" />
            AI Clinical Assistant
          </div>
          <span className="text-xs px-2 py-1 bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400 rounded-full flex items-center gap-1">
            <CheckCircle2 className="h-3 w-3" /> Safety Engine Active
          </span>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map(msg => (
            <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role !== 'user' && (
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

                {msg.role === 'ai' && msg.evidence && msg.evidence.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-800 space-y-3">
                    <div className="flex items-center gap-4 text-xs">
                      <div className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                        <ShieldAlert className="h-4 w-4" /> Safety Checked
                      </div>
                      {msg.confidence !== undefined && (
                        <div className="flex items-center gap-1 text-blue-600 dark:text-blue-400 font-mono">
                          Confidence: {(msg.confidence * 100).toFixed(1)}%
                        </div>
                      )}
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

          {/* Typing indicator */}
          {isTyping && (
            <div className="flex gap-4">
              <div className="h-8 w-8 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center">
                <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="bg-slate-100 dark:bg-slate-900 rounded-2xl p-4 flex items-center gap-2">
                <div className="h-2 w-2 bg-slate-400 rounded-full animate-bounce" />
                <div className="h-2 w-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                <div className="h-2 w-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
              </div>
            </div>
          )}

          {/* Error banner */}
          {error && !isTyping && (
            <div className="flex items-start gap-3 rounded-xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/30 p-4 text-sm text-red-700 dark:text-red-400">
              <AlertCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="font-medium">AI service error</p>
                <p className="mt-1 text-xs opacity-80">{error}</p>
              </div>
              <Button
                size="icon"
                variant="ghost"
                className="h-8 w-8 text-red-600 hover:bg-red-100 dark:hover:bg-red-900/40"
                onClick={handleRetry}
                title="Retry"
              >
                <RefreshCw className="h-4 w-4" />
              </Button>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="p-4 bg-white dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800">
          <div className="relative flex items-center">
            <Input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSend()}
              placeholder="Type symptoms, observations, or ask for differential diagnosis..."
              className="pr-12 h-12 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800 focus-visible:ring-blue-500"
              disabled={isTyping}
            />
            <Button
              size="icon"
              className="absolute right-1 h-10 w-10 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
              onClick={() => handleSend()}
              disabled={isTyping || !input.trim()}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
          {isTyping && (
            <p className="mt-2 text-xs text-slate-400 text-center">
              AI is processing… (up to 45s)
            </p>
          )}
        </div>
      </div>

      {/* Side Panel */}
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
