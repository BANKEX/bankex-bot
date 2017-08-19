"use strict";
define([], function () {
    return {
        /**
         * Склонятор.
         * @param number        int числительное, по которому склоняем
         * @param nameNominative string есть кто, что - место
         * @param nameGenitive   string нет кого, чего - места
         * @param namePlural     string много кого, чего - мест
         * @return string
         */
        pluralize: function (number, nameNominative, nameGenitive, namePlural) {
            var t1 = number % 10,
                t2 = number % 100;
            if (t1 === 1 && t2 !== 11) {
                /* 1, 21, 31... */
                return nameNominative;
            } else if (t1 >= 2 && t1 <= 4 && (t2 < 10 || t2 >= 20)) {
                /* 2-4, 22-24, 32-34... */
                return nameGenitive;
            } else {
                /* 5-9, 10-19, 20, 25-29, 30, 35-39... */
                return namePlural;
            }
        },
        escapeHtml: function (html) {
            if (typeof html !== 'string') {
                html = '';
            }
            return html
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        },
        spaceNumbers: function (n) {
            /* http://stackoverflow.com/questions/9743038/how-do-i-add-a-thousand-seperator-to-a-number-in-javascript */
            if (n === null) {
                return '';
            }
            var rx = /(\d+)(\d{3})/;
            return String(n).replace(/^\d+/, function (w) {
                while (rx.test(w)) {
                    w = w.replace(rx, '$1 $2');
                }
                return w;
            });
        },
        getMonthName: function (monthNumber, monthCase) {
            if (typeof monthNumber !== 'number' || isNaN(monthNumber) || monthNumber > 11) {
                monthNumber = 0;
            }
            if (typeof monthCase !== 'number' || isNaN(monthCase) || monthCase > 1) {
                monthCase = 0;
            }

            var month = [
                ['Январь', 'Января'],
                ['Февраль', 'Февраля'],
                ['Март', 'Марта'],
                ['Апрель', 'Апреля'],
                ['Май', 'Мая'],
                ['Июнь', 'Июня'],
                ['Июль', 'Июля'],
                ['Август', 'Августа'],
                ['Сентябрь', 'Сентября'],
                ['Октябрь', 'Октября'],
                ['Ноябрь', 'Ноября'],
                ['Декабрь', 'Декабря']
            ];

            return month[monthNumber][monthCase];
        },
        getMonthNameLower: function (monthNumber, monthCase) {
            var month = this.getMonthName(monthNumber, monthCase);
            if (typeof month === 'string') {
                month = month.toLowerCase();
            }
            return month;
        }
    };
});