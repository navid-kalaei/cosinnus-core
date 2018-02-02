'use strict';

module.exports = Backbone.View.extend({
	
	/**
	 * Sets these values on the view:
	 *  - self.options: 
	 *  	- purpose: the general behavioural settings for the view. only differ from default
	 *  		if passed through as View.init(options). don't change during runtime
	 *  	- value: extended self.defaults with the parameter options
	 *  - self.state:
	 *  	- purpose: current state variables of the view. defaults can be set in 
	 *  		self.defaults.state, or passed through View.init(options.state).
	 *  		constantly change with the view's current state
	 *  	- value: self.options.state if exists or {}
	 */
    initialize: function (options) {
    	this.options = $.extend(true, {}, this.defaults, options);
        this.state = this.options && this.options.state || {};
    },

    render: function () {
        var self = this;
        // Collect the data to be rendered; can be overridden in child view.
        var data = this.getTemplateData();
        // Use nunjucks to render the template (specified in child view).
        if (this.template && this.template.render &&
            typeof this.template.render === 'function') {
        	var rendered = this.template.render(data);
        	if (self.options.el_append) {
        		this.$el.append(rendered);
        	} else {
        		this.$el.html(rendered);
        	}
        }
        // After a repaint (to allow further rendering in #afterRender),
        // call the after render method if it exists.
        setTimeout(function () {
            self.afterRender && self.afterRender();
        }, 0);
        return this;
    },

    // Default implementation to retrieve data to be rendered.
    // If a model is set, return its attributes as JSON, otherwise
    // an empty object with any state attributes on the view mixed in.
    getTemplateData: function () {
        var modelData = this.model && this.model.toJSON() || {};
        var data = _(modelData).extend(this.state);
        data.options = this.options;
        return data;
    }
});
