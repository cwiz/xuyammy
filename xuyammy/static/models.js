// User
var User = Backbone.Model.extend({
	defaults: {
	}
});

// Project
var ProjectModel = Backbone.Model.extend({
	defaults: {
	}
});

// Sprint
var SprintModel = Backbone.Model.extend({
	defaults: {
		text: ''
	},
	urlRoot: '/sprint'
});

// Story
var StoryModel = Backbone.Model.extend({
	defaults: {
		text: ''
	}
});

// The Task
var TaskModel = Backbone.Model.extend({
	defaults: {
		text: ''
	}
});

// Comment
var CommentModel = Backbone.Model.extend({
	defaults: {
	}
});


// SprintCollection

// StoryCollection
var Stories = Backbone.Collection.extend({
	model: StoryModel,
	url: '/sprint/'
});


// TaskCollection
// CommentCollection
