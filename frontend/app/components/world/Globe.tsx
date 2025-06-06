"use client";
// This component is originally from Aceternity: https://ui.aceternity.com/components/github-globe
import { useEffect, useRef, useState } from "react";
import { Group, Vector2, PerspectiveCamera } from "three";
import ThreeGlobe from "three-globe";
import { useThree, extend, ThreeEvent } from "@react-three/fiber";
import {
  updateGlobeMaterial,
  updateGlobeData,
  setGlobeInitialPosition,
  initializeGlobe,
} from "../../utils/globeDrawing";
import {
  handlePointerDown,
  handlePointerUp,
  handleClick,
} from "../../utils/globeInteraction";
import { getConnections, getMyCoordinates } from "../../services/api";
import Connection from "../../types/connection";

extend({ ThreeGlobe: ThreeGlobe });

export function Globe({ onLocationSelected, }: {
  onLocationSelected: (lat: number, lng: number) => void;
}) {
  const [isInitialized, setIsInitialized] = useState(false);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [myConnection, setMyConnection] = useState<Connection | null>(null);
  const myCoordinatesRef = useRef<{ lat: number; lng: number } | null>(null);
  const sessionIdRef = useRef<string>(generateSessionId()); // Generate sessionId once
  const globeRef = useRef<ThreeGlobe | null>(null);
  const groupRef = useRef<Group>(null);
  const mouseDownPosition = useRef<Vector2 | null>(null);
  const { camera }: { camera: PerspectiveCamera } = useThree();

  function generateSessionId(): string {
    return (
      Math.random().toString(36).substring(2, 15) +
      Math.random().toString(36).substring(2, 15)
    );
  }

  useEffect(() => {
    const fetchConnections = async () => {
      try {
        const connections = await getConnections(
          sessionIdRef.current,
          myConnection?.start,
          myConnection?.end
        );
        setConnections(connections);
      } catch (error) {
        console.error("Failed to fetch connections:", error);
      }
    };

    fetchConnections();
    const interval = setInterval(fetchConnections, 30000);
    return () => clearInterval(interval);
  }, [myConnection]);

  useEffect(() => {
    if (!globeRef.current && groupRef.current) {
      globeRef.current = new ThreeGlobe();
      groupRef.current.add(globeRef.current);

      initializeGlobe(globeRef.current);
      updateGlobeMaterial(globeRef.current);
      setGlobeInitialPosition(globeRef.current, { lat: 0, lng: 0 });
      setIsInitialized(true);
    }
  }, []);

  useEffect(() => {
    if (!globeRef.current || !isInitialized || !connections) return;
    updateGlobeData(globeRef.current, connections, myConnection);
  }, [isInitialized, connections, myConnection]);

  useEffect(() => {
    const fetchMyCoordinates = async () => {
      try {
        const myCoordinates = await getMyCoordinates();
        myCoordinatesRef.current = myCoordinates;
      } catch (error) {
        console.error("Failed to fetch my coordinates:", error);
      }
    };

    fetchMyCoordinates();
  }, []);

  const onLocationSelect = (lat: number, lng: number) => {
    if (!myCoordinatesRef.current) {
      console.error("My coordinates are not available yet.");
      return;
    }

    const newConnection: Connection = {
      start: myCoordinatesRef.current,
      end: { lat, lng },
    };
    setMyConnection(newConnection);
    onLocationSelected(lat, lng);
  };

  const onPointerDown = (event: ThreeEvent<PointerEvent>) => {
    handlePointerDown(event, mouseDownPosition);
  };

  const onPointerUp = (event: ThreeEvent<PointerEvent>) => {
    const globe = globeRef.current;
    if (!globe) return;

    handlePointerUp(event, mouseDownPosition, (e) => {
      handleClick(e, globe, camera, onLocationSelect);
    });
  };

  return (
    <group
      ref={groupRef}
      onPointerDown={onPointerDown}
      onPointerUp={onPointerUp}
    />
  );
}
