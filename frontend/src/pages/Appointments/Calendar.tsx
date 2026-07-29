import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Clock, Plus, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { AppointmentService, OrchestratorService } from '../../services/api';

type ViewMode = 'Day' | 'Week' | 'Month';

export default function Calendar() {
  const queryClient = useQueryClient();
  const [view, setView] = useState<ViewMode>('Week');
  const [booking, setBooking] = useState(false);
  const [bookMsg, setBookMsg] = useState('');

  const { data: appointments, isLoading } = useQuery({
    queryKey: ['appointments'],
    queryFn: AppointmentService.getAll,
  });

  const handleNewAppointment = async () => {
    setBooking(true);
    setBookMsg('');
    try {
      const result = await OrchestratorService.startWorkflow('', {
        type: 'appointment',
        message: 'schedule new appointment',
        patient_id: 'PT-12345',
      });
      setBookMsg(`Appointment workflow started. ID: ${result.workflow_id}`);
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    } catch (e: any) {
      setBookMsg(e?.response?.data?.detail || 'Failed to start appointment workflow.');
    } finally {
      setBooking(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Appointments</h1>
          <p className="text-muted-foreground">Manage hospital schedules and consultations.</p>
        </div>
        <Button
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
          onClick={handleNewAppointment}
          disabled={booking}
        >
          {booking ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
          New Appointment
        </Button>
      </div>

      {bookMsg && <div className="rounded-md bg-primary/10 p-3 text-sm text-primary">{bookMsg}</div>}

      <div className="grid gap-6 md:grid-cols-4">
        <div className="md:col-span-1">
          <Card>
            <CardHeader className="pb-3"><CardTitle className="text-base">Upcoming</CardTitle></CardHeader>
            <CardContent className="space-y-3">
              {isLoading ? (
                <div className="flex justify-center p-4"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>
              ) : appointments?.items?.length === 0 ? (
                <p className="text-sm text-muted-foreground">No appointments.</p>
              ) : (
                appointments?.items?.slice(0, 6).map((apt: any, i: number) => {
                  const t = new Date(apt.appointment_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                  return (
                    <div key={apt.id || i} className="flex items-start gap-3 border-b border-border pb-3 last:border-0 last:pb-0">
                      <div className="bg-primary/10 text-primary rounded p-2 text-xs font-bold text-center w-14 flex-shrink-0">{t}</div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">Patient {apt.patient_id?.substring(0, 6)}</p>
                        <p className="text-xs text-muted-foreground">{apt.status}</p>
                      </div>
                    </div>
                  );
                })
              )}
            </CardContent>
          </Card>
        </div>

        <div className="md:col-span-3">
          <Card className="h-full min-h-[600px]">
            <CardHeader className="flex flex-row items-center justify-between border-b border-border">
              <div className="flex items-center gap-4">
                <h2 className="text-lg font-semibold">Schedule</h2>
                <div className="flex gap-2">
                  {(['Day', 'Week', 'Month'] as ViewMode[]).map(v => (
                    <Button key={v} variant="outline" size="sm"
                      className={view === v ? 'bg-secondary' : ''}
                      onClick={() => setView(v)}
                    >{v}</Button>
                  ))}
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="flex h-[500px] items-center justify-center flex-col text-muted-foreground">
                <Clock className="h-16 w-16 mb-4 opacity-20" />
                <p className="font-medium">{view} View</p>
                <p className="text-xs mt-2 opacity-60">{appointments?.total || 0} total appointments</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
