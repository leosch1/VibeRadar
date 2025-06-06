import { useThree } from "@react-three/fiber";
import { useEffect } from "react";
import { PerspectiveCamera } from "three";

export default function SyncCameraAspect() {
  const { camera, size } = useThree();

  useEffect(() => {
    const cam = camera as PerspectiveCamera;
    cam.aspect = size.width / size.height;
    cam.updateProjectionMatrix();
  }, [camera, size]);

  return null;
}
