/* global google */
"use strict";

import {ButtonsSet} from "./ButtonSet.mjs";
import {DataLayer} from "./DataLayer.mjs";

export class GUI {
    constructor(env, mapStage = null) {
        this.env = env;
        this.mapStage = mapStage !== null ? mapStage : document.querySelector("#map");

        this.makeMap();
        this.makeInfoSpaces();
        this.makeGridButtons();
        this.makeNestsButton();

        this.makeGridLayers();
        this.makeNestsLayer();

        if (this.env.key !== null) {
            this.makeEditorButtons();
        }

        this.makePlayer();
    }

    makeMap() {
        this.map = new google.maps.Map(this.mapStage, {
            zoom: 10,
            center: {lat: 45.464217, lng: 9.189511},
            mapTypeId: google.maps.MapTypeId.HYBRID,
            zoomControl: false,
            disableDefaultUI: true,
            clickableIcons: false
        });

        navigator.geolocation.getCurrentPosition((position) => {
            this.map.setCenter({
                lat: position.coords.latitude,
                lng: position.coords.longitude
            });
            this.map.setZoom(15);
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

    makeGridButtons() {
        this.gridButtons = {};
        this.gridButtons = new ButtonsSet("buttons-grids");

        this.gridButtons.addButton("button-grid-big").addEventListener("click", () => {
            this.s2cellsLayer.big.toggle();
        });
        this.gridButtons.addButton("button-grid-small").addEventListener("click", () => {
            this.s2cellsLayer.small.toggle();
        });

        this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(this.gridButtons.container);
    }

    makeNestsButton() {
        this.nestsButtons = new ButtonsSet("buttons-nests");

        this.nestsButtons.addButton("button-nests").addEventListener("click", () => {
            this.nestsLayer.toggle();
        });

        this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(this.nestsButtons.container);
    }

    makeEditorButtons() {
        this.editorButtons = {};

        /*Type buttons*/
        this.editorButtons.type = new ButtonsSet("buttons-type");

        this.editorButtons.type.addButton("button-pokestop").addEventListener("click", () => {
            this.env.updateEntity({type: "pokestop"});
        });
        this.editorButtons.type.addButton("button-gym").addEventListener("click", () => {
            this.env.updateEntity({type: "gym"});
        });
        this.editorButtons.type.addButton("button-unverified").addEventListener("click", () => {
            this.env.updateEntity({type: "unverified"});
        });
        this.editorButtons.type.addButton("button-portal").addEventListener("click", () => {
            this.env.updateEntity({type: "portal"});
        });

        this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(this.editorButtons.type.container);

        /*Eligible buttons*/
        this.editorButtons.eligible = new ButtonsSet("buttons-eligible");

        this.editorButtons.eligible.addButton("button-eligible").addEventListener("click", () => {
            this.env.updateEntity({isEligible: true});
        });
        this.editorButtons.eligible.addButton("button-not-eligible").addEventListener("click", () => {
            this.env.updateEntity({isEligible: false});
        });

        this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(this.editorButtons.eligible.container);

        /*Edit buttons*/
        this.editorButtons.edit = new ButtonsSet("buttons-edit");

        this.editorButtons.edit.addButton("button-add").addEventListener("click", () => {
            this.env.addEntities();
        });
        this.editorButtons.edit.addButton("button-remove").addEventListener("click", () => {
            this.env.removeEntity();
        });

        this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(this.editorButtons.edit.container);
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

        this.s2cellsLayer = {};
        this.s2cellsLayer.small = new DataLayer(this.map, [s14, s17]);
        this.s2cellsLayer.big = new DataLayer(this.map, [s13]);
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

        this.nestsLayer = new DataLayer(this.map, [nests]);
    }

    currentEntityChanges(entity) {
        if (entity !== null) {
            this.infoSpaces.name.innerText = entity.name;
            this.infoSpaces.image.src = entity.image;

            if (this.env.key !== null) {
                switch (entity.type) {
                    case "gym":
                        this.editorButtons.type.select("button-gym");
                        break;
                    case "pokestop":
                        this.editorButtons.type.select("button-pokestop");
                        break;
                    case "unverified":
                        this.editorButtons.type.select("button-unverified");
                        break;
                    case "portal":
                        this.editorButtons.type.select("button-portal");
                        break;
                }
                switch (entity.isEligible) {
                    case true:
                        this.editorButtons.eligible.select("button-eligible");
                        break;
                    case false:
                        this.editorButtons.eligible.select("button-not-eligible");
                        break;
                }
            }
        } else {
            this.infoSpaces.name.innerText = "";
            this.infoSpaces.image.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=";

            if (this.env.key !== null) {
                this.editorButtons.type.deselect();
                this.editorButtons.eligible.deselect();
            }
        }
    }

    makePlayer() {
        this.player = new google.maps.Marker({
            title: "Player",
            position: new google.maps.LatLng(0, 0),
            icon: {
                url: "/static/icons/cursor.svg",
                size: new google.maps.Size(45, 45),
                scaledSize: new google.maps.Size(45, 45),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(1 / 2 * 45, 1 / 2 * 45)
            },
            clickable: false,
            zIndex: 10
        });

        navigator.geolocation.watchPosition((position) => {
            if (typeof this.player.getMap() === "undefined") this.player.setMap(this.map);

            this.player.setPosition({
                lat: position.coords.latitude,
                lng: position.coords.longitude
            });
        });
    }
}