import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF, Environment, Center, PerspectiveCamera } from '@react-three/drei';
import { Suspense } from 'react';

function Model({ url }) {
  // useGLTF는 항상 호출되어야 함 (조건문 밖에서)
  const { scene } = useGLTF(url);
  
  // 그림자 활성화
  scene.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });
  
  return <primitive object={scene} />;
}

function LoadingSpinner() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#a855f7" wireframe />
    </mesh>
  );
}

function ErrorFallback() {
  return (
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="#ef4444" />
    </mesh>
  );
}

export const ModelViewer = ({ modelUrl }) => {

  // URL 검증은 컴포넌트 레벨에서 (Canvas 밖에서)
  if (!modelUrl || typeof modelUrl !== 'string') {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <i className="ri-error-warning-line text-5xl text-red-400 mb-4"></i>
          <p className="text-white text-lg">Invalid model URL</p>
          <p className="text-gray-400 text-sm mt-2">{String(modelUrl)}</p>
        </div>
      </div>
    );
  }

  return (
    <Canvas
      shadows
      dpr={[1, 2]}
      gl={{ 
        preserveDrawingBuffer: true,
        antialias: true,
        alpha: true
      }}
      style={{ 
        width: '100%', 
        height: '100%',
        background: 'transparent'
      }}
    >
      <PerspectiveCamera 
        makeDefault 
        position={[0, 0, 5]} 
        fov={50} 
      />
      
      <ambientLight intensity={0.6} />
      <directionalLight
        position={[5, 5, 5]}
        intensity={0.8}
        castShadow
      />
      <directionalLight
        position={[-5, 3, -5]}
        intensity={0.4}
      />
      <pointLight position={[0, 5, 0]} intensity={0.3} />

      <Suspense fallback={<LoadingSpinner />}>
        <Center>
          <Model url={modelUrl} />
        </Center>
        
        <Environment preset="sunset" />
      </Suspense>

      <OrbitControls
        makeDefault
        enableZoom={true}
        enablePan={true}
        enableRotate={true}
        minDistance={2}
        maxDistance={20}
        enableDamping
        dampingFactor={0.05}
      />
    </Canvas>
  );
};