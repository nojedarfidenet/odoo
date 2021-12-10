odoo.define('custom_calendar', function (require) {
    "use strict";

    let CalendarModel = require('web.CalendarModel');

    CalendarModel.include({
        _getFullCalendarOptions: function () {
            let res = this._super.apply(this, arguments);
            return _.extend(res, {
                minTime: '07:00:00',
                maxTime: '21:00:00',
                slotDuration: '00:15:00',
            });
        },
    });
});