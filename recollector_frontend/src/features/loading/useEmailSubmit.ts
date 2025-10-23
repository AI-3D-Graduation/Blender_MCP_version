import { useState } from "react";
import { emailApi } from "../../entities";


export interface UseEmailSubmitOptions {
  taskId: string | undefined;
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

export interface UseEmailSubmitReturn {
  email: string;
  setEmail: (email: string) => void;
  emailSubmitted: boolean;
  isSubmitting: boolean;
  handleSubmit: (e: React.FormEvent) => Promise<void>;
}

export const useEmailSubmit = ({
  taskId,
  onSuccess,
  onError
}: UseEmailSubmitOptions): UseEmailSubmitReturn => {
  const [email, setEmail] = useState('');
  const [emailSubmitted, setEmailSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !taskId || isSubmitting) return;

    setIsSubmitting(true);

    try {
      await emailApi.submitEmail(taskId, email);
      setEmailSubmitted(true);
      onSuccess?.();
    } catch (error) {
      console.error('Error submitting email:', error);
      onError?.('Failed to save email. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    email,
    setEmail,
    emailSubmitted,
    isSubmitting,
    handleSubmit
  };
};