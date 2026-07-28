import React from 'react';
import { Search, Filter, Plus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

export default function PatientList() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h1 className="text-2xl font-bold tracking-tight">Patient Directory</h1>
        <Button className="bg-blue-600 hover:bg-blue-700 text-white">
          <Plus className="mr-2 h-4 w-4" /> Register Patient
        </Button>
      </div>

      <Card>
        <CardHeader className="pb-3">
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-500" />
              <Input type="text" placeholder="Search patients by name, ID, or phone..." className="pl-9" />
            </div>
            <Button variant="outline" className="w-full sm:w-auto">
              <Filter className="mr-2 h-4 w-4" /> Filters
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Patient ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>DOB</TableHead>
                <TableHead>Gender</TableHead>
                <TableHead>Blood Type</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell className="font-mono text-xs text-blue-600 dark:text-blue-400">PT-12345</TableCell>
                <TableCell className="font-medium">John Doe</TableCell>
                <TableCell>1980-05-15 (45y)</TableCell>
                <TableCell>Male</TableCell>
                <TableCell>O+</TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="sm" className="text-blue-600 hover:text-blue-700 dark:text-blue-400">View Profile</Button>
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="font-mono text-xs text-blue-600 dark:text-blue-400">PT-99887</TableCell>
                <TableCell className="font-medium">Jane Smith</TableCell>
                <TableCell>1992-11-23 (33y)</TableCell>
                <TableCell>Female</TableCell>
                <TableCell>A-</TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="sm" className="text-blue-600 hover:text-blue-700 dark:text-blue-400">View Profile</Button>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
          
          <div className="flex items-center justify-between mt-4 px-2 text-sm text-slate-500">
            <div>Showing 1-10 of 1,248 patients</div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" disabled>Previous</Button>
              <Button variant="outline" size="sm">Next</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
