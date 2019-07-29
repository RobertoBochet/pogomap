/*jshint esversion: 6 */
import {Enviroment} from "./modules/Enviroment.mjs";

let env = null;

(() => {
    "use strict";

    // Waiting the loading of the google maps library
    let int = setInterval(() => {
        if (typeof google !== 'object' || typeof google.maps !== 'object') return;
        clearInterval(int);
        env = new Enviroment();
    }, 100);
})();
