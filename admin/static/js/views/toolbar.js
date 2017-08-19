"use strict";
define([
    'backbonekts',
    'underscore',
    'backbone',
    'text!templates/toolbar/index.html'
], function (BackboneKTS, _, Backbone, toolbarTemplate) {
    return BackboneKTS.View.extend({
        el: '#toolbar',
        rendered: false,
        toolbarTemplate: _.template(toolbarTemplate),
        render: function () {
            this.$el.html(this.toolbarTemplate({user: config.user}));
            this.rendered = true;

            var onLocationChange = function () {
                var menuItems, selectMenu;
                menuItems = $('.navbar__item');
                menuItems.removeClass('active');
                selectMenu = $('.navbar__link[href="' + window.location.pathname + '"]');
                if (selectMenu.length !== 0) {
                    selectMenu.parent().addClass('active');
                }
            };
            onLocationChange();
            Backbone.history.on("all", onLocationChange);
        }
    });
});