import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useAuth } from '../../contexts/AuthContext';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import Lightfall from '../../components/react-bits/Lightfall';

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
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background">
      {/* React Bits Lightfall Background */}
      <div className="absolute inset-0 z-0">
        <Lightfall
          colors={['#2563EB', '#10B981', '#3B82F6']} // Using enterprise hospital theme colors
          backgroundColor="#020617" // Deep slate background
          speed={0.7}
          streakCount={8}
          streakWidth={1.5}
          streakLength={1}
          glow={0.8}
          density={1}
          twinkle={1}
          zoom={1}
          backgroundGlow={1}
          opacity={1}
          mouseInteraction={true}
          mouseStrength={1}
          mouseRadius={0.6}
        />
      </div>

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-md p-4">
        <Card className="shadow-2xl shadow-primary/20 border-border bg-card/80 backdrop-blur-xl">
          <CardHeader className="space-y-1 pb-6 text-center">
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
              <span className="text-xl text-primary">✦</span>
            </div>
            <CardTitle className="text-2xl font-bold tracking-tight">NovaHealth OS</CardTitle>
            <p className="text-sm text-muted-foreground">
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
                  className={errors.email ? "border-destructive" : ""}
                />
                {errors.email && <p className="text-xs text-destructive">{errors.email.message}</p>}
              </div>
              
              <div className="space-y-2">
                <Input
                  {...register('password')}
                  type="password"
                  placeholder="••••••••"
                  className={errors.password ? "border-destructive" : ""}
                />
                {errors.password && <p className="text-xs text-destructive">{errors.password.message}</p>}
              </div>

              {error && (
                <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
                  {error}
                </div>
              )}

              <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" disabled={isSubmitting}>
                {isSubmitting ? 'Authenticating...' : 'Sign In'}
              </Button>
            </form>

            <div className="mt-6 text-center text-xs text-muted-foreground">
              <p>Demo accounts: admin@, doctor@, nurse@, reception@</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
