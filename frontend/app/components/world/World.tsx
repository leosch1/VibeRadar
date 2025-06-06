"use client";
import { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, PerspectiveCamera } from "@react-three/drei";
import { Globe } from "./Globe";
import WebGLRendererConfig from "./WebGlRenderConfig";
import SyncCameraAspect from "./SyncCameraAspect";
import { Stars } from "../Stars";
import getSunPositionOnEarth from "@/app/utils/sunPosition";
import "./World.css";

export function World({ onLocationSelected }: { onLocationSelected: (lat: number, lng: number) => void }) {
  const [shifted, setShifted] = useState(false);

  const handleGlobeClick = (lat: number, lng: number) => {
    setShifted(true);
    onLocationSelected(lat, lng);
  };

  const sunPosition = getSunPositionOnEarth();

  return (
    <div className="canvas-wrapper" style={{ left: shifted ? "-30vw" : "-15vw" }}>
      <Canvas>
        <Stars count={3000} />
        <PerspectiveCamera makeDefault fov={50} near={180} far={1800} />
        <SyncCameraAspect />
        <WebGLRendererConfig />
        <ambientLight color={"#1DB954"} intensity={0.9} />
        <directionalLight color="#fff6e5" intensity={3} position={sunPosition} castShadow={false} />
        <Globe onLocationSelected={handleGlobeClick} />
        <OrbitControls
          enablePan={false}
          enableZoom={false}
          minDistance={300}
          maxDistance={300}
          autoRotateSpeed={0.2}
          autoRotate={true}
          minPolarAngle={Math.PI / 3.5}
          maxPolarAngle={Math.PI - Math.PI / 3}
        />
      </Canvas>
    </div>
  );
}
