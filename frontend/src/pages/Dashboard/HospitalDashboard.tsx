import React from 'react';
import { Users, Activity, Clock, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';

export default function HospitalDashboard() {
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
            <Users className="h-4 w-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,248</div>
            <p className="text-xs text-slate-500">+12% from yesterday</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Emergencies</CardTitle>
            <AlertCircle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">3</div>
            <p className="text-xs text-slate-500">1 pending triage</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Wait Time</CardTitle>
            <Clock className="h-4 w-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24 min</div>
            <p className="text-xs text-slate-500">-2 min from average</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Workflows Active</CardTitle>
            <Activity className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">84</div>
            <p className="text-xs text-slate-500">0 errors reported</p>
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
                {/* Mock data */}
                <TableRow>
                  <TableCell className="font-medium">PT-10492</TableCell>
                  <TableCell>Sarah Jenkins</TableCell>
                  <TableCell><span className="inline-flex items-center rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-semibold text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400">Triage Complete</span></TableCell>
                  <TableCell>Cardiology</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">PT-10493</TableCell>
                  <TableCell>Michael Chen</TableCell>
                  <TableCell><span className="inline-flex items-center rounded-full bg-amber-100 px-2.5 py-0.5 text-xs font-semibold text-amber-800 dark:bg-amber-900/30 dark:text-amber-400">Pending Lab</span></TableCell>
                  <TableCell>Emergency</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">PT-10494</TableCell>
                  <TableCell>Emily Rodriguez</TableCell>
                  <TableCell><span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-semibold text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">Consultation</span></TableCell>
                  <TableCell>Pediatrics</TableCell>
                </TableRow>
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
              <div className="flex items-start gap-4 rounded-lg bg-red-50 p-3 dark:bg-red-950/30">
                <AlertCircle className="h-5 w-5 text-red-500 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-red-800 dark:text-red-400">Critical DDI Detected</h4>
                  <p className="text-xs text-red-600 dark:text-red-300 mt-1">
                    AI Safety Engine flagged Warfarin + Aspirin for PT-10492. Human review required.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-4 rounded-lg bg-blue-50 p-3 dark:bg-blue-950/30">
                <Activity className="h-5 w-5 text-blue-500 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-blue-800 dark:text-blue-400">Lab Results Ready</h4>
                  <p className="text-xs text-blue-600 dark:text-blue-300 mt-1">
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
