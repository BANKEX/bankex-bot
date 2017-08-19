"use strict";
define([
    'backbonekts', 'underscore', 'jquery',
    'text!templates/texts/index.html',
    'text!templates/texts/form.html',
    'collections/texts', 'models/text'
], function (BackboneKTS, _, $, indexTemplate, formTemplate, TextsCollection, Text) {
    return BackboneKTS.View.extend({
        indexTemplate: _.template(indexTemplate),
        formTemplate: _.template(formTemplate),
        events: {
            'submit .js-text-form': 'formSubmit',
            'click .js-text-remove': 'remove'
        },
        actionIndex: function (offset) {
            var self = this;
            if (offset === null) {
                offset = 0;
            }
            var textsCollection = new TextsCollection();
            textsCollection.fetch({
                data: {
                    offset: offset,
                    limit: 100500
                },
                success: function () {
                    self.$el.html(self.indexTemplate({
                        offset: offset,
                        count: textsCollection.totalCount,
                        items: textsCollection
                    }));
                }
            });
        },
        actionAdd: function () {
            this._actionPut();
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

                config.apiCall('texts.keys', {}, {
                    onSuccess: function (data) {
                        var keys = $('.js-keys');

                        for (var i in data.data) {
                            var item = data.data[i];
                            var option = $('<option/>', {
                                html: item,
                                value: item
                            });
                            
                            if (keys.attr('data-value') == item) {
                                option.prop('selected', true)
                            }

                            keys.append(option);
                        }
                    }
                });
            }

            if (id !== undefined) {
                var currency = new Text({id: id});
                currency.fetch({
                    success: function () {
                        render(currency);
                    }
                });
            } else {
                render(new Text());
            }
        },
        formSubmit: function (evt) {
            var self = this,
                data = self.serializeForm(evt.currentTarget);
            evt.preventDefault();

            var currency = new Text();
            currency.save(data, {
                url: config.getMethodUrl('texts.save'),
                success: function () {
                    if (data.id) {
                        self._showSuccess('Успех', 'Текст успешно сохранен');
                    }
                    self.redirect('texts');
                },
                error: function (object, response) {
                    if (response.responseJSON.status === 'internal_error') {
                        self._showError(undefined, 'Запись уже существует');
                    } else {
                        self._showError(undefined, response.responseJSON.message);
                    }
                }
            });
        },
        remove: function (e) {
            e.preventDefault();
            var id = $(e.currentTarget).attr('data-id');
            var self = this;
            if (confirm('Вы уверены?')) {
                $.ajax({
                    method: 'post',
                    url: config.getMethodUrl('texts.delete', {id: id}),
                    success: function () {
                        self._showSuccess('Успех', 'Текст удален');
                        $('.js-row[data-id="' + id + '"]').remove();
                    }
                });
            }
        }
    });
});