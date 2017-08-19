"use strict";
define([
    'backbonekts', 'underscore', 'jquery',
    'text!templates/offers/index.html',
    'text!templates/offers/form.html',
    'collections/offers', 'models/offer'
], function (BackboneKTS, _, $, indexTemplate, formTemplate, OffersCollection, Offer) {
    return BackboneKTS.View.extend({
        indexTemplate: _.template(indexTemplate),
        formTemplate: _.template(formTemplate),
        events: {
            'click .pagination__item.pagination__item_offers': 'pagination',
            'submit .js-offer-form': 'formSubmit',
            'click .js-offer-remove': 'removeOffer'
        },
        actionIndex: function (offset) {
            var self = this;
            if (offset === null) {
                offset = 0;
            }
            var salesmenCollection = new OffersCollection();
            salesmenCollection.fetch({
                data: {
                    offset: offset
                },
                success: function () {
                    self.$el.html(self.indexTemplate({
                        offset: offset,
                        count: salesmenCollection.totalCount,
                        users: salesmenCollection
                    }));
                    $('[data-toggle="popover"]').popover({html: true});
                }
            });
        },
        actionEdit: function (id) {
            this._actionPut(id);
        },
        _actionPut: function (id) {
            var self = this;

            function render(item) {
                self.$el.html(self.formTemplate({
                    item: item,
                    self: self
                }));
            }

            if (id !== undefined) {
                var offer = new Offer({id: id});
                offer.fetch({
                    success: function () {
                        render(offer);
                    }
                });
            } else {
                render(new Offer());
            }
        },
        formSubmit: function (evt) {
            var self = this,
                data = self.serializeForm(evt.currentTarget);
            evt.preventDefault();

            var offer = new Offer();
            offer.save(data, {
                url: config.getMethodUrl('offers.save'),
                success: function () {
                    if (data.id) {
                        self._showSuccess('Успех', 'Предложение успешно сохранено');
                    }
                    self.redirect('offers');
                },
                error: function (object, response) {
                    self._showError(response);
                }
            });
        },
        removeOffer: function (e) {
            e.preventDefault();
            var id = $(e.currentTarget).attr('data-id');
            var self = this;
            if (confirm('Вы уверены?')) {
                config.apiCall('offers.delete', {id: id}, {
                    method: 'post',
                    onSuccess: function () {
                        self._showSuccess('Успех', 'Предложение удалено');
                        $('.js-offer-row[data-id="' + id + '"]').remove();
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