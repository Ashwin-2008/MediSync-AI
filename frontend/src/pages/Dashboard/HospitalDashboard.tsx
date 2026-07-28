import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Users, Activity, Clock, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';
import { PatientService } from '../../services/api';

export default function HospitalDashboard() {
  const { data: patients, isLoading } = useQuery({
    queryKey: ['patients'],
    queryFn: PatientService.getAll
  });
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Hospital Overview</h1>
      </div>
      
      {/* Top Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Patients Today</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,248</div>
            <p className="text-xs text-muted-foreground">+12% from yesterday</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Emergencies</CardTitle>
            <AlertCircle className="h-4 w-4 text-destructive" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-destructive">3</div>
            <p className="text-xs text-muted-foreground">1 pending triage</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Wait Time</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24 min</div>
            <p className="text-xs text-muted-foreground">-2 min from average</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Workflows Active</CardTitle>
            <Activity className="h-4 w-4 text-accent" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">84</div>
            <p className="text-xs text-muted-foreground">0 errors reported</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
        {/* Main Panel */}
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Recent Patient Intakes</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Patient ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Assigned Dept</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center h-24">Loading...</TableCell>
                  </TableRow>
                ) : patients?.items?.slice(0, 5).map((patient: any) => (
                  <TableRow key={patient.id}>
                    <TableCell className="font-medium text-primary">{patient.id.substring(0, 8)}</TableCell>
                    <TableCell>{`${patient.first_name} ${patient.last_name}`}</TableCell>
                    <TableCell><span className="inline-flex items-center rounded-full bg-accent/20 px-2.5 py-0.5 text-xs font-semibold text-accent">Registered</span></TableCell>
                    <TableCell>General</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
        
        {/* Right Sidebar Panel */}
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>AI Notifications</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start gap-4 rounded-lg bg-destructive/10 p-3">
                <AlertCircle className="h-5 w-5 text-destructive mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-destructive">Critical DDI Detected</h4>
                  <p className="text-xs text-destructive/80 mt-1">
                    AI Safety Engine flagged Warfarin + Aspirin for PT-10492. Human review required.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-4 rounded-lg bg-primary/10 p-3">
                <Activity className="h-5 w-5 text-primary mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-primary">Lab Results Ready</h4>
                  <p className="text-xs text-primary/80 mt-1">
                    Complete Blood Count for PT-10493 processed via LIS Adapter.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
