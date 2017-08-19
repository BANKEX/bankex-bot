"use strict";
define(['backbonekts', 'models/user'], function (BackboneKTS, User) {
    return BackboneKTS.Collection.extend({
        model: User,
        url: function () {
            return config.getMethodUrl('users.get', {
                offset: this.offset,
                count: this.pageSize
            });
        }
    });
});