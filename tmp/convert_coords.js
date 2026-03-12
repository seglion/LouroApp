import proj4 from 'proj4';

const UTM_29N = "+proj=utm +zone=29 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs";
const WGS84 = "EPSG:4326";

const minUTM = [523746.411, 4652606.148];
const maxUTM = [538442.3128989211, 4676652.784];

const minLatLon = proj4(UTM_29N, WGS84, minUTM);
const maxLatLon = proj4(UTM_29N, WGS84, maxUTM);

console.log("--- BBox WGS84 (Lat, Lon) ---");
console.log(`Min: Lat ${minLatLon[1]}, Lon ${minLatLon[0]}`);
console.log(`Max: Lat ${maxLatLon[1]}, Lon ${maxLatLon[0]}`);

// Overpass format: (minLat, minLon, maxLat, maxLon)
console.log("\n--- Overpass BBox String ---");
console.log(`(${minLatLon[1].toFixed(6)},${minLatLon[0].toFixed(6)},${maxLatLon[1].toFixed(6)},${maxLatLon[0].toFixed(6)})`);
