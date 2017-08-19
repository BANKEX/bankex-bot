"use strict";
define(['backbonekts', 'models/offer'], function (BackboneKTS, Offer) {
    return BackboneKTS.Collection.extend({
        model: Offer,
        url: function () {
            return config.getMethodUrl('offers.get', {
                offset: this.offset,
                count: this.pageSize
            });
        }
    });
});