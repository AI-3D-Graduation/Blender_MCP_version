import { Card } from "../../shared";
import { TiLightbulb, TiSocialInstagram } from "react-icons/ti";

export function UploadTips() {
  return (
    <div className="mt-12 grid md:grid-cols-2 gap-6">
      <Card padding="sm" className="border-cyan-500/30 animate-slide-in-left animation-delay-600">
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 bg-cyan-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1 animate-pulse text-white">
            <TiLightbulb/>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-1">Best Results</h4>
            <p className="text-sm text-gray-400">
              배경에 오브젝트가 적고 고화질 사진일수록 더욱 완벽한 결과물을 받아보실 수 있습니다.
            </p>
          </div>
        </div>
      </Card>
      
      <Card padding="sm" className="border-cyan-500/30 animate-slide-in-right animation-delay-700">
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 bg-cyan-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1 animate-pulse animation-delay-500 text-white">
            <TiSocialInstagram />
          </div>
          <div>
            <h4 className="font-semibold text-white mb-1">Processing Time</h4>
            <p className="text-sm text-gray-400">
              대부분의 사진은 5분 내로 변환됩니다. 업로드 된 사진의 사이즈, 화질에 따라 1~2분 정도 더 걸릴 수 있습니다.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
