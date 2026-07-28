import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';
import { BillingService } from '../../services/api';

export default function BillingList() {
  const { data: billing, isLoading, isError } = useQuery({
    queryKey: ['billing'],
    queryFn: BillingService.getAll
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight">Billing</h1>
      <Card>
        <CardHeader>
          <CardTitle>Invoices</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={3} className="h-24 text-center">
                    <Loader2 className="mx-auto h-6 w-6 animate-spin text-muted-foreground" />
                  </TableCell>
                </TableRow>
              ) : isError ? (
                <TableRow>
                  <TableCell colSpan={3} className="h-24 text-center text-destructive">Failed to load billing records.</TableCell>
                </TableRow>
              ) : billing?.items?.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={3} className="h-24 text-center text-muted-foreground">No records found.</TableCell>
                </TableRow>
              ) : (
                billing?.items?.map((item: any) => (
                  <TableRow key={item.id}>
                    <TableCell className="font-mono text-xs">{item.id?.substring(0, 8)}</TableCell>
                    <TableCell>${item.total_amount}</TableCell>
                    <TableCell>{item.status}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
