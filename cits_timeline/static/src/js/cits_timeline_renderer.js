odoo.define('cits_timeline.TimelineRenderer', function (require) {
    'use strict';
    const AbstractRenderer = require('web.AbstractRenderer');
    const field_utils = require('web.field_utils');
    const session = require('web.session');
    const utils = require('web.utils');
    const core = require('web.core');
    const QWeb = require('web.QWeb');
    const _t = core._t;
    const qweb = core.qweb;
    return AbstractRenderer.extend({
        template: 'TimelineView',
        events: _.extend({}, AbstractRenderer.prototype.events, {}),
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.displayFields = params.displayFields;
            this.ignoreGroups = [
                '__ungrouped__',
                '__background__'
            ];
            this.model = params.model;
            if (params.itemTemplate) {
                this.qweb = new QWeb(session.debug, {_s: session.origin});
                this.qweb.add_template(utils.json_node_to_xml(params.itemTemplate));
            }
        },
        start: function () {
            return this._super.apply(this, arguments);
        },
        destroy: function () {
            this._destroyTimeline();
            this._super.apply(this, arguments);
        },
        getLocalState: function () {
            return {
                selection: this.timeline.getSelection()
            };
        },
        setLocalState: function (localState) {
            this.timeline.setSelection(localState.selection);
        },
        _itemRender: function (item) {
            var qweb_context = {
                item: item,
                record: item.record,
                widget: this,
                read_only_mode: this.read_only_mode,
                user_context: session.user_context,
                format: this._format.bind(this),
                fields: this.state.fields
            };
            this.qweb_context = qweb_context;
            if (_.isEmpty(qweb_context.record)) {
                return '';
            } else {
                return (this.qweb || qweb).render('TimelineView.item', qweb_context);
            }
        },
        _format: function (record, fieldName) {
            var field = this.state.fields[fieldName];
            var formatted;
            if (field.type === 'one2many' || field.type === 'many2many') {
                formatted = field_utils.format[field.type]({
                    data: record[fieldName]
                }, field);
            } else {
                formatted = field_utils.format[field.type](record[fieldName], field, {
                    forceString: true
                });
            }
            return formatted;
        },
        _initTimeline: function (scrollTo) {
            var self = this;
            this.$timeline = this.$('.o_timeline_widget');
            var timeline_options = $.extend({}, this.state.timeline_options, {
                stack: false,
                height: '100%',
                locale: 'es',
                orientation: {
                    item: 'top',
                    axis: 'both'
                },
                zoomMin: 1000 * 60 * 15 * 24,
                zoomMax: 1000 * 60 * 60 * 24 * 365,
                min: new moment({year: 2020}).toDate(),
                max: new moment({year: 2030}).toDate(),
                hiddenDates: [
                    {start: "2021-01-01 21:00:00", end: "2021-01-02 09:30:00", repeat: "daily"}
                ],
                tooltipOnItemUpdateTime: true,
                showCurrentTime: false,
                template: function (item) {
                    return self._itemRender(item);
                },
                moment: function (date) {
                    return vis.moment(date).utc();
                },
                groupTemplate: function (group) {
                    if (group !== null) {
                        var value = group.record[group.displayField];
                        if (value instanceof Array) {
                            value = value[1];
                        }
                        return value || _t('Undefined');
                    }
                },
                onMove: function (item, callback) {
                    self.trigger_up('updateItem', item);
                    callback(item);
                }
            });
            this.timeline = new vis.Timeline(this.$timeline.get(0), this.state.items, this.state.groups, timeline_options);
            this.timeline.on('rangechanged', function (evt) {
                if (evt.byUser) {
                    self.trigger_up('changeRange', {
                        start: moment(evt.start),
                        end: moment(evt.end)
                    });
                }
            });
            var previousSelectItem = null;
            this.timeline.on('select', function (evt) {
                if (evt.items.length === 1) {
                    if (evt.items[0] === previousSelectItem) {
                        self.trigger_up('openItem', self.state.items.get(previousSelectItem));
                    }
                    previousSelectItem = evt.items[0];
                } else {
                    previousSelectItem = null;
                }
            });
            this.timeline.on('doubleClick', function (evt) {
                if (previousSelectItem === null) {
                    self.trigger_up('openCreate', {
                        snappedTime: evt.snappedTime,
                        group: evt.group
                    });
                }
            });
        },
        _destroyTimeline: function () {
            this.timeline.destroy();
            this.timeline = undefined;
        },
        _redrawTimeline: function () {
            var self = this;
            setTimeout(function () {
                self.timeline.redraw();
            }, 0);
        },
        _render: function () {
            if (this.timeline !== undefined && this.timeline.itemsData !== this.state.items) {
                this._destroyTimeline();
            }
            if (this.$el.get(0).offsetParent === null && this.timeline !== undefined) {
                this._redrawTimeline();
            }
            if (this.timeline === undefined) {
                this._initTimeline();
                this._redrawTimeline();
            } else {
                this.timeline.setWindow(this.state.start_date.toDate(), this.state.end_date.toDate());
            }
            var visibleGroups = [];
            for (var groupId in this.timeline.itemSet.groups) {
                if (this.ignoreGroups.indexOf(groupId) !== -1) {
                    continue;
                }
                if (this.timeline.itemSet.groups.hasOwnProperty(groupId)) {
                    var group = this.timeline.itemSet.groups[groupId];
                    if (group.isVisible) {
                        visibleGroups.push(group.groupId);
                    }
                }
            }
            this.trigger_up('updateView', {
                visibleGroups: visibleGroups
            });
            return this._super.apply(this, arguments);
            this._redrawTimeline();
        }
    });
})