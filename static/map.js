/*jshint esversion: 6 */
/* global google, key */
import {Enviroment} from "./modules/Enviroment.mjs";

let env = null;

(() => {
    "use strict";

    // Waiting the loading of the google maps library
    let int = setInterval(() => {
        if (typeof google !== "object" || typeof google.maps !== "object") return;
        clearInterval(int);
        env = new Enviroment(key);
    }, 100);
})();
