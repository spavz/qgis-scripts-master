
const turf = require('@turf/turf');

const X_MIN = 76.819;
const X_MAX = 77.371;
const Y_MIN = 28.364;
const Y_MAX = 28.894;
const POINT_ACCURACY = 0.005;

const intersectedCirclesByChargingStationId = {}

let deadBatteryPoints = require('./deadBatteryPoints.json')


let stationIdNumber = 0;

for (let y = Y_MIN; y < Y_MAX; y += POINT_ACCURACY) {
    for (let x = X_MIN; x < X_MAX; x += POINT_ACCURACY) {
        stationIdNumber += 1
        const stationId = 'station_' + stationIdNumber;

        const stationCoordinates = turf.point([parseFloat(x.toFixed(5)), parseFloat(y.toFixed(5))]);
        deadBatteryPoints.features.forEach(deadBatteryPoint => {
            var center = deadBatteryPoint.geometry.coordinates;
            var radius = 500;
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
            intersectedCirclesByChargingStationId[stationId] = Array.from(intersectedCirclesByChargingStationId[stationId]);
        }
    }

}

outputFile = {features: []};

Object.keys(intersectedCirclesByChargingStationId).forEach(stationId => {
    outputFile.features.push({
        properties : {
            Unique_ID : stationId,
            circles: intersectedCirclesByChargingStationId[stationId].join('|')
        }
    })
})


console.log(JSON.stringify(outputFile, null, 2));
