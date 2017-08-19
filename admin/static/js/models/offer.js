"use strict";
define(['backbonekts', 'moment'], function (BackboneKTS, moment) {
    return BackboneKTS.Model.extend({
        url: function () {
            return config.getMethodUrl('offers.get');
        },
        _get: function (key) {
            return BackboneKTS.Model.prototype.get.call(this, key)
        },
        get: function (key) {
            var value = this._get(key);
            if (key === 'creation_date') {
                value = moment(value * 1000).format('DD.MM.YYYY в HH:mm');
            } else if (key === 'salesman') {
                value = value || {};
            } else if (key === 'type_title') {
                value = this._get('type');
                switch (value) {
                    case 'credit':
                        return 'Кредит';
                    case 'futures':
                        return 'Фьючерс';
                    case 'factoring':
                        return 'Факторинг';
                }
            }
            return value;
        }
    });
});