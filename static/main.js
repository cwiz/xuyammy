$(document).ready(function(){
	
	data.get();

	$('div.task').task();
});

var data = {
	get: function(){
		var d = {};
		if(data.timestamp) d['timestamp'] = data.timestamp;
		$.getJSON('/data/', d, data.parse);
	},
	parse: function(resp){
		data.timestamp = parseInt(resp.timestamp);
		var order = ['tags', 'stories', 'tasks'];
		for(var i = 0; i < order.length; i++)
		{
			var id = order[i];
			if((id in resp) && ('parse_' + id in data)) data['parse_' + id](resp[id]);
		}
		data.refresh();

		setTimeout(data.get, 5000);
	},
	parse_stories: function(data){
		for(var id in data)
		{
			var item = data[id],
			    story = $('thead[story=' + id + '], tbody[story=' + id + ']');
			
			if(!story.length)
			{
				story = $.tmpl('<thead story="${id}"><tr><td colspan="3"><a href="#" class="add">+</a><h3></h3></td></tr></thead>\
				<tbody story="${id}"><tr>\
					<td class="open"><h6><strong>open</strong></h6></td>\
					<td class="progress"><h6><strong>in progress</strong></h6></td>\
					<td class="ready"><h6><strong>done</strong></h6></td>\
				</tr></tbody>', item).appendTo('#desk table');

				story.find('a.add').click($.fn.task.create);
			}

			story.find('h3').text(item.title);
		}
	},
	parse_tasks: function(data){
		var status = [null, 'open', 'progress', 'ready'];
		for(var id in data)
		{
			var item = data[id],
			    task = $('div.task[task=' + id + ']');
			
			//console.log(item);
			if(!task.length)
			{
				task = $.tmpl('<div class="task" task="${id}">\
					<div class="text">${description}</div>\
					<ul class="tags"></ul>\
					<p class="actions"><a href="#" class="save">save</a></p>\
					<ul class="comments">\
						<li class="status">no comments</li>\
						<li class="form"><a href="#" class="add">add comment</a></li>\
					</ul>\
				</div>', item).task();
			}

			task.attr('story', item.story_id).appendTo('tbody[story=' + item.story_id + '] td.' + status[item.status]);
		}
	},
	refresh: function() {
		$('#desk tbody td').sortable({
			connectWith: '#desk tbody td',
			items: 'div.task',
			placeholder: 'task placeholder',
			dropOnEmpty: true,
			containment: '#main'
		});
	}
};


$.fn.task = function(){
	return $(this).each(function(){
		var el = $(this);

		el
		.click($.fn.task.expand);

		el.find('a.save').click($.fn.task.save);

	});
};
$.fn.task.drop = function(event, ui){
	var el = $(this);

	ui.draggable.appendTo(el);
};
$.fn.task.expand = function(){
	var el = $(this);

	if(el.parents('#desk').length)
	{
		el.clone(true).data('original', el)
		.find('div.text').attr('contenteditable', 'true').end()
		.appendTo(
			$('#overlay > div').empty()
		);
		$('#overlay').show();
	}
};
$.fn.task.create = function(e){
	e.preventDefault();

	var story = $(this).parents('thead').attr('story');

	$('<div class="task">\
		<div class="text">&nbsp;</div>\
		<ul class="tags"></ul>\
		<p class="actions"><a href="#" class="save">okay, create it</a></p>\
	</div>')
	.task()
	.attr('story', story)
	.appendTo('tbody[story=' + story + '] td.open')
	.trigger('click');

	$('#overlay div.task div.text').focus();
};
$.fn.task.save = function(e){
	e.preventDefault();

	var el = $(this).parents('div.task'),
		d = {
			'description': el.find('div.text').html(),
			'story_id': el.attr('story')
		};
	
	if(el.attr('task')) d['id'] = el.attr('task');

	$.post('/task/save/', d, function(resp){
		
	});

	setTimeout(function(){
		$('#overlay').hide();
		el.data('original').replaceWith(el);
	}, 25);
};






