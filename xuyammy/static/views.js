// Main view contains header, filters panel, main desk
var Xuyammy = Backbone.View.extend({
	el: 'body',
	initialize: function(){
		/*
			app
			  |_user
			       |_projects
			                |_sprints
			                        |_desk
			                        |    |_stories
				                    |            |_tasks
				                    |                  |_comments
			                        |_tags
		*/
		this.desk = new Desk();
		this.stories = new Stories();
		this.stories.fetch();
	},
	render: function(){
		this.$('#main').append(this.desk.el);
	}
});

// Desk view contains stories table of the sprint
var Desk = Backbone.View.extend({
	tag: 'div',
	id: 'desk',
	template: _.template('<table></table>'),
	initialize: function(){
		this.table = this.$(this.template()).appendTo(this.el);
		this.render();
	}
});

