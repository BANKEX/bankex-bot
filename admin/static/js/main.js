require.config({
    paths: {
        text: '../bower_components/requirejs-text/text',
        bootstrap: '../bower_components/bootstrap/dist/js/bootstrap',
        backbone: '../bower_components/backbone/backbone',
        backbonekts: '../bower_components/backbonekts/dist/backbonekts',
        underscore: '../bower_components/underscore/underscore',
        jquery: '../bower_components/jquery/dist/jquery',
        notific: '../bower_components/notific/dist/notific',
        moment: '../bower_components/moment/moment',
        autocomplete: '../bower_components/devbridge-autocomplete/dist/jquery.autocomplete',

        config: './config',
        router: './router',

        helpers: './helpers',

        base: './base',
        views: './views',
        data: './data',
        templates: './templates'
    },
    urlArgs: "nonce=" + (new Date()).getTime(),
    shim: {
        bootstrap: ['jquery']
    },
    config: {
        text: {
            useXhr: function (url, protocol, hostname, port) {
                return true;
            }
        }
    }
});

require(['router', 'bootstrap'], function (App) {
    (new App()).start();
});