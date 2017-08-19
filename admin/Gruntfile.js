"use strict";
module.exports = function (grunt) {
    require('load-grunt-tasks')(grunt);
    require('time-grunt')(grunt);

    var debug = false;

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        requirejs: {
            front: {
                options: {
                    baseUrl: 'static/js',
                    name: 'main',
                    optimize: debug ? "none" : "uglify",
                    mainConfigFile: 'static/js/main.js',
                    out: 'public/static/js/dist.js',
                    paths: {
                        requireLib: '../bower_components/almond/almond'
                    },
                    include: ['requireLib']
                }
            }
        },
        copy: {
            main: {
                files: [
                    {
                        src: ['index.html'],
                        dest: 'public/'
                    },
                    {
                        expand: true,
                        src: ['static/img/*.{png,svg,jpg,jpeg,gif}'],
                        dest: 'public/'
                    }
                ]
            },
            fonts: {
                files: [
                    {
                        src: ['static/css/fonts/*.{eot,svg,ttf,woff}'],
                        dest: 'public/'
                    },
                    {
                        expand: true,
                        cwd: 'static/bower_components/bootstrap',
                        src: ['fonts/*.{eot,svg,ttf,woff}'],
                        dest: 'public/static/'
                    },
                    {
                        expand: true,
                        cwd: 'static/bower_components/font-awesome',
                        src: ['font/*.{eot,svg,ttf,woff}'],
                        dest: 'public/static/'
                    }
                ]
            },
            svg: {
                files: [
                    {
                        src: ['static/img/css/sprite.css'],
                        dest: 'static/css/svg-images.css'
                    },
                    {
                        src: ['static/img/css/svg-images.svg'],
                        dest: 'static/img/svg-images.svg'
                    }
                ]
            },
            public: {
                files: [
                    {
                        expand: true,
                        src: ['public/**/*'],
                        dest: '../'
                    }
                ]
            }
        },
        useminPrepare: {
            html: [
                'index.html'
            ],
            options: {
                dest: './public',
                root: './'
            }
        },
        processhtml: {
            dist: {
                files: {
                    'public/index.html': ['public/index.html']
                }
            }
        },
        postcss: {
            options: {
                processors: [
                    require('autoprefixer')({
                        browsers: ['> 1%', 'last 50 versions', 'Firefox ESR', 'Opera 12.1']
                    })
                ]
            },
            dist: {
                files: [{
                    expand: true,
                    cwd: 'static/css',
                    src: '**/*.css',
                    dest: 'static/css'
                }]
            }
        },
        replace: {
            svg_css: {
                src: ['static/css/svg-images.css'],
                overwrite: true,
                replacements: [
                    {from: 'svg-images.svg', to: '../img/svg-images.svg'}
                ]
            },
            svg: {
                src: ['static/img/svg-images/*.svg'],
                overwrite: true,
                replacements: [
                    {from: /<!--.+?-->/g, to: ''},
                    {from: /<title>.+?<\/title>/g, to: ''},
                    {from: /<desc>.+?<\/desc>/g, to: ''},
                    {from: /(sketch:type=".+?)"/g, to: ''},
                    {from: /<use xlink:href="#a"\/>/g, to: ''},
                    {from: /xlink:href="#a"/g, to: ''},
                    {from: ' xmlns:sketch="http://www.bohemiancoding.com/sketch/ns"', to: ''},
                    {from: '<defs></defs>', to: ''},
                    {from: ' >', to: '>'},
                    {from: ' ">', to: '">'},
                    {from: /^(\s)+$/gm, to: ''}
                ]
            }
        },
        svg_sprite: {
            icons: {
                options: {
                    shape: {
                        spacing: {
                            padding: 5
                        }
                    },
                    mode: {
                        css: {
                            prefix: '.image_',
                            bust: false,
                            sprite: "svg-images.svg",
                            common: 'image',
                            dimensions: true,
                            render: {
                                css: true
                            }
                        }
                    }
                },
                expand: true,
                cwd: 'static/img/svg-images',
                src: ['*.svg'],
                dest: 'static/img'
            }
        },
        csscomb: {
            pretty: {
                options: {
                    config: '.csscomb.json'
                },
                expand: true,
                cwd: 'static/css',
                dest: 'static/css',
                src: ['**/*.css', '!css/fonts.css']
            }
        },
        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            hint: {
                files: {
                    src: ['Gruntfile.js', 'js/**/*.js']
                }
            }
        },
        clean: {
            svg: {
                src: ['static/img/css']
            },
            reset: {
                options: {
                    force: true
                },
                src: ["public/**/*", "../public/**/*"]
            },
            cleanup: {
                src: [".tmp"]
            }
        },
        htmlmin: {
            dist: {
                options: {
                    removeComments: true,
                    collapseWhitespace: true
                },
                files: [{
                    expand: true,
                    cwd: 'public/',
                    src: 'index.html',
                    dest: 'public/'
                }]
            }
        },
        usemin: {
            html: ['public/index.html'],
            css: ['public/static/css/*.css'],
            js: ['public/static/js/*.js'],
            options: {
                dirs: ['public/static'],
                basedir: 'public',
                assetsDir: ['public']
            }
        },
        filerev: {
            dist: {
                src: [
                    'public/static/js/**/*.js',
                    'public/static/css/**/*.css',
                    'public/static/fonts/**/*.css',
                    'public/static/img/**.svg'
                ]
            }
        }
    });

    grunt.registerTask('prettyCss', ['postcss', 'csscomb']);

    grunt.registerTask('buildSvg', ['replace:svg', 'svg_sprite', 'copy:svg', 'replace:svg_css', 'clean:svg']);
    grunt.registerTask('buildCss', ['prettyCss', 'useminPrepare', 'concat', 'cssmin']);
    grunt.registerTask('buildJs', ['requirejs:front']);

    grunt.registerTask('buildHtml', ['copy', 'processhtml', 'filerev', 'usemin', 'htmlmin']);


    grunt.registerTask('default', [
        'clean:reset',

        'buildSvg',
        'buildCss',
        'buildJs',

        'buildHtml',

        'copy:public',
        'clean:cleanup'
    ]);
};