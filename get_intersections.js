
const turf = require('@turf/turf');
const fs = require('fs');

const X_MIN = 76.819;
const X_MAX = 77.371;
const Y_MIN = 28.364;
const Y_MAX = 28.894;
const POINT_ACCURACY = 0.005;

const intersectedCirclesByChargingStationId = {};
const coordinatesByChargingStationId = {};

const deadBatteryPoints = require('./io/deadBatteryPoints.json')
const config = require('./config.json')

circleSet = new Set();
let stationIdNumber = 0;

for (let y = Y_MIN; y < Y_MAX; y += POINT_ACCURACY) {
    for (let x = X_MIN; x < X_MAX; x += POINT_ACCURACY) {
        stationIdNumber += 1
        const stationId = 'station_' + stationIdNumber;

        const stationCoordinates = turf.point([parseFloat(x.toFixed(5)), parseFloat(y.toFixed(5))]);
        deadBatteryPoints.features.forEach(deadBatteryPoint => {
            var center = deadBatteryPoint.geometry.coordinates;
            var radius = config.demandRadius;
            var options = { steps: 10, units: 'meters' };
            var circle = turf.circle(center, radius, options);
            circleSet.add(JSON.stringify(circle));
            if (turf.booleanPointInPolygon(stationCoordinates, circle)) {
                if (!intersectedCirclesByChargingStationId[stationId]) {
                    intersectedCirclesByChargingStationId[stationId] = new Set();
                }
                intersectedCirclesByChargingStationId[stationId].add(deadBatteryPoint.properties.id)
            }
        });
        
        if (intersectedCirclesByChargingStationId[stationId]) {
            coordinatesByChargingStationId[stationId] = [parseFloat(x.toFixed(5)), parseFloat(y.toFixed(5))];
            intersectedCirclesByChargingStationId[stationId] = Array.from(intersectedCirclesByChargingStationId[stationId]);
        }
    }

}


const chargingStations =  {'features': [], 'type': 'FeatureCollection', 'name': 'chargingStations', 'crs': {'type': 'name', 'properties': {
    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
}} }

const circles =  {'features': [], 'type': 'FeatureCollection', 'name': 'circles', 'crs': {'type': 'name', 'properties': {
    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
}} }


Object.keys(intersectedCirclesByChargingStationId).forEach(stationId => {
    chargingStations.features.push({
        type: 'Feature',
        properties : {
            Unique_ID : stationId,
            circles: intersectedCirclesByChargingStationId[stationId].join('|')
        },
        geometry: {
            type: 'Point',
            coordinates: coordinatesByChargingStationId[stationId]
        }
    })
})

circles.features = Array.from(circleSet).map(circle => JSON.parse(circle))

console.log('\nNumber of candidate charging stations: ' + chargingStations.features.length +'\n')
fs.writeFileSync('./io/chargingStations.json', JSON.stringify(chargingStations, null, 4))
fs.writeFileSync('./io/chargingStations.geojson', JSON.stringify(chargingStations))

fs.writeFileSync('./io/circles.json', JSON.stringify(circles, null, 4))
fs.writeFileSync('./io/circles.geojson', JSON.stringify(circles))
// console.log(JSON.stringify(circles))

