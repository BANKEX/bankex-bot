"use strict";
define([], function () {
    var _loaded = {};

    function Loader(resourceUrl) {
        this.url = resourceUrl;
        return this;
    }

    Loader.prototype.load = function (callback) {
        var self = this;

        if (_loaded[self.url] !== undefined) {
            if (_loaded[self.url].loaded) {
                callback.call();
            } else {
                _loaded[self.url].callbacks.push(callback);
            }
        } else {
            _loaded[self.url] = {
                loaded: false,
                callbacks: [callback]
            };

            var script = document.createElement('script');
            script.src = self.url;
            script.async = true;
            script.onload = function () {
                _loaded[self.url].loaded = true;
                var callbacks = _loaded[self.url].callbacks;
                for (var i in callbacks) {
                    callbacks[i].call();
                }
            };

            script.setAttribute("data-external", true);
            document.body.appendChild(script);
        }
    };

    return function (resourceUrl) {
        return new Loader(resourceUrl);
    };
});