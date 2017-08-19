"use strict";
define([
    'config', 'backbonekts', 'backbone', 'jquery', 'underscore',
    'models/admin',
    'views/login',
    'views/main', 'views/toolbar', 'views/admins', 'views/texts',
    'views/users', 'views/offers', 'views/deals'
], function (Config, BackboneKTS, Backbone, $, _, Admin,
             LoginView, MainView, ToolbarView, AdminsView, TextsView, UsersView, OffersView, DealsView) {
    return BackboneKTS.Router.extend({
        routes: {
            "offers/(:action)/(:id)": "offersPage",
            "offers/(:action)": "offersPage",
            "offers": "offersPage",

            "deals/(:action)/(:id)": "dealsPage",
            "deals/(:action)": "dealsPage",
            "deals": "dealsPage",

            "users": "usersPage",

            // service
            "texts": "textsPage",
            "texts/(:action)/(:id)": "textsPage",
            "texts/(:action)": "textsPage",

            "admins/(:action)/(:id)": "adminsPage",
            "admins/(:action)": "adminsPage",
            "admins": "adminsPage",

            "login": "loginPage",
            "": "mainPage",
            '*default': 'mainPage'
        },
        views: {
            'login': LoginView,
            'main': MainView,
            'toolbar': ToolbarView,
            'admins': AdminsView,
            'texts': TextsView,
            'users': UsersView,
            'offers': OffersView,
            'deals': DealsView
        },
        initialize: function () {
            window.config = Config;
            config.user = false;
        },
        start: function () {
            var self = this;
            $(document).delegate("a", "click", function (evt) {
                var event = evt.originalEvent;
                if (event.metaKey || event.ctrlKey) {
                    return true;
                }

                var href = $(this).attr("href");
                if ($(evt.currentTarget).prop('target') === '_blank') {
                    return true;
                }

                if (href === undefined) {
                    href = '';
                }

                if (href === '/logout') {
                    $.ajax({
                        method: 'post',
                        url: config.getMethodUrl('logout'),
                        complete: function () {
                            window.location.pathname = '/login';
                        }
                    });
                    return false;
                }
                var protocol = document.location.protocol + "//";
                if (href.slice(0, protocol.length) !== protocol && href.substring(0, 1) !== '#') {
                    evt.preventDefault();
                    Backbone.history.navigate(href, true);
                }
            });

            var initHistory = function () {
                Backbone.history.start({pushState: true, root: '/'});
                Backbone.history.on("all", function () {
                    if (config.user !== false && self._getViewByName('toolbar').rendered === false) {
                        self._getViewByName('toolbar').render();
                    }
                });
            };

            var admin = new Admin();
            admin.fetch({
                url: config.getMethodUrl('admin.info'),
                success: function () {
                    config.user = admin;
                    initHistory();
                    if (Backbone.history.fragment === 'login') {
                        self.redirect('');
                    }
                    self._getViewByName('toolbar').render();
                },
                error: function () {
                    initHistory();
                    self.redirect('login');
                }
            });
        },
        mainPage: function () {
            if (config.user === false) {
                return false;
            }
            this.redirect('offers');
        },
        loginPage: function (action) {
            this._getViewByName('login').render(action);
        },
        offersPage: function (action, id) {
            if (config.user === false) {
                return false;
            }
            this._getViewByName('offers').render(action, id);
        },
        dealsPage: function (action, id) {
            if (config.user === false) {
                return false;
            }
            this._getViewByName('deals').render(action, id);
        },
        usersPage: function (action, id) {
            if (config.user === false) {
                return false;
            }
            this._getViewByName('users').render(action, id);
        },
        adminsPage: function (action, id) {
            if (config.user === false) {
                return false;
            }
            this._getViewByName('admins').render(action, id);
        },
        textsPage: function (action, id) {
            if (config.user === false) {
                return false;
            }
            this._getViewByName('texts').render(action, id);
        }
    });
});