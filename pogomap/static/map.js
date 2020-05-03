/*jshint esversion: 6 */
/* global google, key */
import {Environment} from "./modules/Environment.mjs";

let env = null;

(() => {
    "use strict";

    // Waiting the loading of the google maps library
    let int = setInterval(() => {
        if (typeof google !== "object" || typeof google.maps !== "object") return;
        clearInterval(int);
        env = new Environment(key);
    }, 100);
})();
