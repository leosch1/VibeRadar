"use client";
import dynamic from "next/dynamic";
import { useState, useMemo, useEffect, useRef } from "react";
import { getVibe } from "./services/api";
import LocationInfo from "./components/LocationInfo";
import type LocationInfoType from "./types/locationInfo";
import posthog from "posthog-js";

const World = dynamic(() => import("./components/world/World").then((m) => m.World), {
  ssr: false,
});

export default function Home() {
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [locationInfo, setLocationInfo] = useState<LocationInfoType | null>(null);
  const [isInfoBoxVisible, setIsInfoBoxVisible] = useState(false);
  const [isHoveringTitle, setIsHoveringTitle] = useState(false);
  const infoBoxRef = useRef<HTMLDivElement>(null);

  const onLocationSelected = (lat: number, lng: number) => {
    setSelectedLocation({ lat, lng });
  };

  useEffect(() => {
    if (!selectedLocation) {
      setLocationInfo(null);
      return;
    }

    getVibe(selectedLocation.lat, selectedLocation.lng)
      .then((info) => {
        setLocationInfo(info);

        posthog.capture("location clicked", {
          selectedLocation: {
            lat: selectedLocation.lat,
            lng: selectedLocation.lng,
          },
          locationName: info.locationName,
          countryName: info.countryName,
        });
      })
      .catch((error) => {
        console.error("Failed to fetch vibe:", error);
        setLocationInfo(null);
      });
  }, [selectedLocation]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        infoBoxRef.current &&
        !infoBoxRef.current.contains(event.target as Node)
      ) {
        setIsInfoBoxVisible(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const memoizedWorld = useMemo(() => (
    <World onLocationSelected={onLocationSelected} />
  ), []);

  const shouldShowInfoBox = isInfoBoxVisible || isHoveringTitle;

  return (
    <main className="min-h-screen bg-[#0a192f] text-white relative overflow-hidden">
      <div className="absolute top-12 left-12 z-10">
        <h1
          className="text-2xl flex items-center gap-2 cursor-pointer"
          onClick={() => setIsInfoBoxVisible((prev) => !prev)}
          onMouseEnter={() => setIsHoveringTitle(true)}
          onMouseLeave={() => setIsHoveringTitle(false)}
        >
          VibeRadar <span className="text-xl">📡</span>
        </h1>
        <div
          ref={infoBoxRef}
          className={`
            absolute top-full mt-2 left-0 w-72 p-4 bg-[#303030] rounded-lg shadow-lg
            transition-opacity duration-300 z-20
            ${shouldShowInfoBox ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"}
          `}
        >
          <p className="text-sm">
            Hi there! :) This is a project we built to discover vibes around the world.
            Spotify playlists come from the wonderful dataset at{" "}
            <a
              href="https://everynoise.com/everyplace.cgi"
              className="text-white underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              everynoise.com
            </a>.
            <br />
            <a
              href="/privacy-policy"
              className="text-xs text-[#cccccc] underline mt-1 inline-block"
              rel="noopener noreferrer"
            >
              Yes, we have a Privacy Policy too.
            </a>
          </p>
        </div>
      </div>

      <div className="flex items-center justify-center min-h-screen">
        <div className="relative w-full h-[100vh]">
          {memoizedWorld}
          {locationInfo && (
            <div className="absolute right-12 left-12 bottom-12 md:left-auto md:bottom-auto md:top-12 md:w-100">
              <LocationInfo info={locationInfo} />
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
