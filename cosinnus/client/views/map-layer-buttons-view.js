'use strict';

var BaseView = require('views/base/view');
var util = require('lib/util.js');

module.exports = BaseView.extend({
	
	template: require('map/map-layers'),
	
	mapView: null,
	
	// will be set to self.options during initialization
	defaults: {
		// will be set to self.state during initialization
		state: {
			layer: null
		}
	},
	
    initialize: function (options) {
    	var self = this;
    	BaseView.prototype.initialize.call(self, options);
    	
    	self.state.layer = options.layer;
    	self.mapView = options.mapView;
    },

    events: {
        'click .layer-button': 'switchLayerClicked',
    },

    // Event Handlers
    // --------------

    // Switch layers if clicked layer isn't the active layer.
    switchLayerClicked: function (event) {
        var layer = $(event.currentTarget).data('layer');
        if (this.mapView.options.layer !== layer) {
            this.mapView.options.layer = layer;
            this.state.layer = layer;
            // TODO: is layer arriving in the template?
            console.log('map-layer-buttons-view.js: TODO: is layer arriving in the template?')
            this.render();
            Backbone.mediator.publish('change:layer', layer);
        }
    },
    
});
