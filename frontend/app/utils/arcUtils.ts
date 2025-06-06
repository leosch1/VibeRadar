import Connection from "../types/connection";

export function computeArcAltitude(connection: Connection): number {
  const toRad = (deg: number): number => deg * (Math.PI / 180);

  const lat1 = toRad(connection.start.lat);
  const lat2 = toRad(connection.end.lat);
  const deltaLng = toRad(connection.end.lng - connection.start.lng);

  const angle = Math.acos(
    Math.sin(lat1) * Math.sin(lat2) +
    Math.cos(lat1) * Math.cos(lat2) * Math.cos(deltaLng)
  );

  const angularDistanceDeg = angle * (180 / Math.PI);

  // Base height + scaled height depending on arc distance
  const arcAlt = 0.05 + 0.65 * Math.pow(angularDistanceDeg / 180, 1.5);

  return arcAlt;
}
