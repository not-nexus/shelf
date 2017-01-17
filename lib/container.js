"use strict";

/* Prepare the container.
 *
 * This module must be synchronous.
 */

var container, Dizzy;

// Load necessary modules to get the container started.
Dizzy = require("dizzy");

// Prepare the container and register itself for further injection.
container = new Dizzy();
container.registerBulk({
    container
});

// Our modules
container.registerBulk({
    app: "./app",
    bootstrap: "./bootstrap",
    config: "./config"
}).fromModule(__dirname).asFactory().cached();

// Load necessary 3rd-party modules into the container.
container.registerBulk({
    bluebird: "bluebird",
    restiq: "restiq"
}).fromModule();


/**
 * Container for dependency injection.
 *
 * @typedef {Dizzy} {shelf~container}
 */
module.exports = container;
