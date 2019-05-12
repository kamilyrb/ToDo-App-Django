/**
 *
 * Core functions
 *
 */
var App = function () {
    // Global AJAX setup
    var handleAjaxSetup = function () {
        // CSRF Token
        var csrftoken = App.getCookie('csrftoken');
        $.ajaxSetup({
            cache: false,
            abortOnRetry: true,
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
        // Current requests
        var currentRequests = {};
        // Filter requests
        $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
            if (options.abortOnRetry) {
                if (currentRequests[options.url]) {
                    currentRequests[options.url].abort();
                }
                currentRequests[options.url] = jqXHR;
            }
        });
        $(document).ajaxStart(function () {
            // App.startPageLoading({
            //     animate: true
            // });
        }).ajaxStop(function () {
            // App.stopPageLoading();
        }).ajaxError(function (jqXHR, textStatus) {
            if (textStatus.status === 403)
                window.location = '/system/error';
            else if (textStatus.statusText !== 'abort') {
                App.alert('An ajax error occured');
            }
        }).ajaxSuccess(function (event, request, settings) {
            var login = settings.url.indexOf('/login') === 0 || settings.url.indexOf('/captcha/refresh') === 0;
            var authenticated = request.getResponseHeader('AUTHENTICATED') === 'true';
            if (!login && !authenticated) {
                window.location.reload();
            }
        });
    };
    // Handles custom checkboxes & radios using $ uniform plugin

    return {
        //main function to initiate the theme
        init: function () {
            // signature
            console.log('%cTo Do Web Application', 'padding:8px 35px; color:#fff; background-color:#2B3643; line-height:25px;');
            handleAjaxSetup(); // AJAX setup
            this.initPlugins();
        },
        //main function to initiate core javascript after ajax complete
        initPlugins: function () {
        },
        // get cookie
        getCookie: function (name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        // wrapper function to scroll(focus) to an element
        scrollTo: function (el, offeset) {
            var pos = (el && el.length > 0) ? el.offset().top : 0;
            if (el) {
                if ($('body').hasClass('page-header-fixed')) {
                    pos = pos - $('.page-header').height();
                } else if ($('body').hasClass('page-header-top-fixed')) {
                    pos = pos - $('.page-header-top').height();
                } else if ($('body').hasClass('page-header-menu-fixed')) {
                    pos = pos - $('.page-header-menu').height();
                }
                pos = pos + (offeset ? offeset : -1 * el.height());
            }
            $('html, body').animate({
                scrollTop: pos
            }, 'slow');
        },
        // function to scroll to the top
        scrollTop: function () {
            App.scrollTo();
        },
        alert: function (message, icon, title = "Error") {
            icon = icon || 'error';
            if ($.inArray(icon, ['success', 'warning', 'error', 'info']) < 0) {
                type = 'info'
            }
            swal({
                title: title,
                text: message,
                // html: message,
                reverseButtons: !0,
            });
        },
        confirm: function (message, confirm, decline, icon) {
            swal({
                title: 'Attention',
                text: message,
                reverseButtons: !0,
                buttons: [
                    'No',
                    'Yes'
                ],
            }).then(function (e) {
                if (e != null && confirm) {
                    confirm();
                } else if (decline) {
                    decline();
                }
            });
        },
        notify: function (message, type, title) {
            type = type || 'success';
            if ($.inArray(type, ['success', 'warning', 'error', 'info']) < 0) {
                type = 'info';
            }
            toastr[type](message, (title || 'Process Result'));
        },
        alertBox: function (options) {
            options = $.extend(true, {
                container: '', // alerts parent container(by default placed after the page breadcrumbs)
                place: 'append', // 'append' or 'prepend' in container
                type: 'success', // alert's type
                message: '', // alert's message
                close: true, // make alert closable
                reset: true, // close all previous alerts first
                focus: true, // auto scroll to the alert after shown
                closeInSeconds: 0, // auto close after defined seconds
                icon: '' // put icon before the message
            }, options);
            var id = App.getUniqueID('alert');
            var html = '<div id="' + id + '" class="custom-alerts alert alert-' + options.type + ' fade in">' + (options.close ? '<button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>' : '') + (options.icon !== "" ? '<i class="fa-lg fa fa-' + options.icon + '"></i>  ' : '') + options.message + '</div>';
            if (options.reset) {
                $('.custom-alerts').remove();
            }
            if (!options.container) {
                if ($('.page-fixed-main-content').length === 1) {
                    $('.page-fixed-main-content').prepend(html);
                } else if (($('body').hasClass("page-container-bg-solid") || $('body').hasClass("page-content-white")) && $('.page-head').length === 0) {
                    $('.page-title').after(html);
                } else {
                    if ($('.page-bar').length > 0) {
                        $('.page-bar').after(html);
                    } else {
                        $('.page-breadcrumb, .breadcrumbs').after(html);
                    }
                }
            } else {
                if (options.place === 'append') {
                    $(options.container).append(html);
                } else {
                    $(options.container).prepend(html);
                }
            }
            if (options.focus) {
                App.scrollTo($('#' + id));
            }
            if (options.closeInSeconds > 0) {
                setTimeout(function () {
                    $('#' + id).remove();
                }, options.closeInSeconds * 1000);
            }
            return id;
        },
        // Load files dynamically
        load: (function () {
            var _load = function (tag) {
                return function (url) {
                    // Get system version
                    var version = App.getCookie('app-version');
                    if (url && (url.indexOf('http') < 0) && version) {
                        // Add version number end of the file for preventing browser cache
                        url += '?v=' + version;
                    }
                    // Existing files
                    var files = {};
                    $(tag).each(function () {
                        var url;
                        if (tag === 'link') {
                            url = $(this).attr('href');
                        } else {
                            url = $(this).attr('src');
                        }
                        if (typeof files[url] === 'undefined') {
                            files[url] = this;
                        }
                    });
                    // This promise will be used by Promise.all to determine success or failure
                    return new Promise(function (resolve, reject) {
                        var el = document.createElement(tag), parent = 'body', attr = 'src', before;
                        if (typeof files[url] !== 'undefined') {
                            resolve(files[url]);
                        } else {
                            // Important success and error for the promise
                            el.onload = function () {
                                resolve(el);
                            };
                            el.onerror = function () {
                                reject('File not found: ' + url);
                            };
                            // Need to set different attributes depending on tag type
                            switch (tag) {
                                case 'script':
                                    el.type = 'text/javascript';
                                    el.async = true;
                                    before = document.querySelector('script[src^="/assets/js"]');
                                    break;
                                case 'link':
                                    el.type = 'text/css';
                                    el.rel = 'stylesheet';
                                    attr = 'href';
                                    parent = 'head';
                                    before = document.querySelector('link[href^="/assets/css"]');
                                    break;
                                case 'img':
                                    el.alt = '';
                            }
                            // Inject into document to kick off loading
                            el[attr] = url;
                            if (before) {
                                document[parent].insertBefore(el, before);
                            } else {
                                document[parent].appendChild(el);
                            }
                        }
                    });
                };
            };
            return {
                css: _load('link'),
                js: _load('script'),
                img: _load('img')
            }
        })(),
        // load multiple files dynamically
        loadFiles: function (srcs, callback) {
            if ($.isArray(srcs) && srcs.length) {
                var loads = [];
                srcs.forEach(function (src) {
                    var type = src.substr(src.lastIndexOf('.') + 1);
                    switch (type) {
                        case 'js':
                            loads.push(App.load.js(src));
                            break;
                        case 'css':
                            loads.push(App.load.css(src));
                            break;
                        case 'img':
                            loads.push(App.load.img(src));
                            break;
                    }
                });
                Promise.all(loads).then(callback).catch(function (e) {
                    console.log('Load error: ' + e.stack);
                });
            }
        },

        getUniqueID: function (prefix) {
            return prefix + '-' + Math.floor(Math.random() * (new Date()).getTime());
        },

        openWindow: function (url, action) {
            var popup;
            if (action === 'print') {
                popup = window.open(url, '', 'width=700,height=500', true);
                popup.focus();
                popup.print();
            } else {
                popup = window.open(url, action);
            }
        },

        exportExcel: function (tbl, title, filename) {
            var uri = 'data:application/vnd.ms-excel;base64,'
                ,
                template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><meta http-equiv="content-type" content="application/vnd.ms-excel; charset=UTF-8"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
                , base64 = function (s) {
                    return window.btoa(unescape(encodeURIComponent(s)))
                }
                , format = function (s, c) {
                    return s.replace(/{(\w+)}/g, function (m, p) {
                        return c[p];
                    })
                };
            if (!tbl.nodeType)
                table = document.getElementById(tbl);
            var ctx = {worksheet: title || 'Worksheet', table: table.innerHTML};
            var link = document.createElement('a');
            link.download = filename || 'excel.xls';
            link.href = uri + base64(format(template, ctx));
            link.click();
        },
        datatable: {},

        modal: function (title, content, buttons) {
            var modal = $('<div/>').addClass('modal').append(
                $('<div/>').addClass('modal-dialog').append(
                    $('<div/>').addClass('modal-content').append(
                        $('<div/>').addClass('modal-header').append(
                            $('<h5/>').addClass('modal-title').html(title || 'Bilgiler'),
                            $('<button/>').click(function (e) {
                                e.preventDefault();
                                $(this).closest('.modal').modal('hide');
                            }).addClass('close').html('&times;'),
                        ),
                        $('<div/>').addClass('modal-body').append(content)
                    )
                )
            ).appendTo('body').on('shown.bs.modal', function () {
                //$(this).find('input[type="text"], textarea').not(':disabled').first().focus();
                window.setTimeout(function () {
                    App.initPlugins();
                }, 100);
            }).on('hidden.bs.modal', function () {
                $(this).next('.modal-backdrop').first().remove();
                $(this).remove();
            }).modal('show');
            if ($.isArray(buttons)) {
                var footer = $('<div/>').addClass('modal-footer').appendTo($('.modal-content', modal));
                buttons.forEach(function (button) {
                    button.appendTo(footer);
                });
            }
            return modal;
        },
        dialogForm: function (title, url, options) {
            // mApp.block($('body'), {});
            var buttons = '';
            var submitText = (options && options['submit-text']) ? options['submit-text'] : 'Save';
            if (options && options['hide-save-button']) {
                buttons = $('<div/>').addClass('modal-footer').append(
                    $('<button/>', {
                        'type': 'button',
                        'data-dismiss': 'modal'
                    }).addClass('btn btn-primary').text('Close')
                );
            } else {
                buttons = $('<div/>').addClass('modal-footer').append(
                    $('<button/>', {
                        'type': 'button',
                        'data-dismiss': 'modal'
                    }).addClass('btn btn-secondary').text('Close'),
                    $('<button/>', {
                        'type': 'submit'
                    }).addClass('btn btn-primary').text(submitText)
                );
            }
            $('<div/>').addClass('modal-body').load(url, function () {
                var modal = App.modal(title);
                modal.find('.modal-body').remove();
                if (options && options['large']) {
                    modal.find('.modal-dialog').addClass('modal-lg');
                } else if (options && options['small']) {
                    modal.find('.modal-dialog').addClass('modal-sm');
                }
                modal.find('.modal-content').append(
                    $('<form/>', {
                        'method': 'post',
                        'class': 'm-form m-form--state',
                        'action': url
                    }).append(
                        this,
                        buttons
                    ).submit(function (e) {
                        e.preventDefault();
                        var $this = $(this),
                            url = $this.attr('action'),
                            id = parseFloat($this.find('input[name="id"]').val()),
                            formData = new FormData(this);

                        if (id && url.substr(url.lastIndexOf('/') + 1) !== id.toString())
                            url = url + id.toString();
                        // mApp.block($this, {});
                        $.ajax({
                            'type': $this.attr('method'),
                            'url': url,
                            'cache': false,
                            'dataType': 'json',
                            'contentType': false,
                            'processData': false,
                            'data': formData
                        }).done(function (result) {
                            console.log("response", result);
                            // mApp.unblock($this);
                            if (result.success) {
                                if (result.info) {
                                    App.alert(result.message, 'info', 'Bilgilendirme');
                                } else {
                                    App.notify(result.message);
                                }
                                $this.closest('.modal').modal('hide');
                                App.reloadDataTables();
                                if (options && options['callback']) {
                                    eval(options['callback'] + '(result);');
                                }
                            } else {
                                App.alert(result.message);
                            }
                        }).fail(function (jqXHR, textStatus) {
                            // mApp.unblock($this);
                            App.alert('Server error generated.Please refresh page!');
                        });
                    })
                );
            });
        },
        reloadDataTables: function () {
            $.each(App.datatable, function (item) {
                App.datatable[item].getDataTable().ajax.reload();
            });
        },

        _fullHeight: function (className) {
            var winHeight = $(window).height();
            $(className).each(function () {
                var top = $(this).position().top + 50;
                $(this).height(winHeight - top);
            });
        },
    };
}();
$(document).ready(function () {
    App.init();
});

