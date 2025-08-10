import type Connection from '../types/connection';
import type { LocationInfoType } from '../types/locationInfo';
import { findClosestCity, type VibeData } from '../utils/locationUtils';
import { getOpenMeteoInfo } from './api';

// Cache for vibes data to avoid repeated fetches
let vibesDataCache: VibeData[] | null = null;

async function loadVibesData(): Promise<VibeData[]> {
    if (vibesDataCache) {
        return vibesDataCache;
    }

    try {
        const response = await fetch('/vibes.json');
        if (!response.ok) {
            throw new Error('Failed to load vibes data');
        }
        const data = await response.json();
        vibesDataCache = data;
        return data;
    } catch (error) {
        console.error('Error loading vibes data:', error);
        throw new Error('Failed to load vibes data');
    }
}

export const getVibeWithoutApi = async (lat: number, lng: number): Promise<LocationInfoType> => {
    const vibesData = await loadVibesData();
    const closestCity = findClosestCity(lat, lng, vibesData);
    const openMeteoInfo = await getOpenMeteoInfo(lat, lng);

    // Transform the vibe data to match LocationInfo interface
    const locationInfo: LocationInfoType = {
        locationName: closestCity.cityName,
        countryName: closestCity.countryName,
        lat: parseFloat(closestCity.lat),
        lng: parseFloat(closestCity.lng),
        utcOffsetSeconds: openMeteoInfo.utcOffsetSeconds,
        weather: {
            temperatureCelsius: openMeteoInfo.temperatureCelsius,
            type: openMeteoInfo.weatherType
        },
        vibes: {
            spotify: {
                playlistId: closestCity.playlistId
            },
            youtube: {
                videoId: closestCity.videoId
            }
        }
    };

    return locationInfo;
};

export const getConnectionsWithoutApi = async (): Promise<Connection[]> => {
    // Return random connections
    const vibesData = await loadVibesData();
    const connections: Connection[] = [];

    for (let i = 0; i < 10; i++) {
        const startIndex = Math.floor(Math.random() * vibesData.length);
        const endIndex = Math.floor(Math.random() * vibesData.length);
        const startCity = vibesData[startIndex];
        const endCity = vibesData[endIndex];

        connections.push({
            start: {
                lat: parseFloat(startCity.lat),
                lng: parseFloat(startCity.lng)
            },
            end: {
                lat: parseFloat(endCity.lat),
                lng: parseFloat(endCity.lng)
            }
        });
    }
    return connections;
}
