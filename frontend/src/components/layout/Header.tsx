import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { Button } from '../ui/Button';
import { LogOut, Moon, Sun, Bell } from 'lucide-react';
import { cn } from '../../lib/utils';

export function Header() {
  const { user, logout } = useAuth();
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6 dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center gap-4">
        {/* Breadcrumbs could go here */}
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 hidden sm:block">
          Hospital Command Center
        </h2>
      </div>

      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={toggleTheme} className="text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100">
          {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </Button>
        
        <Button variant="ghost" size="icon" className="relative text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100">
          <Bell className="h-5 w-5" />
          <span className="absolute right-2 top-2 flex h-2 w-2 rounded-full bg-red-500"></span>
        </Button>

        <div className="flex items-center gap-3 pl-4 border-l border-slate-200 dark:border-slate-800">
          <div className="flex flex-col text-right hidden sm:flex">
            <span className="text-sm font-medium text-slate-900 dark:text-slate-100">{user?.name}</span>
            <span className="text-xs text-slate-500 dark:text-slate-400">{user?.role}</span>
          </div>
          <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-sm">
            {user?.name.charAt(0)}
          </div>
          <Button variant="ghost" size="icon" onClick={logout} className="text-slate-500 hover:text-red-500 ml-2">
            <LogOut className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  );
}
