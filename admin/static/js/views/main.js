"use strict";
define([
    'backbonekts',
    'jquery',
    'underscore',
    'text!templates/main/index.html'
], function (BackboneKTS, $, _, mainTemplate) {
    return BackboneKTS.View.extend({
        mainTemplate: _.template(mainTemplate),
        actionIndex: function () {
            var self = this;
            self.$el.html(this.mainTemplate());
        }
    });
});