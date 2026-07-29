import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Loader2, Plus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';
import { Button } from '../../components/ui/Button';
import { InsuranceService, OrchestratorService } from '../../services/api';

export default function InsuranceList() {
  const queryClient = useQueryClient();
  const [submitting, setSubmitting] = useState(false);
  const [msg, setMsg] = useState('');

  const { data: records, isLoading, isError } = useQuery({
    queryKey: ['insurance'],
    queryFn: InsuranceService.getAll,
  });

  const handleSubmitClaim = async () => {
    setSubmitting(true);
    setMsg('');
    try {
      const result = await OrchestratorService.startWorkflow('', {
        type: 'insurance',
        message: 'submit insurance claim for patient',
        patient_id: 'PT-12345',
      });
      setMsg(`Insurance workflow started. ID: ${result.workflow_id}`);
      queryClient.invalidateQueries({ queryKey: ['insurance'] });
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || 'Failed to start insurance workflow.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Insurance</h1>
        <Button
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
          onClick={handleSubmitClaim}
          disabled={submitting}
        >
          {submitting ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
          Submit Claim
        </Button>
      </div>

      {msg && <div className="rounded-md bg-primary/10 p-3 text-sm text-primary">{msg}</div>}

      <Card>
        <CardHeader><CardTitle>Insurance Claims</CardTitle></CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Provider</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell colSpan={5} className="h-24 text-center"><Loader2 className="mx-auto h-6 w-6 animate-spin text-muted-foreground" /></TableCell></TableRow>
              ) : isError ? (
                <TableRow><TableCell colSpan={5} className="h-24 text-center text-destructive">Failed to load insurance records.</TableCell></TableRow>
              ) : records?.items?.length === 0 ? (
                <TableRow><TableCell colSpan={5} className="h-24 text-center text-muted-foreground">No records found.</TableCell></TableRow>
              ) : (
                records?.items?.map((item: any) => (
                  <TableRow key={item.id}>
                    <TableCell className="font-mono text-xs">{item.id?.substring(0, 8)}</TableCell>
                    <TableCell>{item.provider_name || '—'}</TableCell>
                    <TableCell>${item.claim_amount || item.amount || '—'}</TableCell>
                    <TableCell>
                      <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                        item.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-700' :
                        item.status === 'REJECTED' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                      }`}>{item.status}</span>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" className="text-primary"
                        onClick={() => alert(`Claim ID: ${item.id}\nProvider: ${item.provider_name}\nStatus: ${item.status}`)}>
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
          <div className="mt-4 px-2 text-sm text-muted-foreground">{records?.total || 0} total claims</div>
        </CardContent>
      </Card>
    </div>
  );
}
