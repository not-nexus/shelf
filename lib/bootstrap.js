"use strict";

/**
 * Bootstrap the application.
 *
 * Load configuration, parse files, validation.
 *
 * @param {bluebird} bluebird
 * @param {shelf~container} container
 * @return {shelf~bootstrap}
 */
module.exports = (bluebird, container) => {
    /**
     * Load all of the modules
     *
     * @param {shelf~config} [config]
     * @return {Promise.<shelf~app>}
     */
    function bootstrapAsync(config) {
        var promise;

        if (config && typeof config === "object") {
            promise = container.resolveAsync("config").then((defaultConfig) => {
                // Still may need to process and verify the configuration.
                Object.assign(defaultConfig, config);
            });
        } else {
            promise = bluebird.resolve();
        }

        return promise.then(() => {
            return container.resolveAsync("app").then((app) => {
                return app.startServerAsync();
            });
        });
    }


    /**
     * @typedef {Object} shelf~bootstrap
     * @property {Function} bootstrapAsync
     */
    return {
        bootstrapAsync
    };
};
