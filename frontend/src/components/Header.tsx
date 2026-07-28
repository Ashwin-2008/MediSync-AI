import { Bell, Search } from 'lucide-react';

export default function Header() {
  return (
    <header className="h-16 glass-panel border-x-0 border-t-0 rounded-none px-6 flex items-center justify-between sticky top-0 z-10">
      <div className="flex items-center gap-4 w-96">
        <div className="relative w-full">
          <Search className="w-4 h-4 text-textMuted absolute left-3 top-1/2 -translate-y-1/2" />
          <input 
            type="text" 
            placeholder="Search patients, agents, records..." 
            className="input-field pl-10 h-10 text-sm bg-black/30"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <button className="relative p-2 text-textMuted hover:text-white transition-colors rounded-full hover:bg-white/5">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-primary rounded-full"></span>
        </button>
        
        <div className="h-8 w-px bg-white/10 mx-2"></div>
        
        <div className="flex items-center gap-3 cursor-pointer group">
          <div className="text-right hidden sm:block">
            <div className="text-sm font-semibold text-white group-hover:text-primary transition-colors">Dr. Sarah Jenkins</div>
            <div className="text-xs text-textMuted">Chief Oncologist</div>
          </div>
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 border-2 border-surface shadow-md">
            {/* Avatar placeholder */}
          </div>
        </div>
      </div>
    </header>
  );
}
