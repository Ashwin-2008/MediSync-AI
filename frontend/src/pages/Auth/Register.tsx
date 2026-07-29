import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate } from 'react-router-dom';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import Lightfall from '../../components/react-bits/Lightfall';
import { AuthService } from '../../services/api';

const registerSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(12, "Password must be at least 12 characters"),
  first_name: z.string().min(2, "First name is required"),
  last_name: z.string().min(2, "Last name is required"),
  role: z.enum(['admin', 'doctor', 'nurse', 'receptionist']),
});

type RegisterForm = z.infer<typeof registerSchema>;

export default function Register() {
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();
  
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema)
  });

  const onSubmit = async (data: RegisterForm) => {
    setError('');
    setSuccess('');
    try {
      const submitData = {
        ...data,
        username: data.email
      };
      await AuthService.register(submitData);
      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background">
      <div className="absolute inset-0 z-0">
        <Lightfall
          colors={['#2563EB', '#10B981', '#3B82F6']}
          backgroundColor="#020617"
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

      <div className="relative z-10 w-full max-w-md p-4">
        <Card className="shadow-2xl shadow-primary/20 border-border bg-card/80 backdrop-blur-xl">
          <CardHeader className="space-y-1 pb-6 text-center">
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
              <span className="text-xl text-primary">✦</span>
            </div>
            <CardTitle className="text-2xl font-bold tracking-tight">Create Account</CardTitle>
            <p className="text-sm text-muted-foreground">
              Register for NovaHealth OS
            </p>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="flex gap-2">
                <div className="space-y-2 flex-1">
                  <Input
                    {...register('first_name')}
                    type="text"
                    placeholder="First Name"
                    className={errors.first_name ? "border-destructive" : ""}
                  />
                  {errors.first_name && <p className="text-xs text-destructive">{errors.first_name.message}</p>}
                </div>
                <div className="space-y-2 flex-1">
                  <Input
                    {...register('last_name')}
                    type="text"
                    placeholder="Last Name"
                    className={errors.last_name ? "border-destructive" : ""}
                  />
                  {errors.last_name && <p className="text-xs text-destructive">{errors.last_name.message}</p>}
                </div>
              </div>

              <div className="space-y-2">
                <Input
                  {...register('email')}
                  type="email"
                  placeholder="Email"
                  className={errors.email ? "border-destructive" : ""}
                />
                {errors.email && <p className="text-xs text-destructive">{errors.email.message}</p>}
              </div>
              
              <div className="space-y-2">
                <Input
                  {...register('password')}
                  type="password"
                  placeholder="Password"
                  className={errors.password ? "border-destructive" : ""}
                />
                {errors.password && <p className="text-xs text-destructive">{errors.password.message}</p>}
              </div>

              <div className="space-y-2">
                <select 
                  {...register('role')} 
                  className="w-full flex h-10 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                >
                  <option value="doctor">Doctor</option>
                  <option value="nurse">Nurse</option>
                  <option value="receptionist">Receptionist</option>
                  <option value="admin">Admin</option>
                </select>
                {errors.role && <p className="text-xs text-destructive">{errors.role.message}</p>}
              </div>

              {error && (
                <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
                  {error}
                </div>
              )}
              {success && (
                <div className="rounded-md bg-primary/10 p-3 text-sm text-primary">
                  {success}
                </div>
              )}

              <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" disabled={isSubmitting}>
                {isSubmitting ? 'Registering...' : 'Sign Up'}
              </Button>
            </form>
            
            <div className="mt-4 text-center text-sm text-muted-foreground">
              Already have an account? <Link to="/login" className="text-primary hover:underline">Sign In</Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
