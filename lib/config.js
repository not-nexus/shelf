"use strict";

/**
 * Default configuration for Shelf.
 *
 * Uses the factory pattern to be consistent.
 *
 * @return {shelf~config}
 */
module.exports = () => {
    /**
     * @typedef {Object} shelf~config
     * @property {number} [port]
     */
    return {
        port: 8080
    };
};
