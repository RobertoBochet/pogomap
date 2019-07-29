"use strict";

export class Entity {
    constructor(obj) {
        let self = this;

        this.id = obj.id;
        this.name = obj.name;
        this.latitude = obj.latitude;
        this.longitude = obj.longitude;
        this.image = obj.image;

        this.type = (obj.type === undefined) ? "portal" : obj.type;
        this.is_eligible = (obj.is_eligible === undefined) ? false : Boolean(obj.is_eligible);

        switch (this.type) {
            case "portal":
                this.icon = Entity.icons.portal;
                break;
            case "pokestop":
                this.icon = Entity.icons.pokestop;
                break;
            case "gym":
                this.icon = (this.is_eligible) ? Entity.icons.gymEligible : Entity.icons.gym;
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
            self.updateInfobox();
        });
        this.marker.setMap(Entity.env.map);
    }

    updateInfobox() {
        console.log(this);
        Entity.env.currentEntity = this;

        Entity.env.infoSpaces.name.innerText = this.name;
        Entity.env.infoSpaces.image.src = this.image;

        if (key != "") {
            Entity.env.editorButtons.type.container.childNodes.forEach((o) => {
                o.classList.remove("selected");
            });
            Entity.env.editorButtons.eligible.container.childNodes.forEach((o) => {
                o.classList.remove("selected");
            });
            switch (this.type) {
                case "gym":
                    Entity.env.editorButtons.type.gym.classList.add("selected");
                    break;
                case "pokestop":
                    Entity.env.editorButtons.type.pokestop.classList.add("selected");
                    break;
                case "unverified":
                    Entity.env.editorButtons.type.unverified.classList.add("selected");
                    break;
                case "portal":
                    Entity.env.editorButtons.type.notInPogo.classList.add("selected");
                    break;
            }
            switch (this.is_eligible) {
                case true:
                    Entity.env.editorButtons.eligible.eligible.classList.add("selected");
                    break;
                case false:
                    Entity.env.editorButtons.eligible.notEligible.classList.add("selected");
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