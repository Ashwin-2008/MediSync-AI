import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, Filter, Plus, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { PatientService } from '../../services/api';

export default function PatientList() {
  const { data: patients, isLoading, isError } = useQuery({
    queryKey: ['patients'],
    queryFn: PatientService.getAll
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h1 className="text-2xl font-bold tracking-tight">Patient Directory</h1>
        <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">
          <Plus className="mr-2 h-4 w-4" /> Register Patient
        </Button>
      </div>

      <Card>
        <CardHeader className="pb-3">
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input type="text" placeholder="Search patients by name, ID, or phone..." className="pl-9" />
            </div>
            <Button variant="outline" className="w-full sm:w-auto">
              <Filter className="mr-2 h-4 w-4" /> Filters
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Patient ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Department</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  <TableRow>
                    <TableCell colSpan={5} className="h-24 text-center">
                      <Loader2 className="mx-auto h-6 w-6 animate-spin text-muted-foreground" />
                    </TableCell>
                  </TableRow>
                ) : isError ? (
                  <TableRow>
                    <TableCell colSpan={5} className="h-24 text-center text-destructive">
                      Failed to load patients.
                    </TableCell>
                  </TableRow>
                ) : patients?.items?.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                      No patients found.
                    </TableCell>
                  </TableRow>
                ) : (
                  patients?.items?.map((patient: any) => (
                    <TableRow key={patient.id}>
                      <TableCell className="font-mono text-xs text-primary">{patient.id.substring(0, 8)}</TableCell>
                      <TableCell className="font-medium">{`${patient.first_name} ${patient.last_name}`}</TableCell>
                      <TableCell>
                        <span className="inline-flex items-center rounded-full bg-secondary px-2.5 py-0.5 text-xs font-semibold text-secondary-foreground">
                          Registered
                        </span>
                      </TableCell>
                      <TableCell>General</TableCell>
                      <TableCell className="text-right">
                        <Button variant="ghost" size="sm" className="text-primary hover:text-primary/80">View Profile</Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
          
          <div className="flex items-center justify-between mt-4 px-2 text-sm text-muted-foreground">
            <div>Showing {patients?.items?.length || 0} of {patients?.total || 0} patients</div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" disabled={!patients || patients.page === 1}>Previous</Button>
              <Button variant="outline" size="sm" disabled={!patients || patients.items.length < patients.size}>Next</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
