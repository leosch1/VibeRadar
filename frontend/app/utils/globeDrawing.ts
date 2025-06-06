import { Color, MeshPhongMaterial } from "three";
import { Arc, Point } from "../types/globe";
import { computeArcAltitude } from "./arcUtils";
import countries from "../data/globe.json";
import ThreeGlobe from "three-globe";
import Connection from "../types/connection";

export function initializeGlobe(globe: ThreeGlobe) {
  // Setup polygons for countries
  globe
    .hexPolygonsData(countries.features)
    .hexPolygonResolution(3)
    .hexPolygonMargin(0.7)
    .showAtmosphere(true)
    .atmosphereColor("#1DB954") // Spotify green
    .atmosphereAltitude(0.15)
    .hexPolygonColor(() => "rgba(255,255,255,0.7)");

  // Setup points styling
  globe
    .pointsMerge(true)
    .pointAltitude(0.0)
    .pointRadius(1);

  // Setup rings styling
  globe
    .ringsData([])
    .ringColor(() => "#1DB954") // Spotify green
    .ringMaxRadius(2)
    .ringPropagationSpeed(0.5)
    .ringRepeatPeriod(3000);
}

export function updateGlobeMaterial(globe: ThreeGlobe) {
  const globeMaterial = globe.globeMaterial() as MeshPhongMaterial;
  globeMaterial.color = new Color("#191414"); // Spotify black
  globeMaterial.emissive = new Color("#191414"); // Spotify black
  globeMaterial.emissiveIntensity = 0.1;
  globeMaterial.shininess = 0.9;
}

export function setGlobeInitialPosition(
  globe: ThreeGlobe,
  position: {
    lat: number;
    lng: number;
  }
) {
  globe.rotateY(position.lng * Math.PI / 180);
  globe.rotateX(-position.lat * Math.PI / 180);
}

function getPointsFromConnections(
  connections: Connection[],
  isOwnConnection: boolean,
): Point[] {
  return connections.flatMap((c) => [{
    lat: c.start.lat,
    lng: c.start.lng,
    color: isOwnConnection ? "#FFFFFF" : "#808080", // White for home points, gray for others
  }, {
    lat: c.end.lat,
    lng: c.end.lng,
    color: "#1DB954" // Spotify green
  }]);
}

export function updateGlobeData(
  globe: ThreeGlobe,
  connections: Connection[],
  myConnection: Connection | null
) {
  // Points
  let points = getPointsFromConnections(connections, false);
  if (myConnection) {
    const myPoints = getPointsFromConnections([myConnection], true);
    points = [...points, ...myPoints];
  }
  globe
    .pointsData(points)
    .pointColor((p: object) => (p as Point).color);

  // Rings around points
  const allConnections = myConnection ? [myConnection, ...connections] : connections;
  const connectionEndPoints = allConnections.map((c) => ({
    lat: c.end.lat,
    lng: c.end.lng
  }));
  globe.ringsData(connectionEndPoints)

  // Arcs
  const arcs: Arc[] = connections.map((c, index) => ({
    start: c.start,
    end: c.end,
    color: "#1DB954", // Spotify green
    order: (index + 1),
    arcAltitude: computeArcAltitude(c),
    arcStroke: 0.5,
    arcDashInitialGap: (index + 1) * 1,
    arcDashGap: 10,
    arcDashAnimateTime: 2000,
  }));
  if (myConnection) {
    arcs.push({
      start: myConnection.start,
      end: myConnection.end,
      color: "#1DB954", // Spotify green
      arcAltitude: computeArcAltitude(myConnection),
      order: 1,
      arcStroke: 1,
      arcDashInitialGap: 1,
      arcDashGap: 0,
      arcDashAnimateTime: 1000
    });
  }
  globe
    .arcsData(arcs)
    .arcStartLat((a: object) => (a as Arc).start.lat)
    .arcStartLng((a: object) => (a as Arc).start.lng)
    .arcEndLat((a: object) => (a as Arc).end.lat)
    .arcEndLng((a: object) => (a as Arc).end.lng)
    .arcColor((a: object) => (a as Arc).color)
    .arcAltitude((a: object) => (a as Arc).arcAltitude)
    .arcStroke((a: object) => (a as Arc).arcStroke)
    .arcDashInitialGap((a: object) => (a as Arc).arcDashInitialGap)
    .arcDashGap((a: object) => (a as Arc).arcDashGap)
    .arcDashAnimateTime((a: object) => (a as Arc).arcDashAnimateTime)
}
