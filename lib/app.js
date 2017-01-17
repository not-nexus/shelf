"use strict";

/**
 * The app that will start up a server and start listening.
 *
 * @param {bluebird} bluebird
 * @param {shelf~config} config
 * @param {restiq} restiq
 * @return {shelf~app}
 */
module.exports = (bluebird, config, restiq) => {
    var appModule;

    /**
     * Starts listening on the port defined in the config.  If the port is
     * falsy, does not listen.
     *
     * @return {Promise.<this>}
     */
    function startServerAsync() {
        var restiqApp;

        restiqApp = restiq.createServer({
            restify: true
        });
        restiqApp.addRoute("GET", "/", (req, res, next) => {
            res.send(200, "ok");
            next();
        });

        if (!config.port) {
            return bluebird.resolve(appModule);
        }

        return bluebird.fromCallback((callback) => {
            restiqApp.listen(config.port, callback);
        }).then(() => {
            console.log(`server started on port ${config.port}`);
        });
    }


    /**
     * @typedef {Object} shelf~app
     * @property {Function} startServerAsync
     */
    appModule = {
        startServerAsync
    };

    return appModule;
};
