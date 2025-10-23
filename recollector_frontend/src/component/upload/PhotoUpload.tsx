import { useNavigate } from 'react-router-dom';
import { usePhotoUpload, useGenerateModel } from '../../features';
import { EmptyUploadZone } from './NoPhoto';
import { PreviewUploadedPhoto } from './Preview';
import { UploadTips } from './UploadTips';
import { Button, Card } from '../../shared';
import { UploadingView } from './Uploading';

export function PhotoUploadWidget() {
  const navigate = useNavigate();
  
  // 파일 업로드 상태 관리
  const {
    selectedFile,
    previewUrl,
    isUploading,
    fileInputRef,
    handleFileSelect,
    handleFileInputChange,
    clearFile,
  } = usePhotoUpload();

  // 3D 모델 생성 API 호출
  const {
    isGenerating,
    error: generateError,
    startGeneration,
  } = useGenerateModel();

  // Generate 버튼 클릭 시
  const handleGenerate = async () => {
    if (!selectedFile) return;

    try {
      // 백엔드에 파일 전송 및 task_id 받기
      const taskId = await startGeneration(selectedFile);
      
      // task_id를 URL 파라미터로 전달하여 result 페이지로 이동
      //navigate(`/result/${taskId}`);
      
      navigate(`/loading/${taskId}`);
    } catch (err) {
      console.error('Generation failed:', err);
      // 에러 토스트나 모달 표시
    }
  };

  return (
    <div className="px-6 w-full">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 animate-fade-in">
            <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
              Photo Upload
            </span>
          </h1>
          <p className="text-gray-200 text-lg animate-fade-in animation-delay-200">
            사진 업로드
          </p>
        </div>

        {/* 에러 메시지 */}
        {generateError && (
          <Card className="mb-6 border-red-500/50 bg-red-500/10">
            <div className="flex items-center space-x-3">
              <i className="ri-error-warning-line text-2xl text-red-400"></i>
              <div>
                <h4 className="font-semibold text-white mb-1"> Generation Failed </h4>
                <p className="text-sm text-red-300">{generateError}</p>
              </div>
            </div>
          </Card>
        )}

        {/* Upload Card */}
        <Card className="mb-8 animate-fade-in animation-delay-400">
          {isUploading && <UploadingView />}
          
          {!isUploading && !selectedFile && (
            <EmptyUploadZone
              fileInputRef={fileInputRef}
              onFileSelect={handleFileSelect}
            />
          )}
          
          {!isUploading && selectedFile && previewUrl && (
            <PreviewUploadedPhoto
              file={selectedFile}
              previewUrl={previewUrl}
              fileInputRef={fileInputRef}
              onClear={clearFile}
            />
          )}
          
          {/* Hidden input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileInputChange}
            className="hidden"
          />
        </Card>

        {/* Generate Button */}
        {selectedFile && !isUploading && (
          <div className="text-center animate-fade-in animation-delay-500">
            <Button
              variant="primary"
              size="lg"
              onClick={handleGenerate}
              disabled={isGenerating}
              className="px-12 shadow-2xl shadow-purple-500/30 hover:shadow-purple-500/50 transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? (
                <>
                  <i className="ri-loader-4-line mr-2 animate-spin"></i>
                  Generating...
                </>
              ) : (
                <>
                  <i className="ri-arrow-right-line mr-2"></i>
                  3D 모델로 변환하기
                </>
              )}
            </Button>
          </div>
        )}

        {/* Tips */}
        <UploadTips />
      </div>
    </div>
  );
}