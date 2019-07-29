"use strict";


export class DataLayer {
    constructor() {
        this.isHide = true;
        this.data = [];
    }

    show() {
        for (let i in this.data) {
            if (this.data[i].getMap() === undefined) this.data[i].setMap(DataLayer.env.map);
        }
        this.isHide = false;
    }

    hide() {
        for (let i in this.data) {
            if (this.data[i].getMap() !== undefined) this.data[i].setMap(undefined);
        }
        this.isHide = true;
    }
}