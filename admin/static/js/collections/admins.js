"use strict";
define(['backbonekts', 'models/admin'], function (BackboneKTS, Admin) {
    return BackboneKTS.Collection.extend({
        model: Admin,
        url: function () {
            return config.getMethodUrl('admin.get', {
                offset: this.offset,
                count: this.pageSize
            });
        }
    });
});