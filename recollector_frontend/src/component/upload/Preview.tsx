import { Button } from "../../shared";

interface PreviewUploadedPhotoProps {
  file: File;
  previewUrl: string;
  fileInputRef: React.RefObject<HTMLInputElement | null>;
  onClear: () => void;
}

export function PreviewUploadedPhoto({ 
  file, 
  previewUrl, 
  fileInputRef, 
  onClear 
}: PreviewUploadedPhotoProps) {
  return (
    <div className="text-center animate-fade-in">
      <div className="mb-6">
        <div className="relative inline-block">
          <img
            src={previewUrl}
            alt="Preview"
            className="w-64 h-64 object-cover rounded-2xl border-2 border-gray-600 animate-zoom-in"
          />
          <button
            onClick={onClear}
            className="absolute -top-3 -right-3 w-8 h-8 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center text-white transition-all duration-200 transform hover:scale-110 animate-fade-in animation-delay-300"
          >
            <i className="ri-close-line"></i>
          </button>
        </div>
      </div>
      
      <h3 className="text-xl font-semibold text-white mb-2 animate-fade-in animation-delay-100">
        {file.name}
      </h3>
      <p className="text-gray-400 mb-6 animate-fade-in animation-delay-200">
        {(file.size / 1024 / 1024).toFixed(2)} MB
      </p>
      
      <Button
        variant="ghost"
        size="sm"
        onClick={() => fileInputRef.current?.click()}
        className="mb-6 transform hover:scale-105 transition-transform duration-200 animate-fade-in animation-delay-300"
      >
        <i className="ri-refresh-line mr-2"></i>
        다른 사진 고르기
      </Button>
    </div>
  );
}