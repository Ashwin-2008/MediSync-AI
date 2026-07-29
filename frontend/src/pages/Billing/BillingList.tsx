import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Loader2, Plus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';
import { Button } from '../../components/ui/Button';
import { BillingService, OrchestratorService } from '../../services/api';

export default function BillingList() {
  const queryClient = useQueryClient();
  const [generating, setGenerating] = useState(false);
  const [msg, setMsg] = useState('');

  const { data: billing, isLoading, isError } = useQuery({
    queryKey: ['billing'],
    queryFn: BillingService.getAll,
  });

  const handleGenerate = async () => {
    setGenerating(true);
    setMsg('');
    try {
      const result = await OrchestratorService.startWorkflow('', {
        type: 'billing',
        message: 'generate invoice for patient',
        patient_id: 'PT-12345',
      });
      setMsg(`Billing workflow started. ID: ${result.workflow_id}`);
      queryClient.invalidateQueries({ queryKey: ['billing'] });
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || 'Failed to start billing workflow.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Billing</h1>
        <Button
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
          onClick={handleGenerate}
          disabled={generating}
        >
          {generating ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
          Generate Invoice
        </Button>
      </div>

      {msg && <div className="rounded-md bg-primary/10 p-3 text-sm text-primary">{msg}</div>}

      <Card>
        <CardHeader><CardTitle>Invoices</CardTitle></CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell colSpan={4} className="h-24 text-center"><Loader2 className="mx-auto h-6 w-6 animate-spin text-muted-foreground" /></TableCell></TableRow>
              ) : isError ? (
                <TableRow><TableCell colSpan={4} className="h-24 text-center text-destructive">Failed to load billing records.</TableCell></TableRow>
              ) : billing?.items?.length === 0 ? (
                <TableRow><TableCell colSpan={4} className="h-24 text-center text-muted-foreground">No records found.</TableCell></TableRow>
              ) : (
                billing?.items?.map((item: any) => (
                  <TableRow key={item.id}>
                    <TableCell className="font-mono text-xs">{item.id?.substring(0, 8)}</TableCell>
                    <TableCell>${item.total_amount}</TableCell>
                    <TableCell>
                      <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                        item.status === 'PAID' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                      }`}>{item.status}</span>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" className="text-primary"
                        onClick={() => alert(`Invoice ID: ${item.id}\nAmount: $${item.total_amount}\nStatus: ${item.status}`)}>
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
          <div className="mt-4 px-2 text-sm text-muted-foreground">
            {billing?.total || 0} total invoices
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
