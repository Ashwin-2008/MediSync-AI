import React, { useState } from 'react';
import { Pill, Search, AlertTriangle, CheckCircle2, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { OrchestratorService } from '../../services/api';

export default function PharmacyDash() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResult, setSearchResult] = useState('');
  const [searching, setSearching] = useState(false);
  const [actionMsg, setActionMsg] = useState('');
  const [actionLoading, setActionLoading] = useState('');

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    setSearchResult('');
    try {
      const result = await OrchestratorService.startWorkflow('', {
        type: 'pharmacy',
        message: `search formulary: ${searchQuery}`,
        symptoms: searchQuery,
      });
      const text = result?.result?.summary || result?.result?.diagnosis || JSON.stringify(result?.result || result);
      setSearchResult(text);
    } catch (e: any) {
      setSearchResult(e?.response?.data?.detail || 'Search failed.');
    } finally {
      setSearching(false);
    }
  };

  const handleAction = async (action: string, label: string) => {
    setActionLoading(action);
    setActionMsg('');
    try {
      const result = await OrchestratorService.startWorkflow('', {
        type: 'pharmacy',
        message: `${action} prescription`,
        patient_id: 'PT-10492',
      });
      setActionMsg(`${label}: Workflow ${result.workflow_id} started.`);
    } catch (e: any) {
      setActionMsg(e?.response?.data?.detail || `${label} failed.`);
    } finally {
      setActionLoading('');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Pharmacy Module</h1>
          <p className="text-slate-500">Manage prescriptions, inventory, and DDI checks.</p>
        </div>
      </div>

      <Card className="bg-blue-50/50 dark:bg-blue-950/10 border-blue-100 dark:border-blue-900/50">
        <CardContent className="p-6 space-y-3">
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-500" />
              <Input
                placeholder="Search medications, active ingredients, or Rx IDs..."
                className="pl-9 h-10 bg-white dark:bg-slate-950"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <Button className="bg-blue-600 hover:bg-blue-700" onClick={handleSearch} disabled={searching}>
              {searching ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Search Formulary'}
            </Button>
          </div>
          {searchResult && (
            <div className="rounded-md bg-white dark:bg-slate-900 border p-3 text-sm whitespace-pre-wrap">{searchResult}</div>
          )}
        </CardContent>
      </Card>

      {actionMsg && <div className="rounded-md bg-primary/10 p-3 text-sm text-primary">{actionMsg}</div>}

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" /> Active DDI Warnings
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/20 p-4 rounded-lg">
              <div className="flex justify-between items-start mb-2">
                <span className="font-semibold text-red-700 dark:text-red-400">Warfarin + Aspirin</span>
                <span className="text-xs font-mono text-red-500">PT-10492</span>
              </div>
              <p className="text-sm text-red-600 dark:text-red-300">High risk of catastrophic bleeding. Prescription pending doctor override.</p>
              <div className="mt-3 flex gap-2">
                <Button
                  size="sm" variant="destructive"
                  disabled={actionLoading === 'reject'}
                  onClick={() => handleAction('reject', 'Reject Rx')}
                >
                  {actionLoading === 'reject' ? <Loader2 className="h-3 w-3 animate-spin" /> : 'Reject Rx'}
                </Button>
                <Button
                  size="sm" variant="outline" className="border-red-200 text-red-700"
                  disabled={actionLoading === 'contact'}
                  onClick={() => handleAction('contact_md', 'Contact MD')}
                >
                  {actionLoading === 'contact' ? <Loader2 className="h-3 w-3 animate-spin" /> : 'Contact MD'}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-emerald-500" /> Ready for Dispensing
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="border border-slate-200 dark:border-slate-800 p-4 rounded-lg flex justify-between items-center">
              <div>
                <p className="font-semibold">Amoxicillin 500mg (21 caps)</p>
                <p className="text-sm text-slate-500">PT-44556 • Dr. Smith</p>
              </div>
              <Button
                size="sm"
                disabled={actionLoading === 'dispense'}
                onClick={() => handleAction('dispense amoxicillin', 'Dispense')}
              >
                {actionLoading === 'dispense' ? <Loader2 className="h-3 w-3 animate-spin" /> : 'Dispense'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
