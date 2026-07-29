import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import Lightfall from '../../components/react-bits/Lightfall';

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = async (data: LoginForm) => {
    setError('');
    try {
      const { AuthService } = await import('../../services/api');

      // Step 1: authenticate and get the token
      const response = await AuthService.login(data);
      const token = response.access_token;

      // Step 2: store the token in localStorage BEFORE calling /me
      // The Axios request interceptor reads from localStorage, so this must
      // happen before any subsequent authenticated request fires.
      localStorage.setItem('token', token);

      // Step 3: now fetch the current user — the interceptor will attach the token
      const user = await AuthService.getCurrentUser();

      // Step 4: map backend role to frontend Role type
      let role: any = 'Doctor';
      if (user.role && typeof user.role === 'object' && user.role.name) {
        const roleName = user.role.name.toLowerCase();
        role = roleName.charAt(0).toUpperCase() + roleName.slice(1);
      } else if (typeof user.role === 'string') {
        const roleName = user.role.toLowerCase();
        role = roleName.charAt(0).toUpperCase() + roleName.slice(1);
      }

      const userObj = {
        id: user.id,
        name: user.full_name || user.first_name || user.email,
        role,
      };

      // Step 5: commit to AuthContext (also persists user to localStorage)
      login(token, userObj);

      // Step 6: explicit navigation — do not rely on re-render timing
      navigate('/', { replace: true });
    } catch (err: any) {
      // Clean up the token if anything after login() failed
      localStorage.removeItem('token');
      console.error(err);
      setError(err.response?.data?.detail || 'Invalid email or password');
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background">
      {/* React Bits Lightfall Background */}
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

              <Button
                type="submit"
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Authenticating...' : 'Sign In'}
              </Button>
            </form>

            <div className="mt-6 text-center text-xs text-muted-foreground">
              <p>Demo accounts: admin@hospital.com / password123</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
