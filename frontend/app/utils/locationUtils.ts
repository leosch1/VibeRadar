// Haversine formula to calculate distance between two coordinates
export function calculateDistance(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const R = 6371; // Earth's radius in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lng2 - lng1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

export interface VibeData {
  cityName: string;
  regionCode: string;
  playlistId: string;
  lat: string;
  lng: string;
  countryName: string;
  videoId: string;
}

export function findClosestCity(lat: number, lng: number, vibesData: VibeData[]): VibeData {
  let closestCity = vibesData[0];
  let minDistance = Infinity;

  for (const city of vibesData) {
    const cityLat = parseFloat(city.lat);
    const cityLng = parseFloat(city.lng);
    const distance = calculateDistance(lat, lng, cityLat, cityLng);
    
    if (distance < minDistance) {
      minDistance = distance;
      closestCity = city;
    }
  }

  return closestCity;
}
