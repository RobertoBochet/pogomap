/* global key, google */
"use strict";

export class Entity {
    constructor(obj) {
        let self = this;

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
        this.marker.addListener("click", () => {
            self.updateInfoBox();
        });
        this.marker.setMap(Entity.env.map);
    }

    updateInfoBox() {
        console.log(this);
        Entity.env.currentEntity = this;

        Entity.env.infoSpaces.name.innerText = this.name;
        Entity.env.infoSpaces.image.src = this.image;

        if (typeof key !== "undefined" && key !== "") {
            Entity.env.editorButtons.type.container.childNodes.forEach((o) => {
                o.classList.remove("selected");
            });
            Entity.env.editorButtons.eligible.container.childNodes.forEach((o) => {
                o.classList.remove("selected");
            });
            switch (this.type) {
                case "gym":
                    Entity.env.editorButtons.type.select("button-gym");
                    break;
                case "pokestop":
                    Entity.env.editorButtons.type.select("button-pokestop");
                    break;
                case "unverified":
                    Entity.env.editorButtons.type.select("button-unverified");
                    break;
                case "portal":
                    Entity.env.editorButtons.type.select("button-portal");
                    break;
            }
            switch (this.isEligible) {
                case true:
                    Entity.env.editorButtons.eligible.select("button-eligible");
                    break;
                case false:
                    Entity.env.editorButtons.eligible.select("button-not-eligible");
                    break;
            }
        }
    }

    hide() {
        this.marker.setMap(null);
    }

    show() {
        this.marker.setMap(Entity.env.map);
    }
}

export class Unverified extends Entity {
    constructor(obj) {
        obj.type = "unverified";

        super(obj);
    }
}