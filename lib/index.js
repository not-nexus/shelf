"use strict";

/**
 * The main exported library.
 *
 * This module must be synchronous.
 */

var container;

container = require("./container");


/**
 * @typedef {Object} shelf
 * @property {Function} appAsync
 * @property {shelf~container} container
 */
module.exports = {
    /**
     * Create an app, start the server.
     *
     * @param {shelf~config} [config]
     * @return {Promise.<shelf~app>}
     */
    appAsync: (config) => {
        return container.resolveAsync("bootstrap").then((bootstrap) => {
            return bootstrap.bootstrapAsync(config);
        });
    },
    container
};
