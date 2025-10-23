const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

export function validateImageFile(file: File): boolean {
  // 파일 타입 검증
  if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
    alert('Only JPG, PNG, and WEBP files are supported');
    return false;
  }

  // 파일 크기 검증
  if (file.size > MAX_FILE_SIZE) {
    alert('File size must be less than 10MB');
    return false;
  }

  return true;
}

export function formatFileSize(bytes: number): string {
  return (bytes / 1024 / 1024).toFixed(2);
}