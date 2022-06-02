
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


const outputFile =  {'features': [], 'type': 'FeatureCollection', 'name': 'intersectedCircles', 'crs': {'type': 'name', 'properties': {
    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
}} }

Object.keys(intersectedCirclesByChargingStationId).forEach(stationId => {
    outputFile.features.push({
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

console.log('\nNumber of candidate charging stations: ' + outputFile.features.length +'\n')
fs.writeFileSync('./io/chargingStations.json', JSON.stringify(outputFile, null, 4))
fs.writeFileSync('./io/chargingStations.geojson', JSON.stringify(outputFile))

