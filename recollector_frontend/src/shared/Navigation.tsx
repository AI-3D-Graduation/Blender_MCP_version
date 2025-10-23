import { useNavigate } from 'react-router-dom';

export default function Navigation() {
  const navigate = useNavigate();

  return (
    <nav className="w-full bg-transparent relative z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-8 py-4 sm:py-6">
        <div className="flex items-center justify-between">
          {/* Left - Brand Name */}
          <div
            className="cursor-pointer group"
            onClick={() => navigate('/')}
          >
            <h2 className="text-xl sm:text-2xl font-serif tracking-wide text-white">
              Recollector
            </h2>
          </div>
          
          {/* Right - Menu Items */}
          <div className="flex items-center space-x-4 sm:space-x-8">
            <button
              onClick={() => navigate('/')}
              className="text-xs sm:text-sm font-light tracking-wide text-white hover:text-white/70 transition-colors duration-300"
            >
              About Us
            </button>
            <button
              onClick={() => navigate('/')}
              className="px-3 sm:px-5 py-1.5 sm:py-2 border border-white/40 rounded-full text-xs sm:text-sm font-light tracking-wide text-white hover:bg-white hover:text-black transition-all duration-300"
            >
              Contact Us
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}