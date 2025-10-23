
import { useNavigate } from 'react-router-dom';
import Navigation from '../shared/Navigation';

export default function Home() {
  const navigate = useNavigate();
  
  return (
    <div className="h-screen bg-black overflow-hidden">
      {/*네비게이션*/}
        <nav className="w-full bg-transparent absolute top-0 left-0 z-50">
          <div className="max-w-7xl mx-auto px-8 py-6">
            <div className="flex items-center justify-between">
              {/* Left - Brand Name */}
              <div
                className="cursor-pointer group"
                onClick={() => navigate('/')}
              >
                <h2 className="text-2xl font-serif tracking-wide text-white">
                  Recollector
                </h2>
                
              </div>
              
              {/* Right - Menu Items */}
              <div className="flex items-center space-x-8">
                <button
                  onClick={() => navigate('/')}
                  className="text-sm font-light tracking-wide text-white hover:text-white/70 transition-colors duration-300"
                >
                  About Us
                </button>
                <button
                  onClick={() => navigate('/')}
                  className="px-5 py-2 border border-white/40 rounded-full text-sm font-light tracking-wide text-white hover:bg-white hover:text-black transition-all duration-300"
                >
                  Contact Us
                </button>
              </div>
            </div>
          </div>
        </nav>

      {/* Hero Section */}
      <div className="relative h-full flex items-center justify-center px-6">
        {/* Background with texture */}
        <div className="absolute inset-0">
          <img src="img/exhibition_background.png"/>
          <div className="absolute inset-0 bg-black opacity-20"></div>
        </div>
        
        {/* Oval Image Container */}
        <div className="absolute inset-0 flex items-center justify-center">
          <img 
            src="/img/exhibition_main.png"
            alt="Main"
            className="max-w-full max-h-full object-contain opacity-100"
            style={{ maxWidth: '80%', maxHeight: '70%' }}
          />
        </div>
        
        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-black/40" />
        
        {/* Content */}
        <div className="relative z-10 text-center max-w-4xl mx-auto">
          {/* Main Logo/Title */}
          <div className="mb-12">
            <button
              onClick={() => navigate('/upload')}
              className="group"
            >
              <h1 className="text-7xl md:text-8xl lg:text-9xl font-light mb-6 leading-none tracking-wider transition-transform duration-300 group-hover:scale-105">
                <span className="text-white font-serif" style={{ textShadow: '2px 2px 20px rgba(0,0,0,0.8)' }}>
                  Recollector
                </span>
              </h1>
              <p className="text-base md:text-lg text-white/80 font-serif tracking-wide italic">
                Bring your memories into dimension
              </p>
            </button>
          </div>
          
          
        </div>
        
        {/* Subtle decorative elements */}
        <div 
          className="absolute w-1 h-1 bg-white/20 rounded-full animate-pulse"
          style={{ top: '25%', left: '25%' }}
        />
        <div 
          className="absolute w-1 h-1 bg-white/20 rounded-full animate-pulse"
          style={{ bottom: '33%', right: '25%', animationDelay: '1s' }}
        />
        <div 
          className="absolute w-1 h-1 bg-white/20 rounded-full animate-pulse"
          style={{ top: '50%', right: '33%', animationDelay: '0.5s' }}
        />
      </div>
    </div>
  );
}
