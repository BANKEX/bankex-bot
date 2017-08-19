"use strict";
define([
    'backbonekts', 'underscore', 'jquery',
    'text!templates/deals/index.html', 'collections/deals'
], function (BackboneKTS, _, $, indexTemplate, DealsCollection) {
    return BackboneKTS.View.extend({
        indexTemplate: _.template(indexTemplate),
        events: {
            'click .pagination__item.pagination__item_deals': 'pagination',
            'click .js-deal-remove': 'removeDeal'
        },
        actionIndex: function (offset) {
            var self = this;
            if (offset === null) {
                offset = 0;
            }
            var dealsCollection = new DealsCollection();
            dealsCollection.fetch({
                data: {
                    offset: offset
                },
                success: function () {

                    self.$el.html(self.indexTemplate({
                        offset: offset,
                        count: dealsCollection.totalCount,
                        users: dealsCollection
                    }));
                }
            });
        },
        removeDeal: function (e) {
            e.preventDefault();
            var id = $(e.currentTarget).attr('data-id');
            var self = this;
            if (confirm('Вы уверены?')) {
                $.ajax({
                    method: 'post',
                    url: config.getMethodUrl('deals.delete', {id: id}),
                    success: function () {
                        self._showSuccess('Успех', 'Предложение удалено');
                        $('.js-deal-row[data-id="' + id + '"]').remove();
                    }
                });
            }
        },
        pagination: function (e) {
            var self = this,
                offset = $(e.currentTarget).attr('data-offset');
            e.preventDefault();
            self.actionIndex(offset);
        }
    });
});