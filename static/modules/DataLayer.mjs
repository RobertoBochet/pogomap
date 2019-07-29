"use strict";


export class DataLayer {
    constructor(map, data = []) {
        this.isHide = true;
        this.data = data;
        this.map = map;
    }

    show() {
        this.data.forEach((v) => {
            v.setMap(this.map);
        });

        this.isHide = false;
    }

    hide() {
        this.data.forEach((v) => {
            v.setMap(null);
        });

        this.isHide = true;
    }

    toggle() {
        if (this.isHide) this.show();
        else this.hide();
    }
}