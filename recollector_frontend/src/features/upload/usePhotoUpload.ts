import { useState, useRef } from 'react';
import { validateImageFile } from '../../shared/lib/fileValidator';

export function usePhotoUpload() {
  const fileInputRef = useRef<HTMLInputElement>(null);  
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileSelect = (file: File) => {
    if (!validateImageFile(file)) {
      return;
    }

    setIsUploading(true);
    
    setTimeout(() => {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      setIsUploading(false);
    }, 1000);
  };

  const clearFile = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setSelectedFile(null);
    setPreviewUrl('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  return {
    selectedFile,
    previewUrl,
    isUploading,
    fileInputRef,  // RefObject<HTMLInputElement>로 반환됨
    handleFileSelect,
    handleFileInputChange,
    clearFile,
  };
}