/* global google */
"use strict";


import {Entity, Unverified} from "./Entity.mjs";
import {DataLayer} from "./DataLayer.mjs";
import {ButtonsSet} from "./ButtonSet.mjs";

export class Environment {
    constructor(key = null) {
        this.key = typeof key === "string" ? key : null;
        this.mapElement = document.querySelector("#map");
        this.entities = [];
        this.currentEntity = null;

        Entity.env = this;

        this.makeMap();
        this.makeIcons();

        this.makeInfoSpaces();

        this.makeLayers();
        this.makeControlButtons();

        this.fetch();

        this.initEditor();
    }

    makeIcons() {
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

    makeMap() {
        this.map = new google.maps.Map(this.mapElement, {
            zoom: 15,
            center: new google.maps.LatLng(45.309552, 9.504114),
            mapTypeId: google.maps.MapTypeId.HYBRID,
            zoomControl: false,
            disableDefaultUI: true,
            clickableIcons: false
        });
    }

    makeInfoSpaces() {
        this.infoSpaces = {};
        this.infoSpaces.imageContainer = document.createElement("div");
        this.infoSpaces.image = document.createElement("img");
        this.infoSpaces.imageContainer.classList.add("container");
        this.infoSpaces.imageContainer.append(this.infoSpaces.image);
        this.infoSpaces.image.id = "image";
        this.infoSpaces.image.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=";

        this.map.controls[google.maps.ControlPosition.RIGHT_TOP].push(this.infoSpaces.imageContainer);

        this.infoSpaces.nameContainer = document.createElement("div");
        this.infoSpaces.name = document.createElement("div");
        this.infoSpaces.nameContainer.classList.add("container");
        this.infoSpaces.nameContainer.append(this.infoSpaces.name);
        this.infoSpaces.nameContainer.id = "nameContainer";
        this.infoSpaces.name.id = "name";

        this.map.controls[google.maps.ControlPosition.TOP_CENTER].push(this.infoSpaces.nameContainer);
    }

    makeControlButtons() {
        this.controlButtons = {};
        this.makeGridButtons();
        this.makeNestsButton();
    }

    makeGridButtons() {
        this.controlButtons.grids = new ButtonsSet("buttons-grids");

        this.controlButtons.grids.addButton("button-grid-small").addEventListener("click", () => {
            this.layers.s2cells.small.toggle();
        });
        this.controlButtons.grids.addButton("button-grid-big").addEventListener("click", () => {
            this.layers.s2cells.big.toggle();
        });

        this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(this.controlButtons.grids.container);
    }

    makeNestsButton() {
        this.controlButtons.nests = new ButtonsSet("buttons-nests");

        this.controlButtons.nests.addButton("button-nests").addEventListener("click", () => {
            this.layers.nests.toggle();
        });

        this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(this.controlButtons.nests.container);
    }

    makeLayers() {
        this.layers = {};
        this.makeGridLayers();
        this.makeNestsLayer();
    }

    makeGridLayers() {
        let s17 = new google.maps.Data();
        let s14 = new google.maps.Data();
        let s13 = new google.maps.Data();

        s17.setStyle({
            fillColor: "transparent",
            strokeColor: "#AAAAAA",
            strokeWeight: 1,
            zIndex: 3
        });
        s14.setStyle({
            fillColor: "transparent",
            strokeColor: "blue",
            strokeWeight: 3,
            zIndex: 5
        });
        s13.setStyle({
            fillColor: "transparent",
            strokeColor: "red",
            strokeWeight: 5,
            zIndex: 10
        });

        s17.loadGeoJson("/static/layers/s2cells/17.geojson");
        s14.loadGeoJson("/static/layers/s2cells/14.geojson");
        s13.loadGeoJson("/static/layers/s2cells/13.geojson");

        this.layers.s2cells = {};
        this.layers.s2cells.small = new DataLayer(this.map, [s13]);
        this.layers.s2cells.big = new DataLayer(this.map, [s14, s17]);
    }

    makeNestsLayer() {

        let nests = new google.maps.Data();

        nests.setStyle({
            fillColor: "green",
            fillOpacity: 0.6,
            strokeColor: "green",
            strokeWeight: 3,
            zIndex: 1
        });

        nests.loadGeoJson("/static/layers/nests.geojson");

        this.layers.nests = new DataLayer(this.map, [nests]);
    }

    initEditor() {
        let self = this;
        if (this.key !== null) {
            $.getJSON("/get_entities/unverified/", (data) => {
                if (data.done === true) {
                    for (let o of data.entities) {
                        self.entities.push(new Unverified(o));
                    }
                } else console.error("Error");
            }).then(null);
            $.getJSON("/get_entities/not_in_pogo/", (data) => {
                if (data.done === true) {
                    for (let o of data.entities) {
                        self.entities.push(new Entity(o));
                    }
                } else console.error("Error");
            }).then(null);

            this.makeEditorButtons();
        }
    }

    makeEditorButtons() {
        this.editorButtons = {};

        /*Type buttons*/
        this.editorButtons.type = new ButtonsSet("buttons-type");

        this.editorButtons.type.addButton("button-pokestop").addEventListener("click", () => {
            this.update({type: "pokestop"});
        });
        this.editorButtons.type.addButton("button-gym").addEventListener("click", () => {
            this.update({type: "gym"});
        });
        this.editorButtons.type.addButton("button-unverified").addEventListener("click", () => {
            this.update({type: "unverified"});
        });
        this.editorButtons.type.addButton("button-portal").addEventListener("click", () => {
            this.update({type: "portal"});
        });

        this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(this.editorButtons.type.container);

        /*Eligible buttons*/
        this.editorButtons.eligible = new ButtonsSet("buttons-eligible");

        this.editorButtons.eligible.addButton("button-eligible").addEventListener("click", () => {
            this.update({isEligible: true});
        });
        this.editorButtons.eligible.addButton("button-not-eligible").addEventListener("click", () => {
            this.update({isEligible: false});
        });

        this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(this.editorButtons.eligible.container);

        /*Edit buttons*/
        this.editorButtons.edit = new ButtonsSet("buttons-edit");

        this.editorButtons.edit.addButton("button-add").addEventListener("click", () => {
        });
        this.editorButtons.edit.addButton("button-remove").addEventListener("click", () => {
            this.removeEntity();
        });

        this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(this.editorButtons.edit.container);
    }

    update(obj) {
        if (typeof obj.type === "undefined" && typeof obj.isEligible === "undefined") {
            console.error("Error");
            return;
        }
        if (typeof obj.type !== "undefined" && obj.type === this.currentEntity.type) return;
        if (typeof obj.isEligible !== "undefined" && obj.isEligible === this.currentEntity.isEligible) return;

        $.ajax({
            type: "POST",
            url: "/set_entities/",
            data: JSON.stringify({
                key: this.key,
                id: this.currentEntity.id,
                type: ((typeof obj.type !== "undefined") ? obj.type : this.currentEntity.type),
                is_eligible: ((typeof obj.isEligible !== "undefined") ? obj.isEligible : this.currentEntity.isEligible)
            }),
            success: (data) => {
                if (data.done === true) {
                    if (typeof data.entity.type === "undefined") data.entity = new Unverified(data.entity);
                    else data.entity = new Entity(data.entity);

                    this.currentEntity.hide();
                    this.entities.filter((entity) => {
                        return this.currentEntity.id === data.entity.id;
                    });

                    this.entities.push(data.entity);
                    data.entity.updateInfoBox();
                } else console.error(data.error);
            },
            contentType: "application/json",
            dataType: "json"
        }).then(null);
    }

    removeEntity() {
        if(this.currentEntity === null) return;

        if(!confirm(`Are you sure to delete "${this.currentEntity.name}"?`)) return;

        $.ajax({
            type: "POST",
            url: "/remove_entities/",
            data: JSON.stringify({
                key: this.key,
                entities: [this.currentEntity.id]
            }),
            success: (data) => {
                if (data.done === true) {
                    this.currentEntity.hide();
                    this.entities.filter((entity) => {
                        return this.currentEntity.id === entity.id;
                    });
                } else console.error(data.error);
            },
            contentType: "application/json",
            dataType: "json"
        }).then(null);
    }

    fetch() {
        let self = this;
        $.getJSON("/get_entities/in_pogo/", (data) => {
            if (data.done === true) {
                for (let o of data.entities) {
                    self.entities.push(new Entity(o));
                }
            } else console.error("Error");
        }).then(null);
    }
}