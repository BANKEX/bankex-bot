"use strict";
define(['backbonekts', 'models/text'], function (BackboneKTS, Text) {
    return BackboneKTS.Collection.extend({
        model: Text,
        url: function () {
            return config.getMethodUrl('texts.get', {
                offset: this.offset,
                count: 100500
            });
        }
    });
});