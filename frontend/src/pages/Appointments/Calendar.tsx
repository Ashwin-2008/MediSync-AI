import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Calendar as CalendarIcon, Clock, MoreVertical, Plus, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { AppointmentService } from '../../services/api';

export default function Calendar() {
  const { data: appointments, isLoading } = useQuery({
    queryKey: ['appointments'],
    queryFn: AppointmentService.getAll
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Appointments</h1>
          <p className="text-muted-foreground">Manage hospital schedules and consultations.</p>
        </div>
        <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">
          <Plus className="mr-2 h-4 w-4" /> New Appointment
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-4">
        <div className="md:col-span-1 space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Mini Calendar</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-secondary/50 rounded-lg h-64 flex items-center justify-center text-muted-foreground">
                <CalendarIcon className="h-10 w-10 opacity-50 mb-2" />
                <span className="block w-full text-center text-xs">Date picker placeholder</span>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Upcoming Today</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {isLoading ? (
                <div className="flex justify-center p-4">
                  <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                </div>
              ) : (
                appointments?.items?.map((apt: any, i: number) => {
                  const dateObj = new Date(apt.appointment_time);
                  const timeString = dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                  
                  return (
                    <div key={apt.id || i} className="flex items-start gap-3 border-b border-border pb-4 last:border-0 last:pb-0">
                      <div className="bg-primary/10 text-primary rounded p-2 text-xs font-bold text-center w-12">
                        {timeString.split(' ')[0]}<br/>{timeString.split(' ')[1] || ''}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium">{`Patient (${apt.patient_id?.substring(0, 5)})`}</p>
                        <p className="text-xs text-muted-foreground">{`Dr. (${apt.doctor_id?.substring(0, 5)})`} • {apt.status}</p>
                      </div>
                      <Button variant="ghost" size="icon" className="h-6 w-6"><MoreVertical className="h-4 w-4" /></Button>
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
                <h2 className="text-lg font-semibold">Today</h2>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">Day</Button>
                  <Button variant="outline" size="sm" className="bg-secondary">Week</Button>
                  <Button variant="outline" size="sm">Month</Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="flex h-[500px] items-center justify-center flex-col text-muted-foreground">
                <Clock className="h-16 w-16 mb-4 opacity-20" />
                <p>Full Calendar Grid View</p>
                <p className="text-xs mt-2 text-muted-foreground/60">React Big Calendar integration goes here</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
