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
    var handleUniform = function () {
        if (!$().uniform) {
            return;
        }
        $('input:checkbox, input:radio, input:file').not('.make-switch').uniform();
        $('input:checkbox, input:radio').click(function () {
            $.uniform.update();
        });
    };
    // Handles Bootstrap switches
    var handleBootstrapSwitch = function () {
        if (!$().bootstrapSwitch) {
            return;
        }
        $('.make-switch').bootstrapSwitch();
    };
    // Handle Select2 Dropdowns
    var handleSelect2 = function () {
        if ($().select2) {
            $('.m-select2').select2({
                placeholder: 'Seçiniz',
                language: {
                    noResults: function () {
                        return 'Kayıt bulunamadı';
                    }
                },
                selectOnClose: true
            });
        }
    };
    var handleDatepicker = function () {
        var el = $('.date-picker');
        el.datepicker({
            autoclose: true,
            todayHighlight: true,
            todayBtn: 'linked',
            clearBtn: true,
        });
        el.attr('autocomplete', 'off');
        if (el.data('last-date')) {
            el.datepicker('setEndDate', el.data('last-date'));
        }
    };
    var handleTimepicker = function () {
        if ($().timepicker()) {
            $.fn.timepicker.defaults.language = $('html').attr('lang');
            $('.time-picker').timepicker({
                timeFormat: 'HH:mm',
                showMeridian: false
            });
        }
    };
    var handleDateTimepicker = function () {
        if ($().datetimepicker()) {
            $.fn.datetimepicker.defaults.language = $('html').attr('lang');
            $('.datetime-picker').datetimepicker({
                defaultDate: new Date(),
                format: 'DD/MM/YYYY HH:mm'
            });
        }
    };
    var handleColorpicker = function () {
        if ($().minicolors) {
            $('.color-picker').each(function () {
                $(this).minicolors({
                    control: $(this).attr('data-control') || 'hue',
                    defaultValue: $(this).attr('data-defaultValue') || '',
                    inline: $(this).attr('data-inline') === 'true',
                    letterCase: $(this).attr('data-letterCase') || 'lowercase',
                    opacity: $(this).attr('data-opacity'),
                    position: $(this).attr('data-position') || 'bottom left',
                    change: function (hex, opacity) {
                        if (!hex) return;
                        if (opacity) hex += ', ' + opacity;
                        //console.log(hex);
                    },
                    theme: 'bootstrap'
                });
            });
        }
    };
    var handleMultiselect = function () {
        if (jQuery().multiSelect) {
            $('.multi-select').multiSelect();
        }
        if (jQuery().multiselect) {
            $('.multiselect').multiselect({
                enableFiltering: true,
                includeSelectAllOption: true,
                selectAllText: 'Hepsini seç',
                nonSelectedText: 'Hiçbiri seçilmedi',
                allSelectedText: 'Hepsi seçildi',
                nSelectedText: "tanesi seçili",
                maxHeight: 300
            });
        }
    };
    // Currency
    var handleCurrency = function () {
        if ($().maskMoney) {
            $('[data-currency]').each(function () {
                $(this).maskMoney({
                    prefix: '₺ ',
                    allowNegative: ($(this).data('negative') || false),
                    thousands: '.',
                    decimal: ',',
                    affixesStay: true
                }).focus();
            });
        }
    };
    var handleInputmask = function () {
        $('input.mask-date').inputmask('dd.mm.yyyy', {'placeholder': '_'});
        $('input.mask-time').inputmask('hh:mm:ss', {'placeholder': '_'});
        $('input.mask-short-time').inputmask('hh:mm', {'placeholder': '_'});
        $('input.mask-phone').inputmask('99 999 999 9999', {'placeholder': '_'});
        $('input.mask-short-phone').inputmask('999 999 9999', {'placeholder': '_'});
        $('input.mask-currency').inputmask('currency', {
            groupSeparator: '.',
            prefix: '',
            radixPoint: ',',
            clearMaskOnLostFocus: true
        });
    };
    var handleMaxlength = function () {
        $('input[maxlength]').maxlength({
            warningClass: "m-badge m-badge--warning m-badge--rounded m-badge--wide",
            limitReachedClass: "m-badge m-badge--success m-badge--rounded m-badge--wide"
        });
    };
    var handleAutoComplete = function () {
        if ($().devbridgeAutocomplete) {
            $('.auto-complete').each(function () {
                var $this = $(this);
                var url = $this.data('url');
                var parent = $(this).data('parent');
                if (parent !== undefined) {
                    url = url.replace('0', $('#' + parent).val());
                }
                $this.devbridgeAutocomplete({
                    serviceUrl: url,
                    noCache: true,
                    minChars: $this.data('min-chars') || 1,
                    autoSelectFirst: true,
                    // groupBy: $this.data('group') || '',
                    appendTo: $this.data('append') || 'body',
                    forceFixPosition: true,
                    onSelect: function (suggestion) {
                        if ($this.data('target')) {
                            $($this.data('target')).val(suggestion.data.id);
                        }
                        if ($this.data('selected-url')) {
                            window.location = $this.data('selected-url').replace('{url}',
                                suggestion.data.url).replace('{id}', suggestion.data.id);
                        }
                        var callback = $this.data('callback');
                        var x = eval(callback);
                        if (typeof x === 'function') {
                            x($this, suggestion.data);
                        }
                    }
                });
            });
        }
    };
    // Bestupper
    var handleBestupper = function () {
        $('.bestupper').not('.bestupper-active').addClass('bestupper-active').bestupper({ln: 'tr'});
    };
    //* END:CORE HANDLERS *//
    return {
        //main function to initiate the theme
        init: function () {
            // signature
            console.log('%cTo Do Web Application', 'padding:8px 35px; color:#fff; background-color:#2B3643; line-height:25px;');
            // Moment set language
            // moment.locale($('html').attr('lang'));
            // var offset = moment($('body').attr('data-now')).valueOf() - Date.now();
            // moment.now = function () {
            //     return moment(Date.now() + offset);
            // };
            // Core handlers
            // handleInit(); // initialize core variables
            // handleOnResize(); // set and handle responsive
            handleAjaxSetup(); // AJAX setup
            this.initPlugins();
        },
        //main function to initiate core javascript after ajax complete
        initPlugins: function () {
            // UI Component handlers
            // handleUniform(); // handles custom icheck radio and checkboxes
            // handleBootstrapSwitch(); // handle bootstrap switch plugin
            //handleScrollers(); // handles slim scrolling contents
            // handleFancybox(); // handle fancy box
            // handleSelect2(); // handle custom Select2 dropdowns
            // handleMaxlength(); // handle custom Select2 dropdowns
            //handlePortletTools(); // handles portlet action bar functionality(refresh, configure, toggle, remove)
            //handleAlerts(); //handle closabled alerts
            //handleDropdowns(); // handle dropdowns
            //handleTabs(); // handle tabs
            //handleTooltips(); // handle bootstrap tooltips
            //handlePopovers(); // handles bootstrap popovers
            // handleAccordions(); //handles accordions
            // handleBootstrapConfirmation(); // handle bootstrap confirmations
            // handleTextareaAutosize(); // handle autosize textareas
            // handleCounterup(); // handle counterup instances
            // handleDatepicker(); // Datepicker
            // handleTimepicker(); // Timepicker
            // handleDateTimepicker(); // Datetimepicker
            // handleColorpicker();
            // handleInputmask();
            // handleAutoComplete();
            // handleBestupper();
            // handleMultiselect();
            // handleCurrency();
            //handleBootstrapSelect();
            // Hacks
            //handleFixInputPlaceholderForIE(); //IE8 & IE9 input placeholder issue fix
            // Handle group element heights
            // this.addResizeHandler(handleHeight); // handle auto calculating height on window resize
            // $('.modal[data-draggable]').draggable({
            //     handle: '.modal-header'
            // });
        },
        autoComplete: function () {
            handleAutoComplete();
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
                // text: message,
                html: message,
                type: icon,
                reverseButtons: !0,
                confirmButtonText: 'Ok',
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
        //public function to get a parameter by name from URL
        getURLParameter: function (paramName) {
            var searchString = window.location.search.substring(1),
                i, val, params = searchString.split('&');
            for (i = 0; i < params.length; i++) {
                val = params[i].split('=');
                if (val[0] === paramName) {
                    return unescape(val[1]);
                }
            }
            return null;
        },
        getUniqueID: function (prefix) {
            return prefix + '-' + Math.floor(Math.random() * (new Date()).getTime());
        },
        getFilterValues: function () {
            var filters = {};
            $('[name^="filter_"]', '#filter-form').each(function () {
                var key = $(this).attr('name'), val;
                switch ($(this).prop('tagName')) {
                    case 'INPUT':
                        if ($.inArray($(this).attr('type'), ['checkbox', 'radio']) > -1) {
                            if ($(this).is(':checked')) {
                                val = $(this).val();
                            }
                        } else {
                            val = $(this).val();
                        }
                        break;
                    case 'SELECT':
                        if ($(this).prop('multiple')) {
                            val = $(this).val().join(',');
                        } else {
                            val = $(this).val();
                        }
                        break;
                    default:
                        val = $(this).val();
                }
                if (val !== null && val.length) {
                    filters[key] = val;
                }
            });
            return filters;
        },
        resetForm: function (form) {
            $(form).find('input[type="hidden"], input[type="text"], input[type="email"], textarea').not('.no-reset').val('');
            $(form).find('select').each(function () {
                var that = $(this);
                that.removeData('value').val('');
                //that.find('option:first').prop('selected', true);
                that.change();
            });
            $(form).find('input[type="radio"]').first().prop('checked', true);
            $(form).find('input[type="checkbox"]').each(function () {
                $(this).prop('checked', $(this).attr('checked') === 'checked');
            });
            $(form).find('.fileinput').find('[data-dismiss]').click();
            App.destroyUIComponents();
        },
        // Set form field value
        setValue: function (name, value, form) {
            var inp = $('input[name="' + name + '"]', form);
            var sel = $('select[name="' + name + '"]', form);
            var txt = $('textarea[name="' + name + '"]', form);
            if (inp.length) {
                value = (/string|number|boolean/).test(typeof value) ? value.toString() : $.isArray(value) ? value : '';
                if (inp.is(':radio') || inp.is(':checkbox')) {
                    if ($.isArray(value)) {
                        inp.each(function () {
                            var current = $(this);
                            $.each(value, function (index, v) {
                                if (parseInt(current.val()) === parseInt(v)) {
                                    current.prop('checked', true);
                                }
                            });
                        });
                    } else if (value) {
                        inp.each(function () {
                            $(this).prop('checked', $(this).val() === value);
                        });
                    }
                } else {
                    inp.val(value);
                }
            } else if (sel.length) {
                if ($.isArray(value)) {
                    $.each(value, function (index, v) {
                        sel.find('> option[value="' + v + '"]').prop('selected', true).change();
                    });
                    sel.data('value', value.join(','));
                } else if (value !== null) {
                    sel.data('value', value.toString()).val(value.toString()).change();
                }
            } else if (txt.length && value) {
                txt.val(value.toString());
            }
        },
        destroyUIComponents: function () {
            if ($.fn.multiSelect !== undefined) {
                $('.multi-select, .multiselect').multiSelect('destroy');
            }
        },
        refreshUIComponents: function () {
            if ($.fn.multiSelect !== undefined) {
                $('.multi-select').multiSelect('refresh');
            }
        },
        disableInputs: function (form) {
            if (!form) {
                form = $('#content').find('form').first();
            }
            if (window.location.href.indexOf('/view') > -1) {
                $(':input', form).prop('disabled', true);
                $('.make-switch', form).bootstrapSwitch('disabled', true);
                $('button[type="submit"]', form).hide();
            }
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
        remoteModal: function (url, modalid, callback) {
            $('.modal-remote').remove();
            var modalRemote = $('<div/>').addClass('modal-remote').appendTo('body');
            modalRemote.load(url, function () {
                var modal = $(modalid).modal();
                if (callback !== undefined)
                    eval(callback);
            });
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
        showDialog: function (sender, target, url, id) {
            var senderel = $(sender);
            var formurl = url || senderel.attr('href');
            var formid = id || 0;
            var dialog = $(target);
            var frm = dialog.find('form').first();
            frm.attr('action', formurl);
            frm.find('input:hidden[name="id"]').first().val(formid);
            dialog.modal();
            return false;
        },
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
            var submitText = (options && options['submit-text']) ? options['submit-text'] : 'Kaydet';
            if (options && options['hide-save-button']) {
                buttons = $('<div/>').addClass('modal-footer').append(
                    $('<button/>', {
                        'type': 'button',
                        'data-dismiss': 'modal'
                    }).addClass('btn btn-primary').text('Kapat')
                );
            } else {
                buttons = $('<div/>').addClass('modal-footer').append(
                    $('<button/>', {
                        'type': 'button',
                        'data-dismiss': 'modal'
                    }).addClass('btn btn-secondary').text('Kapat'),
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
                        // if (!$this.valid()) {
                        //     App.notify('Zorunlu alanları doldurunuz!!!', 'error');
                        //     return;
                        // }
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
                            App.alert('Sunucu hatası oluştu, sayfayı yenileyin!');
                        });
                    })
                );
                // App.validator(modal.find('.modal-content').find('form'));
                // $('.modal-dialog').draggable({
                //     handle: ".modal-header"
                // });
                // mApp.unblock($('body'));
            });
        },
        validator: function (form) {
            return $(form).validate({
                ignore: 'input[type=hidden], .select2-search__field, :not(:visible)', // ignore hidden fields
                errorClass: 'validation-error-label form-control-feedback',
                successClass: 'validation-valid-label',
                onfocusout: function (element) {
                    $(element).valid();
                },
                highlight: function (element, errorClass) {
                    $(element).removeClass(errorClass).closest('div').addClass('has-danger');
                },
                unhighlight: function (element, errorClass) {
                    $(element).removeClass(errorClass).closest('div').removeClass('has-danger');
                },
                // Different components require proper error label placement
                errorPlacement: function (error, element) {
                    // Styled checkboxes, radios, bootstrap switch
                    if (element.parents('div').hasClass('checker') || element.parents('div').hasClass('choice') || element.parent().hasClass('bootstrap-switch-container')) {
                        if (element.parents('label').hasClass('checkbox-inline') || element.parents('label').hasClass('radio-inline')) {
                            error.appendTo(element.parent().parent().parent().parent());
                        } else {
                            error.appendTo(element.parent().parent().parent().parent().parent());
                        }
                    }
                    // Unstyled checkboxes, radios
                    else if (element.parents('div').hasClass('checkbox') || element.parents('div').hasClass('radio')) {
                        error.appendTo(element.parent().parent().parent());
                    }
                    // Input with icons and Select2
                    else if (element.parents('div').hasClass('has-feedback') || element.hasClass('select2-hidden-accessible')) {
                        error.appendTo(element.parent());
                    }
                    // Inline checkboxes, radios
                    else if (element.parents('label').hasClass('checkbox-inline') || element.parents('label').hasClass('radio-inline')) {
                        error.appendTo(element.parent().parent());
                    }
                    // Input group, styled file input
                    else if (element.parent().hasClass('uploader') || element.parents().hasClass('input-group')) {
                        error.appendTo(element.parent().parent());
                    } else {
                        error.insertAfter(element);
                    }
                },
                validClass: 'validation-valid-label',
                success: function (label) {
                    label.closest('div').removeClass('has-danger');
                    // label.addClass('validation-valid-label').text('Geçerli')
                },
                //rules: rules,
                //messages: messages,
                submitHandler: function (form) {
                    //    callback(form);
                }
            });
        },
        makeAjaxForm: function (form_elem) {
            var frm = form_elem || $('#form');
            frm.submit(function (e) {
                e.preventDefault();
                if (!$(this).valid()) {
                    App.notify('Zorunlu alanları doldurunuz!!!', 'error');
                    return;
                }
                var next = $(this).data('next');
                var target = $(this).data('target');
                var callback = $(this).data('callback');
                var formData = new FormData(this);
                // mApp.block(frm, {});
                $.ajax({
                    'type': $(this).attr('method'),
                    'url': $(this).attr('action'),
                    'cache': false,
                    'dataType': 'json',
                    'contentType': false,
                    'processData': false,
                    'data': formData
                }).done(function (result) {
                    // mApp.unblock(frm);
                    if (result.success) {
                        App.notify(result.message);
                        if (callback) {
                            eval(callback + '(result);');
                        }
                        if (next) {
                            if (parseFloat(result.id)) {
                                next = next.replace('0', parseFloat(result.id));
                                next = next.replace('{id}', parseFloat(result.id));
                            }
                            if (target) {
                                App.openWindow(next, target);
                            } else {
                                window.location.href = next;
                            }
                        } else if (!parseFloat($('#id').val()) && parseFloat(result.id)) {
                            if (window.location.href.substr(window.location.href.toString().lastIndexOf('/') + 1) !== result.id.toString())
                                window.location.href = window.location.origin + window.location.pathname + '/' + result.id;
                        }
                    } else {
                        App.alert(result.message);
                    }
                }).fail(function (jqXHR, textStatus) {
                    // mApp.unblock(frm);
                    App.alert('Sunucu hatası oluştu, sayfayı yenileyin!');
                });
            });
            App.validator('#form');
        },
        reloadDataTables: function () {
            $.each(App.datatable, function (item) {
                App.datatable[item].getDataTable().ajax.reload();
            });
        },
        stringFormat: function (format) {
            var args = Array.prototype.slice.call(arguments, 1);
            return format.replace(/{(\d+)}/g, function (match, number) {
                return typeof args[number] != 'undefined' ? args[number] : match;
            });
        },
        fullHeight: function (className) {
            App._fullHeight(className);
            $(window).resize(function () {
                App._fullHeight(className);
            });
        },
        _fullHeight: function (className) {
            var winHeight = $(window).height();
            $(className).each(function () {
                var top = $(this).position().top + 50;
                $(this).height(winHeight - top);
            });
        },
        openLocation: function (provider, lat, lon) {
            var url = null;
            switch (provider) {
                case 1: //google
                    url = App.stringFormat('https://www.google.com/maps/search/?api=1&query={0},{1}&language=tr', lat, lon);
                    break;
                case 2: //yandex
                    url = App.stringFormat('https://yandex.com.tr/harita/?pt={1},{0}&z=16', lat, lon);
                    break;
                case 3: //osm
                    url = App.stringFormat('https://www.openstreetmap.org/edit#map=19/{0}/{1}', lat, lon);
                    break;
            }
            if (url != null) {
                App.openWindow(url);
            }
        },
        replaceTurkishChars: function (txt) {
            var dict = {
                'ğ': 'g',
                'ı': 'i',
                'ç': 'c',
                'ü': 'u',
                'ö': 'o',
                'ş': 's',
                'Ğ': 'G',
                'İ': 'I',
                'Ç': 'C',
                'Ü': 'U',
                'Ö': 'O',
                'Ş': 'S'
            };
            txt = txt.replace(/[^\w ]/g, function (char) {
                return dict[char] || char;
            });
            return txt;
        },
        b64EncodeUnicode: function (str) {
            return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
                function toSolidBytes(match, p1) {
                    return String.fromCharCode('0x' + p1);
                }));
        },
        b64DecodeUnicode: function (str) {
            return decodeURIComponent(atob(str).split('').map(function (c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
        },
    };
}();
$(document).ready(function () {
    App.init();
});
Number.prototype.format_decimal = function (dec, dec_del, tho_del, symbol, grouping) {
    var re = '\\d(?=(\\d{' + (grouping || 3) + '})+' + (dec > 0 ? '\\D' : '$') + ')',
        num = this.toFixed(Math.max(0, ~~dec));
    return (symbol ? symbol + ' ' : '')
        + (dec_del ? num.replace('.', dec_del) : num).replace(new RegExp(re, 'g'), '$&' + (tho_del || ','));
};
Number.prototype.format_decimal_tr = function () {
    return this.format_decimal(2, ',', '.', '₺');
};
/**
 * Number.prototype.format_try()
 *
 * @usage 12345678.9.format_try() = "₺ 12.345.678,90"
 *
 * @returns {string}
 */
// Number.prototype.format_try = function () {
//     return this.format_decimal(2, ',', '.', '₺');
// };
// Number.prototype.format = function () {
//     return this.format_decimal(2, ',', '.', '');
// };
// Number.prototype.format_int = function () {
//     return this.format_decimal(0, ',', '.', '');
// };
// $.fn.datepicker.dates['tr'] = {
//     days: ['Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'],
//     daysShort: ['Paz', 'Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cts'],
//     daysMin: ['Pa', 'Pt', 'Sa', 'Ça', 'Pe', 'Cu', 'Ct'],
//     months: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
//     monthsShort: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'],
//     today: 'Bugün',
//     weekStart: 1,
//     format: 'dd.mm.yyyy',
//     clear: 'Temizle'
// };
// $.fn.datepicker.defaults.language = 'tr';
// (function ($) {
//     $.extend($.fn, {
//         makeCssInline: function () {
//             this.each(function (idx, el) {
//                 var style = el.style;
//                 var properties = [];
//                 for (var property in style) {
//                     if ($(this).css(property)) {
//                         properties.push(property + ':' + $(this).css(property));
//                     }
//                 }
//                 this.style.cssText = properties.join(';');
//                 $(this).children().makeCssInline();
//             });
//         }
//     });
// }(jQuery));