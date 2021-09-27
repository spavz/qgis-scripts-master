const polyline = require('google-polyline')
const geolib = require('geolib');
const fs = require('fs');

// const pointsAlongLine = polyline.decode('uz`oDwnpuMUpEFLLDNh@HjA?rACZIRMPG@[?GD?`@@^BFxB\\jAJOv@i@zB[`AGHULyCx@QFXzANz@_ATk@PsAb@wA^_EjA_GbB]Do@IaD{@g@`DSlA?RALo@tEk@bCs@lCEd@AnCTlEV~CC^BXJ`@j@tERpB^lERdCTpCRdCFtA?r@AVUjBaAnEa@fBUzAG`@EdAEnB?dCAlBEbBM`Be@`Ec@`EUlBg@bEOdASlAGz@F`CBdChFH|GACbI@jB');
const pointsAlongLine = JSON.parse(fs.readFileSync('./data/pointsAlongLine.json')).pointsAlongLine;
const batteryRange = JSON.parse(fs.readFileSync('./config.json')).batteryRange;
let distanceTravelled = 0;
let deadBatteryPoint;

for (let i = 0; i < pointsAlongLine.length - 1; i++) {

    if (batteryRange <= distanceTravelled + geolib.getDistance(pointsAlongLine[i], pointsAlongLine[i + 1])) {
        deadBatteryPoint = pointsAlongLine[i];
        break;
    }
    distanceTravelled += geolib.getDistance(pointsAlongLine[i], pointsAlongLine[i + 1]);
}

console.log({ distanceTravelled })
console.log({ deadBatteryPoint })