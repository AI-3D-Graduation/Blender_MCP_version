import { useEmailSubmit } from "../../features";

interface EmailFormProps {
  taskId: string | undefined;
}

export const EmailForm = ({ taskId }: EmailFormProps) => {
  const { email, setEmail, emailSubmitted, isSubmitting, handleSubmit } = useEmailSubmit({
    taskId
  });

  if (emailSubmitted) {
    return (
      <div className="mb-8 animate-fade-in">
        <div className="max-w-md mx-auto p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
          <div className="flex items-center justify-center space-x-2">
            <i className="ri-check-line text-green-400 text-xl"></i>
            <p className="text-green-400 font-medium">
              접수 완료!
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mb-8 animate-fade-in animation-delay-400">
      <form onSubmit={handleSubmit} className="max-w-md mx-auto">
        <div className="flex flex-col space-y-4">
          <input
            type="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="이메일 주소를 입력하세요."
            className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all duration-200"
            required
            disabled={isSubmitting}
          />
          <button
            type="submit"
            disabled={!email.trim() || isSubmitting}
            className="w-full px-6 py-3 bg-gradient-to-r from-purple-500 to-cyan-400 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-cyan-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Saving...' : 'Save Email'}
          </button>
        </div>
      </form>

      <div className="mt-4 p-3 bg-gray-800/50 border border-gray-600/30 rounded-lg">
        <p className="text-sm text-white">
          변환이 완료되면 이메일로 결과물을 보내드립니다.
        </p>
      </div>
    </div>
  );
};