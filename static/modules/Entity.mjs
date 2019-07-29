/* global google */
"use strict";

export class Entity {
    constructor(obj) {
        this.id = obj.id;
        this.name = obj.name;
        this.latitude = obj.latitude;
        this.longitude = obj.longitude;
        this.image = obj.image;

        this.type = (typeof obj.type === "undefined") ? "portal" : obj.type;
        this.isEligible = (typeof obj.is_eligible === "undefined") ? false : Boolean(obj.is_eligible);

        switch (this.type) {
            case "portal":
                this.icon = Entity.icons.portal;
                break;
            case "pokestop":
                this.icon = Entity.icons.pokestop;
                break;
            case "gym":
                this.icon = (this.isEligible) ? Entity.icons.gymEligible : Entity.icons.gym;
                break;
            case "unverified":
                this.icon = Entity.icons.unverified;
                break;
        }

        this.marker = new google.maps.Marker({
            position: new google.maps.LatLng(this.latitude, this.longitude),
            animation: google.maps.Animation.DROP,
            title: this.name,
            icon: this.icon,
            zIndex: this.icon.zIndex || 1
        });
    }

    static makeIcons() {
        Entity.icons = {
            portal: {
                url: "/static/icons/portal_pink.svg",
                size: new google.maps.Size(60, 60),
                scaledSize: new google.maps.Size(60, 60),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(1 / 2 * 60, 9 / 10 * 60)
            },
            pokestop: {
                url: "/static/icons/pokestop_blue.svg",
                size: new google.maps.Size(60, 60),
                scaledSize: new google.maps.Size(60, 60),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(1 / 2 * 60, 9 / 10 * 60),
                zIndex: 2
            },
            gym: {
                url: "/static/icons/gym.svg",
                size: new google.maps.Size(45, 45),
                scaledSize: new google.maps.Size(45, 45),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(1 / 2 * 45, 1 / 2 * 45),
                zIndex: 3
            },
            gymEligible: {
                url: "/static/icons/gym_gold.svg",
                size: new google.maps.Size(45, 45),
                scaledSize: new google.maps.Size(45, 45),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(1 / 2 * 45, 1 / 2 * 45),
                zIndex: 4
            },
            unverified: {
                url: "/static/icons/question_mark.svg",
                size: new google.maps.Size(45, 45),
                scaledSize: new google.maps.Size(45, 45),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(1 / 2 * 45, 1 / 2 * 45),
                zIndex: 5
            }
        };
    }
}


export class Unverified extends Entity {
    constructor(obj) {
        obj.type = "unverified";

        super(obj);
    }
}