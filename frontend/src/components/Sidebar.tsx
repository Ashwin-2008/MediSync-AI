import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, Activity, Stethoscope, Pill, CreditCard, Bot, FileText, Settings, LogOut } from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'AI Agents', path: '/agents', icon: Bot },
  { name: 'Patients', path: '/patients', icon: Users },
  { name: 'Diagnosis', path: '/diagnosis', icon: Stethoscope },
  { name: 'Treatment', path: '/treatment', icon: Activity },
  { name: 'Pharmacy', path: '/pharmacy', icon: Pill },
  { name: 'Billing', path: '/billing', icon: CreditCard },
  { name: 'Reports', path: '/reports', icon: FileText },
];

export default function Sidebar() {
  return (
    <aside className="w-64 glass-panel border-y-0 border-l-0 rounded-none h-full flex flex-col relative z-20">
      <div className="p-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/20">
            <Activity className="text-white w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-white text-lg leading-tight">Nova<span className="text-primary">Health</span></h1>
            <p className="text-xs text-textMuted">AI Coordination System</p>
          </div>
        </div>
      </div>
      
      <div className="px-4 py-2 text-xs font-semibold text-textMuted uppercase tracking-wider">Menu</div>
      
      <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) => `
              flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group
              ${isActive 
                ? 'bg-primary/10 text-primary border border-primary/20 shadow-[inset_0_0_12px_rgba(59,130,246,0.1)]' 
                : 'text-textMuted hover:text-white hover:bg-white/5'
              }
            `}
          >
            <item.icon className={`w-5 h-5 transition-colors ${location.pathname.startsWith(item.path) ? 'text-primary' : 'group-hover:text-white'}`} />
            <span className="font-medium text-sm">{item.name}</span>
          </NavLink>
        ))}
      </nav>
      
      <div className="p-4 border-t border-white/5 mt-auto">
        <button className="flex items-center gap-3 px-3 py-2 text-textMuted hover:text-red-400 hover:bg-red-400/10 rounded-xl transition-all w-full text-left">
          <LogOut className="w-5 h-5" />
          <span className="font-medium text-sm">Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
