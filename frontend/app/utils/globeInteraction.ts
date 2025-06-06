import { Vector2, Raycaster, PerspectiveCamera } from "three";
import { RefObject } from "react";
import { ThreeEvent } from "@react-three/fiber";
import ThreeGlobe from "three-globe";

export function handlePointerDown(event: ThreeEvent<PointerEvent>, mouseDownPosition: RefObject<Vector2 | null>) {
  event.stopPropagation();
  mouseDownPosition.current = new Vector2(event.clientX, event.clientY);
}

export function handlePointerUp(
  event: ThreeEvent<PointerEvent>,
  mouseDownPosition: RefObject<Vector2 | null>,
  onClick: (event: ThreeEvent<PointerEvent>) => void
) {
  if (!mouseDownPosition.current) return;

  const mouseUpPosition = new Vector2(event.clientX, event.clientY);
  const distance = mouseDownPosition.current.distanceTo(mouseUpPosition);

  // Only trigger click if mouse moved less than 5 pixels
  if (distance < 5) {
    onClick(event);
  }

  mouseDownPosition.current = null;
}

export function handleClick(
  event: ThreeEvent<PointerEvent>,
  globe: ThreeGlobe,
  camera: PerspectiveCamera,
  onLocationSelected: (lat: number, lng: number) => void
) {

  const canvas = document.querySelector("canvas");
  if (!canvas) {
    console.warn("Canvas not found in document.");
    return;
  }

  const rect = canvas.getBoundingClientRect();
  const mouse = new Vector2(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1
  );

  const raycaster = new Raycaster();
  raycaster.setFromCamera(mouse, camera);

  const intersects = raycaster.intersectObject(globe);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const lat = 90 - (Math.acos(point.y / point.length()) * 180) / Math.PI;
    const lng = (Math.atan2(point.x, point.z) * 180) / Math.PI;

    onLocationSelected(lat, lng);
  } else {
    console.warn("No intersection found.");
  }
}
