
const hashjs = import('hash.js')

async function sha256(message) {

    const hashHex = (await hashjs).sha256().update(message).digest('hex');

    return hashHex;
}

function randInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function stringToColour(string) {
    return '#' + parseInt(string, 36).toString(16).slice(0, 6).toUpperCase();
}

function randomPointInCircle(latitude, longitude) {
    const earthRadius = 6371000.0
    const dx = randInt(10, 300)
    const dy = randInt(10, 300)
    const new_latitude = latitude + (dy / earthRadius) * (180 / Math.PI);
    const new_longitude = longitude + (dx / earthRadius) * (180 / Math.PI) / Math.cos(longitude * Math.PI / 180);

    return { latitude: new_latitude, longitude: new_longitude }
}

function distance(coords1, coords2) {
    const lat1 = coords1.latitude;
    const lon1 = coords1.longitude;
    const lat2 = coords2.latitude;
    const lon2 = coords2.longitude;
 
    const earthRadius = 6371000.0;
    const p = Math.PI / 180;
    const c = Math.cos;
    const a = 0.5 - c((lat2 - lat1) * p) / 2 +
        c(lat1 * p) * c(lat2 * p) *
        (1 - c((lon2 - lon1) * p)) / 2;

    return earthRadius * 2 * Math.asin(Math.sqrt(a));
}

export { sha256, randInt, stringToColour, randomPointInCircle, distance }