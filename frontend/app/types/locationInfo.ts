export default interface LocationInfo {
    locationName: string;
    countryName: string;
    lat: number;
    lng: number;
    utcOffsetSeconds: number;
    weather: {
        temperatureCelsius: number;
        type: "cloudy" | "sunny" | "rainy";
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
