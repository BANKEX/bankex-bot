"use strict";
define(['backbonekts', 'models/deal'], function (BackboneKTS, Deal) {
    return BackboneKTS.Collection.extend({
        model: Deal,
        url: function () {
            return config.getMethodUrl('deals.get', {
                offset: this.offset,
                count: this.pageSize
            });
        }
    });
});