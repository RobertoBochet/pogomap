"use strict";

export class ButtonsSet {
    constructor(id, classes = []) {
        this.buttons = [];

        this.container = document.createElement("div");
        this.container.id = id;

        this.container.classList.add("buttonsContainer");
        classes.forEach((v) => {
            this.container.classList.add(v);
        });
    }

    addButton(id) {
        let button = document.createElement("div");
        button.id = id;

        this.buttons.push(button);
        this.container.append(button);

        return button;
    }

    select(button) {
        this.buttons.forEach((v) => {
            if (v.id === button) v.classList.add("selected");
            else v.classList.remove("selected");
        });
    }

    deselect() {
        this.buttons.forEach((v) => {
            v.classList.remove("selected");
        });
    }
}