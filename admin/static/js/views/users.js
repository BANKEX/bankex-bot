"use strict";
define([
    'backbonekts', 'underscore', 'jquery',
    'text!templates/users/index.html',
    'collections/users'
], function (BackboneKTS, _, $, indexTemplate, UsersCollection) {
    return BackboneKTS.View.extend({
        indexTemplate: _.template(indexTemplate),
        events: {
            'click .pagination__item.pagination__item_users': 'pagination'
        },
        actionIndex: function (offset) {
            var self = this;
            if (offset === null) {
                offset = 0;
            }
            var currencyCollection = new UsersCollection();
            currencyCollection.fetch({
                data: {offset: offset},
                success: function () {
                    self.$el.html(self.indexTemplate({
                        offset: offset,
                        count: currencyCollection.totalCount,
                        items: currencyCollection
                    }));
                }
            });
        },
        pagination: function (e) {
            var self = this,
                offset = $(e.currentTarget).attr('data-offset');
            e.preventDefault();
            self.actionIndex(offset);
        }
    });
});