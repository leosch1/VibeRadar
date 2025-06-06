import { useEffect } from "react";
import { useThree } from "@react-three/fiber";

export default function WebGLRendererConfig() {
  const { gl, size } = useThree();

  useEffect(() => {
    gl.setPixelRatio(window.devicePixelRatio);
    gl.setSize(size.width, size.height);
    gl.setClearColor(0x07061E, 1);
  }, [gl, size.width, size.height]);

  return null;
}
