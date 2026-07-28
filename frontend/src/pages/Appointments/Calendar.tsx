import React from 'react';
import { Calendar as CalendarIcon, Clock, MoreVertical, Plus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';

export default function Calendar() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Appointments</h1>
          <p className="text-slate-500">Manage hospital schedules and consultations.</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700 text-white">
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
              <div className="bg-slate-100 dark:bg-slate-900 rounded-lg h-64 flex items-center justify-center text-slate-400">
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
              {[1, 2, 3].map((_, i) => (
                <div key={i} className="flex items-start gap-3 border-b border-slate-100 dark:border-slate-800 pb-4 last:border-0 last:pb-0">
                  <div className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-400 rounded p-2 text-xs font-bold text-center w-12">
                    09:00<br/>AM
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">John Doe</p>
                    <p className="text-xs text-slate-500">Cardiology Consult</p>
                  </div>
                  <Button variant="ghost" size="icon" className="h-6 w-6"><MoreVertical className="h-4 w-4" /></Button>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
        
        <div className="md:col-span-3">
          <Card className="h-full min-h-[600px]">
            <CardHeader className="flex flex-row items-center justify-between border-b border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-4">
                <h2 className="text-lg font-semibold">Today</h2>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">Day</Button>
                  <Button variant="outline" size="sm" className="bg-slate-100 dark:bg-slate-900">Week</Button>
                  <Button variant="outline" size="sm">Month</Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="flex h-[500px] items-center justify-center flex-col text-slate-400">
                <Clock className="h-16 w-16 mb-4 opacity-20" />
                <p>Full Calendar Grid View</p>
                <p className="text-xs mt-2 text-slate-500">React Big Calendar integration goes here</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
