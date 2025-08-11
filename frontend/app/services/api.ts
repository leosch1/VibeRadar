import { WeatherType } from "../types/locationInfo";

export const getMyCoordinates = async (): Promise<{ lat: number; lng: number }> => {
  const endpointDomain = 'https://ipapi.co/json/';

  const response = await fetch(endpointDomain);
  if (!response.ok) {
    return { // Fallback coordinates are in Switzerland
      lat: 46.8182,
      lng: 8.2275
    }
    // throw new Error('Failed to fetch coordinates');
  }
  const data = await response.json();
  return {
    lat: data.latitude,
    lng: data.longitude
  };
};

const mapWeatherCodeToSimpleType = (code: number): WeatherType => {
  // Open-Meteo weather codes: https://open-meteo.com/en/docs
  // Simplified mapping:
  if ([0, 1].includes(code)) return "sunny"; // Clear sky or mainly clear
  if ([2, 3, 45, 48].includes(code)) return "cloudy"; // Partly cloudy, overcast, fog
  if (
    [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]
      .includes(code)
  ) return "rainy"; // Various rain intensities
  return "sunny"; // default fallback
};

export const getOpenMeteoInfo = async (
  lat: number,
  lng: number
): Promise<{ temperatureCelsius: number; weatherType: WeatherType; utcOffsetSeconds: number }> => {
  const url =
    `https://api.open-meteo.com/v1/forecast` +
    `?latitude=${lat}&longitude=${lng}` +
    `&current=temperature_2m,weathercode` +
    `&timezone=auto`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`Weather API request failed: ${resp.status}`);
  const data = await resp.json();

  const temp = data.current?.temperature_2m ?? 0;
  const code = data.current?.weathercode ?? 0;
  const offset = data.utc_offset_seconds ?? 0;

  return {
    temperatureCelsius: temp,
    weatherType: mapWeatherCodeToSimpleType(code),
    utcOffsetSeconds: offset
  };
};

// NOT NEEDED ANYMORE SINCE APP IS NOW FRONTEND ONLY

// import type Connection from '../types/connection';
// import type { LocationInfoType } from '../types/locationInfo';

// export const getVibe = async (lat: number, lng: number): Promise<LocationInfo> => {
//   const backendDomain = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8008';

//   const response = await fetch(`${backendDomain}/getVibe`, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ lat, lng })
//   });

//   if (!response.ok) {
//     throw new Error('Failed to fetch vibe data');
//   }

//   return response.json();
// };

// export const getConnections = async (sessionId: string, myStart?: { lat: number; lng: number }, myEnd?: { lat: number; lng: number }): Promise<Connection[]> => {
//   const backendDomain = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8008';

//   const requestBody: {
//     sessionId: string;
//     myConnection?: Connection;
//   } = {
//     sessionId,
//   }

//   if (myStart && myEnd) {
//     requestBody.myConnection = {
//       start: myStart,
//       end: myEnd,
//     };
//   }

//   const response = await fetch(`${backendDomain}/getOtherConnections`, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify(requestBody),
//   });

//   if (!response.ok) {
//     throw new Error('Failed to fetch connections data');
//   }

//   const data: { connections: Connection[] } = await response.json();
//   return data.connections;
// };
