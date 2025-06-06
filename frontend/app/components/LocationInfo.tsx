import { useEffect, useState } from 'react';
import type LocationInfo from '../types/locationInfo';
import styles from './LocationInfo.module.css'; // import the styles

interface LocationInfoProps {
  info: LocationInfo;
}

export default function LocationInfo({ info }: LocationInfoProps) {
  const [time, setTime] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const nowUTC = new Date(); // current time in user's local time
      const nowUTCms = nowUTC.getTime(); // in UTC ms

      const locationTime = new Date(nowUTCms + info.utcOffsetSeconds * 1000);

      // Format as HH:MM (24h)
      const hours = locationTime.getUTCHours().toString().padStart(2, '0');
      const minutes = locationTime.getUTCMinutes().toString().padStart(2, '0');

      setTime(`${hours}:${minutes}`);
    };

    updateTime(); // Set initial time
    const interval = setInterval(updateTime, 1000); // Update every second

    return () => clearInterval(interval); // Clean up
  }, [info.utcOffsetSeconds]);

  return (
    <div className="relative bg-[#202250]/70 backdrop-blur-md rounded-lg p-5 text-white shadow-xl overflow-hidden">
      {/* Cloud animation if cloudy */}
      {info.weather.type.toLowerCase() === 'cloudy' && (
        <div className="absolute -top-20 pointer-events-none z-0">
          <img
            src="/cloud.png"
            alt="cloud"
            className={`${styles.cloudSettle}`}
          />
        </div>
      )}

      {/* Rain animation if raining */}
      {info.weather.type.toLowerCase() === 'rainy' && (
        <div className={`${styles.rainContainer}`}>
          {Array.from({ length: 160 }).map((_, i) => {
            const left = Math.random() * 100;
            const delay = Math.random(); // in seconds
            const duration = 0.8 + Math.random() * 0.6;
            const width = 1 + Math.random();
            return (
              <div
                key={i}
                className={styles.rainDrop}
                style={{
                  left: `${left}%`,
                  animationDelay: `${delay}s`,
                  animationDuration: `${duration}s`,
                  width: `${width}px`,
                }}
              />
            );
          })}
        </div>
      )}

      {/* Main content */}
      <div className="relative z-10">
        <div className="mb-5">
          <div className="flex justify-between items-end mb-0.5">
            <h2 className="text-2xl font-medium">{info.locationName}</h2>
            <p className="text-xl font-medium">{time}</p>
          </div>
          <div className="flex justify-between items-end">
            <p className="text-white/80 font-medium">{info.countryName}</p>
            <p className="text-white/80 font-medium">
              {info.weather.temperatureCelsius}° C, {info.weather.type}
            </p>
          </div>
        </div>

        <div className="p-3 bg-[#303030] rounded-lg">
          <div className="relative aspect-[2/1] md:aspect-[5/6] overflow-hidden rounded-lg">
            <iframe
              src={`https://open.spotify.com/embed/playlist/${info.vibes.spotify.playlistId}?utm_source=generator&theme=0`}
              width="100%"
              height="200%"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
              loading="lazy"
              className="absolute inset-0"
            />
          </div>
        </div>

        <div className="mt-5 p-3 bg-[#303030] rounded-lg">
          <iframe
            className="rounded-lg"
            width="100%"
            height="100%"
            src={`https://www.youtube.com/embed/${info.vibes.youtube.videoId}?autoplay=1&mute=1&start=10&loop=1`}
            title="YouTube video player"
            allow="autoplay; encrypted-media; fullscreen;"
          />
        </div>
      </div>
    </div>
  );
}
