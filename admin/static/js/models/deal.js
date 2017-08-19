"use strict";
define(['backbonekts', 'moment'], function (BackboneKTS, moment) {
    return BackboneKTS.Model.extend({
        url: function () {
            return config.getMethodUrl('deals.get');
        },
        _get: function (key) {
            return BackboneKTS.Model.prototype.get.call(this, key)
        },
        get: function (key) {
            var value = BackboneKTS.Model.prototype.get.call(this, key);
            if (key === 'creation_date') {
                value = moment(value * 1000).format('DD.MM.YYYY в HH:mm');
            }
            if (key === 'user' || key === 'salesman' || key === 'offer') {
                value = value || {};
            }
            return value;
        }
    });
});