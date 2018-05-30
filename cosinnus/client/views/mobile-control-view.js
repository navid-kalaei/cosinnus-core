'use strict';

var BaseView = require('views/base/view');
var util = require('lib/util');

var mobileControlsTemplate = require('map/mobile-controls');


/** 
 * A small view, basically just to encapsulate the mobile control
 * template and buttons, to be able to render and refresh them independently
 * of the search controls. 
 * This is contained by and delegates almost everything back to the control-view.
 * */
module.exports = BaseView.extend({
    
    // reference back to the main App
    App: null,
    
    controlView: null,
    
    template: mobileControlsTemplate,
    
    // The DOM events specific to an item.
    events: {
        'click .trigger-mobile-list-view': 'triggerMobileListView',
        'click .trigger-mobile-search-view': 'triggerMobileSearchView',
        'click .trigger-mobile-map-view': 'triggerMobileMapView'
    },
    
    initialize: function (options, app, controlView) {
        var self = this;
        BaseView.prototype.initialize.call(self, options);
        self.App = app;
        self.controlView = controlView;
    },
    
    /** Extend the template data by the controlView's options and state */
    getTemplateData: function () {
        var self = this;
        var data = BaseView.prototype.getTemplateData.call(self);
        data = _.extend(
            data,
            self.controlView.options,
            self.controlView.state
        );
        return data;
    },
    
    
    // Events  -------------
    

    // delegate to controlView
    triggerMobileListView: function (event) {
        self.controlView.triggerMobileListView();
    },

    // delegate to controlView
    triggerMobileSearchView: function (event) {
        self.controlView.triggerMobileSearchView();
    },

    // delegate to controlView
    triggerMobileMapView: function (event) {
        self.controlView.triggerMobileMapView();
    },
    
    
});