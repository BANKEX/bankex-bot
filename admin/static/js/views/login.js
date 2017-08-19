"use strict";
define([
    'backbonekts',
    'underscore',
    'models/admin',
    'text!templates/login/index.html'
], function (BackboneKTS, _, Admin, loginTemplate) {
    return BackboneKTS.View.extend({
        loginTemplate: _.template(loginTemplate),
        events: {
            'submit .js-login-form': 'loginSubmit'
        },
        actionIndex: function () {
            this.$el.html(this.loginTemplate());
        },
        loginSubmit: function (evt) {
            evt.preventDefault();
            var self = this,
                data = {
                    email: self.$('.js-login-form__email').val(),
                    password: self.$('.js-login-form__password').val()
                };

            config.apiCall('admin.auth', data, {
                method: 'POST',
                onSuccess: function () {
                    var user = new Admin();
                    user.fetch({
                        url: config.getMethodUrl('admin.info'),
                        success: function () {
                            config.user = user;
                            self.redirect('');
                        },
                        error: function (response, xhr) {
                            var data = xhr.responseJSON;
                            if (data) {
                                self._showError(data.status);
                            } else {
                                self._showError(data);
                            }
                        }
                    });
                },
                onError: function (response, xhr) {
                    var data = response.responseJSON;
                    if (data) {
                        self._showError(response.status);
                    } else {
                        self._showError(response);
                    }
                }
            });

        }
    });
});