import type Connection from '../types/connection';
import type LocationInfo from '../types/locationInfo';

export const getVibe = async (lat: number, lng: number): Promise<LocationInfo> => {
  const backendDomain = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8008';

  const response = await fetch(`${backendDomain}/getVibe`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ lat, lng })
  });

  if (!response.ok) {
    throw new Error('Failed to fetch vibe data');
  }

  return response.json();
};

export const getConnections = async (sessionId: string, myStart?: { lat: number; lng: number }, myEnd?: { lat: number; lng: number }): Promise<Connection[]> => {
  const backendDomain = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8008';

  const requestBody: {
    sessionId: string;
    myConnection?: Connection;
  } = {
    sessionId,
  }

  if (myStart && myEnd) {
    requestBody.myConnection = {
      start: myStart,
      end: myEnd,
    };
  }

  const response = await fetch(`${backendDomain}/getOtherConnections`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch connections data');
  }

  const data: { connections: Connection[] } = await response.json();
  return data.connections;
};

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
