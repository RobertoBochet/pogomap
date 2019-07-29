/* global google */
"use strict";

import {GUI} from "./GUI.mjs";
import {Entity, Unverified} from "./Entity.mjs";
import {EntitiesList} from "./EntitiesList.mjs";

export class Environment {
    constructor(key = null) {
        this.key = typeof key === "string" ? key : null;
        this.currentEntity = null;

        // Create a new entities list
        this.entities = new EntitiesList(this);

        // Init the GUI
        this.gui = new GUI(this);

        // Set the current entity to nothing
        this.setCurrentEntity(null);

        // Creates the icons for entities markers
        Entity.makeIcons();

        // Retrieves the entities
        this.getEntities();
    }


    setCurrentEntity(entity) {
        this.currentEntity = entity;

        this.gui.currentEntityChanges(entity);
    }

    getEntities() {
        let self = this;
        $.getJSON("/get_entities/in_pogo/", (data) => {
            if (data.done === true) {
                for (let o of data.entities) {
                    self.entities.push(new Entity(o));
                }
            } else console.error("Error");
        }).then(null);

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
        }
    }

    updateEntity(obj) {
        if (typeof obj.type === "undefined" && typeof obj.isEligible === "undefined") {
            console.error("Error");
            return;
        }
        if (typeof obj.type !== "undefined" && obj.type === this.currentEntity.type) return;
        if (typeof obj.isEligible !== "undefined" && obj.isEligible === this.currentEntity.isEligible) return;

        $.ajax({
            type: "POST",
            contentType: "application/json",
            dataType: "json",
            url: "/set_entities/",
            data: JSON.stringify({
                key: this.key,
                id: this.currentEntity.id,
                type: ((typeof obj.type !== "undefined") ? obj.type : this.currentEntity.type),
                is_eligible: ((typeof obj.isEligible !== "undefined") ? obj.isEligible : this.currentEntity.isEligible)
            }),
            success: (data) => {
                if (data.done === true) {
                    let new_entity = (typeof data.entity.type === "undefined") ? new Unverified(data.entity) :
                        new Entity(data.entity);

                    this.entities.remove(this.currentEntity);

                    this.entities.push(new_entity);
                    this.setCurrentEntity(new_entity);
                } else console.error(data.error);
            }
        }).then(null);
    }

    removeEntity() {
        if (this.currentEntity === null) return;

        if (!confirm(`Are you sure to delete "${this.currentEntity.name}"?`)) return;

        $.ajax({
            type: "POST",
            url: "/remove_entities/",
            data: JSON.stringify({
                key: this.key,
                entities: [this.currentEntity.id]
            }),
            success: (data) => {
                if (data.done === true) {
                    this.entities.remove(this.currentEntity);
                    this.setCurrentEntity(null);
                } else console.error(data.error);
            },
            contentType: "application/json",
            dataType: "json"
        }).then(null);
    }
}