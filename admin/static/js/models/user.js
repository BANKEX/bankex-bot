"use strict";
define(['backbonekts', 'moment'], function (BackboneKTS, moment) {
    return BackboneKTS.Model.extend({
        url: function () {
            return config.getMethodUrl('users.get');
        },
        get: function (key) {
            var value = BackboneKTS.Model.prototype.get.call(this, key);
            if (key === 'update_date' && value) {
                value = moment(value * 1000).format('DD.MM.YYYY в HH:mm');
            }
            return value;
        }
    });
});