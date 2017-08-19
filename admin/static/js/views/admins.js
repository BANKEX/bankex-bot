"use strict";
define([
    'backbonekts', 'underscore', 'jquery',
    'text!templates/admins/index.html',
    'text!templates/admins/form.html',
    'collections/admins', 'models/admin'
], function (BackboneKTS, _, $, indexTemplate, formTemplate, AdminsCollection, Admin) {
    return BackboneKTS.View.extend({
        indexTemplate: _.template(indexTemplate),
        formTemplate: _.template(formTemplate),
        events: {
            'click .pagination__item.pagination__item_admins': 'pagination',
            'submit .js-corp-form': 'formSubmit',
            'click .js-admin-remove': 'removeAdmin'
        },
        actionIndex: function (offset) {
            var self = this;
            if (offset === null) {
                offset = 0;
            }
            var adminCollection = new AdminsCollection();
            adminCollection.fetch({
                data: {
                    offset: offset
                },
                success: function () {
                    self.$el.html(self.indexTemplate({
                        offset: offset,
                        count: adminCollection.totalCount,
                        users: adminCollection
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
                    item: item
                }));
            }

            if (id !== undefined) {
                var admin = new Admin({id: id});
                admin.fetch({
                    success: function () {
                        render(admin);
                    }
                });
            } else {
                render(new Admin());
            }
        },
        formSubmit: function (evt) {
            var self = this,
                data = self.serializeForm(evt.currentTarget);
            evt.preventDefault();

            var admin = new Admin();
            admin.save(data, {
                url: config.getMethodUrl('admin.save'),
                success: function () {
                    if (data.id) {
                        self._showSuccess('Успех', 'Администратор успешно сохранен');
                    }
                    self.redirect('admins');
                },
                error: function (object, response) {
                    self._showError(response);
                }
            });
        },
        removeAdmin: function (e) {
            e.preventDefault();
            var id = $(e.currentTarget).attr('data-id');
            var self = this;
            if (confirm('Вы уверены?')) {
                $.ajax({
                    method: 'post',
                    url: config.getMethodUrl('admin.delete', {id: id}),
                    success: function () {
                        self._showSuccess('Успех', 'Администратор удален');
                        $('.js-admin-row[data-id="' + id + '"]').remove();
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