import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useAuth } from '../../contexts/AuthContext';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';

// Temporary simplistic validation since it's client-side mocked
const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(4, "Password must be at least 4 characters"),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function Login() {
  const { login } = useAuth();
  const [error, setError] = useState('');
  
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginForm>();

  const onSubmit = async (data: LoginForm) => {
    setError('');
    // Mock API Call delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Hardcoded roles based on email domain for demo purposes
    if (data.email.includes('admin')) {
      login('mock-jwt-admin', 'Admin');
    } else if (data.email.includes('nurse')) {
      login('mock-jwt-nurse', 'Nurse');
    } else if (data.email.includes('reception')) {
      login('mock-jwt-receptionist', 'Receptionist');
    } else {
      // Default to doctor
      login('mock-jwt-doctor', 'Doctor');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 dark:bg-slate-900 p-4">
      <Card className="w-full max-w-md shadow-2xl shadow-blue-900/5 border-slate-200 dark:border-slate-800">
        <CardHeader className="space-y-1 pb-6 text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900/30">
            <span className="text-xl text-blue-600 dark:text-blue-400">✦</span>
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight">NovaHealth OS</CardTitle>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Enter your credentials to access the command center
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-2">
              <Input
                {...register('email')}
                type="email"
                placeholder="dr.smith@novahealth.com"
                className={errors.email ? "border-red-500" : ""}
              />
              {errors.email && <p className="text-xs text-red-500">{errors.email.message}</p>}
            </div>
            
            <div className="space-y-2">
              <Input
                {...register('password')}
                type="password"
                placeholder="••••••••"
                className={errors.password ? "border-red-500" : ""}
              />
              {errors.password && <p className="text-xs text-red-500">{errors.password.message}</p>}
            </div>

            {error && (
              <div className="rounded-md bg-red-50 p-3 text-sm text-red-500 dark:bg-red-500/10 dark:text-red-400">
                {error}
              </div>
            )}

            <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white" disabled={isSubmitting}>
              {isSubmitting ? 'Authenticating...' : 'Sign In'}
            </Button>
          </form>

          <div className="mt-6 text-center text-xs text-slate-500">
            <p>Demo accounts: admin@, doctor@, nurse@, reception@</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
