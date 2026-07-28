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
    { name: 'Treatments', to: '/treatments', icon: TestTube2, roles: ['Admin', 'Doctor', 'Nurse'] },
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
    <div className="flex h-screen w-64 flex-col bg-card border-r border-border text-muted-foreground">
      <div className="flex h-16 items-center px-6 font-bold text-foreground tracking-tight border-b border-border">
        <span className="text-primary mr-2">✦</span> NovaHealth AI
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
                      ? "bg-primary text-primary-foreground shadow-md shadow-primary/20" 
                      : "hover:bg-secondary hover:text-secondary-foreground"
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
      
      <div className="p-4 border-t border-border text-xs text-muted-foreground/60">
        v2.4.0-enterprise
      </div>
    </div>
  );
}
