"use strict";
define('config', ['underscore', 'backbonekts'], function (_, BackboneKTS) {
    return _.extend(BackboneKTS.Config, {
        webRoot: '',
        apiURL: window.location.origin + '/api/',
        imgResizerUrl: window.location.origin + '/filter/',
        staticPrefix: '/',
        mediaPrefix: '/uploads/'
    });
});