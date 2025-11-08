import { Navigate, useLocation } from 'react-router-dom';
import { PropsWithChildren } from 'react';

function isAuthenticated(): boolean {
  return localStorage.getItem('auth') === 'true';
}

export default function ProtectedRoute({ children }: PropsWithChildren) {
  const location = useLocation();
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  return <>{children}</>;
}
