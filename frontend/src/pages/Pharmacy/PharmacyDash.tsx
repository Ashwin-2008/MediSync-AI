import React from 'react';
import { Pill, Search, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';

export default function PharmacyDash() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Pharmacy Module</h1>
          <p className="text-slate-500">Manage prescriptions, inventory, and DDI checks.</p>
        </div>
      </div>

      <Card className="bg-blue-50/50 dark:bg-blue-950/10 border-blue-100 dark:border-blue-900/50">
        <CardContent className="p-6">
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-500" />
              <Input placeholder="Search medications, active ingredients, or Rx IDs..." className="pl-9 h-10 bg-white dark:bg-slate-950" />
            </div>
            <Button className="bg-blue-600">Search Formulary</Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" /> Active DDI Warnings (2)
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/20 p-4 rounded-lg">
              <div className="flex justify-between items-start mb-2">
                <span className="font-semibold text-red-700 dark:text-red-400">Warfarin + Aspirin</span>
                <span className="text-xs font-mono text-red-500">PT-10492</span>
              </div>
              <p className="text-sm text-red-600 dark:text-red-300">High risk of catastrophic bleeding. Prescription pending doctor override.</p>
              <div className="mt-3 flex gap-2">
                <Button size="sm" variant="destructive">Reject Rx</Button>
                <Button size="sm" variant="outline" className="border-red-200 text-red-700">Contact MD</Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-emerald-500" /> Ready for Dispensing
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="border border-slate-200 dark:border-slate-800 p-4 rounded-lg flex justify-between items-center">
              <div>
                <p className="font-semibold">Amoxicillin 500mg (21 caps)</p>
                <p className="text-sm text-slate-500">PT-44556 • Dr. Smith</p>
              </div>
              <Button size="sm">Dispense</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
