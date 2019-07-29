"use strict";

export class ButtonsSet {
    constructor(id, classes = ["buttonsContainer"]) {
        this.buttons = [];

        this.container = document.createElement("div");
        this.container.id = id;

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
}