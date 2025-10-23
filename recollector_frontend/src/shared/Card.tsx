
import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  padding?: 'sm' | 'md' | 'lg';
}

export default function Card({ children, className = '', padding = 'md' }: CardProps) {
  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };
  
  return (
    <div className={`bg-gray-900/80 backdrop-blur-sm border border-gray-700 rounded-2xl shadow-2xl ${paddingClasses[padding]} ${className}`}>
      {children}
    </div>
  );
}