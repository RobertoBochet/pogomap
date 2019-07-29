"use strict";


export class DataLayer {
    constructor(map, data=[]) {
        this.isHide = true;
        this.data = data;
        this.map = map;
    }

    show() {
        this.data.forEach((v) => {
            if (typeof v.getMap() === "undefined") v.setMap(this.map);
        });

        this.isHide = false;
    }

    hide() {
        this.data.forEach((v) => {
            if (typeof v.getMap() !== "undefined") v.setMap(undefined);
        });

        this.isHide = true;
    }
}