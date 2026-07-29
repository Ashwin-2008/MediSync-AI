import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, Loader2, UserRound, Filter } from 'lucide-react';
import { Card, CardContent, CardHeader } from '../../components/ui/Card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/Table';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { DoctorService } from '../../services/api';

export default function DoctorList() {
  const [search, setSearch] = useState('');

  const { data: doctors, isLoading, isError } = useQuery({
    queryKey: ['doctors'],
    queryFn: DoctorService.getAll,
  });

  const filtered = doctors?.items?.filter((d: any) =>
    search === '' ||
    (d.specialization || '').toLowerCase().includes(search.toLowerCase()) ||
    d.id.includes(search)
  ) ?? [];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h1 className="text-2xl font-bold tracking-tight">Doctor Directory</h1>
        <Button
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
          onClick={() => alert('Add Doctor form — connect to POST /api/v1/doctors/')}
        >
          <UserRound className="mr-2 h-4 w-4" /> Add Doctor
        </Button>
      </div>

      <Card>
        <CardHeader className="pb-3">
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search doctors by name or specialty..."
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
                  <TableHead>Doctor ID</TableHead>
                  <TableHead>Specialization</TableHead>
                  <TableHead>License No.</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  <TableRow><TableCell colSpan={5} className="h-24 text-center"><Loader2 className="mx-auto h-6 w-6 animate-spin text-muted-foreground" /></TableCell></TableRow>
                ) : isError ? (
                  <TableRow><TableCell colSpan={5} className="h-24 text-center text-destructive">Failed to load doctors.</TableCell></TableRow>
                ) : filtered.length === 0 ? (
                  <TableRow><TableCell colSpan={5} className="h-24 text-center text-muted-foreground">No doctors found.</TableCell></TableRow>
                ) : (
                  filtered.map((doc: any) => (
                    <TableRow key={doc.id}>
                      <TableCell className="font-mono text-xs text-primary">{doc.id.substring(0, 8)}</TableCell>
                      <TableCell className="font-medium">{doc.specialization || 'General'}</TableCell>
                      <TableCell className="font-mono text-xs">{doc.license_number || '—'}</TableCell>
                      <TableCell>
                        <span className="inline-flex items-center rounded-full bg-secondary px-2.5 py-0.5 text-xs font-semibold text-secondary-foreground">Active</span>
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost" size="sm" className="text-primary hover:text-primary/80"
                          onClick={() => alert(`Doctor ID: ${doc.id}\nSpecialization: ${doc.specialization}`)}
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
          <div className="mt-4 px-2 text-sm text-muted-foreground">
            Showing {filtered.length} of {doctors?.total || 0} doctors
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
