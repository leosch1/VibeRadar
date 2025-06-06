import { Vector3 } from 'three';

export default function getSunPositionOnEarth(radius = 1000): Vector3 {
  const now = new Date();
  const utcHours = now.getUTCHours() + now.getUTCMinutes() / 60;

  // Day of year for seasonal tilt
  const startOfYear = new Date(Date.UTC(now.getUTCFullYear(), 0, 0));
  const diff = now.getTime() - startOfYear.getTime();
  const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24));

  const subsolarLongitude = 15 * (12 - utcHours); // in degrees
  const subsolarLatitude = -23.44 * Math.cos((2 * Math.PI / 365) * (dayOfYear + 10)); // in degrees

  // Convert to radians
  const latRad = subsolarLatitude * (Math.PI / 180);
  const lonRad = subsolarLongitude * (Math.PI / 180);

  // Match Three.js coordinate system
  const x = radius * Math.cos(latRad) * Math.sin(lonRad);
  const y = radius * Math.sin(latRad);
  const z = radius * Math.cos(latRad) * Math.cos(lonRad);

  return new Vector3(x, y, z);
}
