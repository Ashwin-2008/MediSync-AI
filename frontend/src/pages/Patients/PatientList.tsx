import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Search, Filter, Plus, Loader2, RefreshCw } from 'lucide-react';
import { Card, CardContent, CardHeader } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { PatientService, OrchestratorService } from '../../services/api';

export default function PatientList() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [registering, setRegistering] = useState(false);
  const [registerMsg, setRegisterMsg] = useState('');

  const { data: patients, isLoading, isError } = useQuery({
    queryKey: ['patients', page],
    queryFn: () => PatientService.getAll(),
  });

  const filtered = patients?.items?.filter((p: any) =>
    search === '' ||
    `${p.first_name} ${p.last_name}`.toLowerCase().includes(search.toLowerCase()) ||
    p.id.includes(search)
  ) ?? [];

  const handleRegister = async () => {
    setRegistering(true);
    setRegisterMsg('');
    try {
      const result = await OrchestratorService.startWorkflow('', {
        type: 'intake',
        message: 'Register new patient',
        symptoms: 'new patient intake',
        patient_name: 'New Patient',
      });
      setRegisterMsg(`Intake workflow started. Workflow ID: ${result.workflow_id}`);
      queryClient.invalidateQueries({ queryKey: ['patients'] });
    } catch (e: any) {
      setRegisterMsg(e?.response?.data?.detail || 'Failed to start intake workflow.');
    } finally {
      setRegistering(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h1 className="text-2xl font-bold tracking-tight">Patient Directory</h1>
        <Button
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
          onClick={handleRegister}
          disabled={registering}
        >
          {registering ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
          Register Patient
        </Button>
      </div>

      {registerMsg && (
        <div className="rounded-md bg-primary/10 p-3 text-sm text-primary">{registerMsg}</div>
      )}

      <Card>
        <CardHeader className="pb-3">
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search patients by name or ID..."
                className="pl-9"
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
            </div>
            <Button variant="outline" className="w-full sm:w-auto" onClick={() => setSearch('')}>
              <Filter className="mr-2 h-4 w-4" /> Clear
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
                    <TableCell colSpan={5} className="h-24 text-center text-destructive">Failed to load patients.</TableCell>
                  </TableRow>
                ) : filtered.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">No patients found.</TableCell>
                  </TableRow>
                ) : (
                  filtered.map((patient: any) => (
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
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-primary hover:text-primary/80"
                          onClick={() => alert(`Patient ID: ${patient.id}\nName: ${patient.first_name} ${patient.last_name}`)}
                        >
                          View Profile
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>

          <div className="flex items-center justify-between mt-4 px-2 text-sm text-muted-foreground">
            <div>Showing {filtered.length} of {patients?.total || 0} patients</div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>Previous</Button>
              <Button variant="outline" size="sm" disabled={!patients || filtered.length < (patients?.size || 100)} onClick={() => setPage(p => p + 1)}>Next</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
