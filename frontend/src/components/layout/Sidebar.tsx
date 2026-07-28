import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { 
  LayoutDashboard, 
  Users, 
  UserRound,
  CalendarDays,
  BrainCircuit,
  TestTube2,
  Pill,
  Receipt,
  ShieldCheck,
  Bell,
  BarChart3,
  Settings,
  ServerCog
} from 'lucide-react';
import { cn } from '../../lib/utils';

export function Sidebar() {
  const { user } = useAuth();
  
  const navItems = [
    { name: 'Dashboard', to: '/', icon: LayoutDashboard, roles: ['Admin', 'Doctor', 'Nurse', 'Receptionist'] },
    { name: 'Patients', to: '/patients', icon: Users, roles: ['Admin', 'Doctor', 'Nurse', 'Receptionist'] },
    { name: 'Doctors', to: '/doctors', icon: UserRound, roles: ['Admin', 'Receptionist'] },
    { name: 'Appointments', to: '/appointments', icon: CalendarDays, roles: ['Admin', 'Doctor', 'Receptionist'] },
    { name: 'AI Diagnosis', to: '/ai-diagnosis', icon: BrainCircuit, roles: ['Admin', 'Doctor'] },
    { name: 'Lab Reports', to: '/labs', icon: TestTube2, roles: ['Admin', 'Doctor', 'Nurse'] },
    { name: 'Pharmacy', to: '/pharmacy', icon: Pill, roles: ['Admin', 'Doctor'] },
    { name: 'Billing', to: '/billing', icon: Receipt, roles: ['Admin', 'Receptionist'] },
    { name: 'Insurance', to: '/insurance', icon: ShieldCheck, roles: ['Admin', 'Receptionist'] },
    { name: 'Notifications', to: '/notifications', icon: Bell, roles: ['Admin', 'Doctor', 'Nurse', 'Receptionist'] },
    { name: 'Analytics', to: '/analytics', icon: BarChart3, roles: ['Admin'] },
    { name: 'Settings', to: '/settings', icon: Settings, roles: ['Admin', 'Doctor', 'Nurse', 'Receptionist'] },
    { name: 'AI Orchestrator', to: '/admin', icon: ServerCog, roles: ['Admin'] },
  ];

  const allowedItems = navItems.filter(item => 
    user && item.roles.includes(user.role)
  );

  return (
    <div className="flex h-screen w-64 flex-col bg-slate-950 border-r border-slate-800 text-slate-300">
      <div className="flex h-16 items-center px-6 font-bold text-white tracking-tight border-b border-slate-800">
        <span className="text-blue-500 mr-2">✦</span> NovaHealth AI
      </div>
      
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-3">
          {allowedItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.name}
                to={item.to}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                    isActive 
                      ? "bg-blue-600 text-white shadow-md shadow-blue-900/20" 
                      : "hover:bg-slate-900 hover:text-white"
                  )
                }
              >
                <Icon className="h-4 w-4" />
                {item.name}
              </NavLink>
            )
          })}
        </nav>
      </div>
      
      <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
        v2.4.0-enterprise
      </div>
    </div>
  );
}
