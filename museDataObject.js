class MuseDataObject {
    constructor(timeStamp, deltaTP9, deltaAF7, deltaAF8, deltaTP10, thetaTP9, thetaAF7, thetaAF8, thetaTP10, alphaTP9, alphaAF7, alphaAF8, alphaTP10, betaTP9, betaAF7, betaAF8, betaTP10, gammaTP9, gammaAF7, gammaAF8, gammaTP10, rawTP9, rawAF7, rawAF8, rawTP10) {
        this.timeStamp = timeStamp;
        this.deltaTP9 = deltaTP9;
        this.deltaAF7 = deltaAF7;
        this.deltaAF8 = deltaAF8;
        this.deltaTP10 = deltaTP10;
        this.thetaTP9 = thetaTP9;
        this.thetaAF7 = thetaAF7;
        this.thetaAF8 = thetaAF8;
        this.thetaTP10 = thetaTP10;
        this.alphaTP9 = alphaTP9;
        this.alphaAF7 = alphaAF7;
        this.alphaAF8 = alphaAF8;
        this.alphaTP10 = alphaTP10;
        this.betaTP9 = betaTP9;
        this.betaAF7 = betaAF7;
        this.betaAF8 = betaAF8;
        this.betaTP10 = betaTP10;
        this.gammaTP9 = gammaTP9;
        this.gammaAF7 = gammaAF7;
        this.gammaAF8 = gammaAF8;
        this.gammaTP10 = gammaTP10;
        this.rawTP9 = rawTP9;
        this.rawAF7 = rawAF7;
        this.rawAF8 = rawAF8;
        this.rawTP10 = rawTP10;
    }

    get deltaMeasures() {
        return [this.deltaTP9, this.deltaAF7, this.deltaAF8, this.deltaTP10];
    }

    get thetaMeasures() {
        return [this.thetaTP9, this.thetaAF7, this.thetaAF8, this.thetaTP10];
    }

    get alphaMeasures() {
        return [this.alphaTP9, this.alphaAF7, this.alphaAF8, this.alphaTP10];
    }

    get betaMeasures() {
        return [this.betaTP9, this.betaAF7, this.betaAF8, this.betaTP10];
    }

    get gammaMeasures() {
        return [this.gammaTP9, this.gammaAF7, this.gammaAF8, this.gammaTP10];
    }

    get rawMeasures() {
        return [this.gammaTP9, this.gammaAF7, this.gammaAF8, this.gammaTP10];
    }
}

module.exports = { MuseDataObject };
