export interface GlobeConfig {
  pointSize?: number;
  globeColor?: string;
  showAtmosphere?: boolean;
  atmosphereColor?: string;
  atmosphereAltitude?: number;
  emissive?: string;
  emissiveIntensity?: number;
  shininess?: number;
  polygonColor?: string;
  ambientLight?: string;
  directionalLeftLight?: string;
  directionalTopLight?: string;
  pointLight?: string;
  arcTime?: number;
  arcLength?: number;
  rings?: number;
  maxRings?: number;
  autoRotate?: boolean;
  autoRotateSpeed?: number;
  initialPosition?: {
    lat: number;
    lng: number;
  };
}

export interface Point {
  lat: number;
  lng: number;
  color: string;
}

export interface Arc {
  start: {
    lat: number;
    lng: number;
  };
  end: {
    lat: number;
    lng: number;
  };
  color: string;
  order: number;
  arcAltitude: number;
  arcStroke: number;
  arcDashInitialGap: number;
  arcDashGap: number;
  arcDashAnimateTime: number;
}
