export type WeatherType = "cloudy" | "sunny" | "rainy";

export interface LocationInfoType {
    locationName: string;
    countryName: string;
    lat: number;
    lng: number;
    utcOffsetSeconds: number;
    weather: {
        temperatureCelsius: number;
        type: WeatherType;
    };
    vibes: {
        spotify: {
            playlistId: string;
        };
        youtube: {
            videoId: string;
        };
    };
}
