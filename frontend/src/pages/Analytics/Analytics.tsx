import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { AnalyticsService } from '../../services/api';

export default function Analytics() {
  const { data: records, isLoading, isError } = useQuery({
    queryKey: ['analytics'],
    queryFn: AnalyticsService.getAll
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight">Analytics</h1>
      <Card>
        <CardHeader>
          <CardTitle>System Performance</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex h-24 items-center justify-center">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          ) : isError ? (
            <div className="text-center text-destructive">Failed to load analytics.</div>
          ) : (
            <div className="grid gap-4 md:grid-cols-3">
               <div className="p-4 border rounded-lg bg-card">
                 <h3 className="text-sm font-medium text-muted-foreground">Total API Calls</h3>
                 <p className="text-2xl font-bold mt-2">1,204</p>
               </div>
               <div className="p-4 border rounded-lg bg-card">
                 <h3 className="text-sm font-medium text-muted-foreground">Active Workflows</h3>
                 <p className="text-2xl font-bold mt-2">42</p>
               </div>
               <div className="p-4 border rounded-lg bg-card">
                 <h3 className="text-sm font-medium text-muted-foreground">Error Rate</h3>
                 <p className="text-2xl font-bold mt-2 text-primary">0.5%</p>
               </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
