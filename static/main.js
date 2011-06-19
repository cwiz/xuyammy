$(document).ready(function(){
	
	data.get();

	$('div.task').task();
});

var data = {
	get: function(){
		$.getJSON('/data/', data.parse);
	},
	parse: function(resp){
		var order = ['tags', 'stories', 'tasks'];
		for(var i = 0; i < order.length; i++)
		{
			var id = order[i];
			if((id in resp) && ('parse_' + id in data)) data['parse_' + id](resp[id]);
		}
		data.refresh();
	},
	parse_stories: function(data){
		for(var id in data)
		{
			var item = data[id],
			    story = $('thead[story=' + id + '], tbody[story=' + id + ']');
			
			if(!story.length)
			{
				story = $.tmpl('<thead story="${id}"><tr><td colspan="3"><h3></h3></td></tr></thead>\
				<tbody story="${id}"><tr>\
					<td class="open"><h6><strong>open</strong></h6></td>\
					<td class="progress"><h6><strong>in progress</strong></h6></td>\
					<td class="ready"><h6><strong>done</strong></h6></td>\
				</tr></tbody>', item).appendTo('#desk table');
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
					<ul class="comments">\
						<li class="tc"><a href="#" class="add">add comment</a></li>\
					</ul>\
				</div>', item).task();
				
			}

			task.appendTo('tbody[story=' + item.story_id + '] td.' + status[item.status]);
		}
	},
	refresh: function() {
		$('#desk tbody td').sortable({
			connectWith: '#desk tbody td',
			items: 'div.task',
			placeholder: 'task placeholder',
			dropOnEmpty: true,
			containment: '#desk table'
		});
	}
};


$.fn.task = function(){
	return $(this).each(function(){
		var el = $(this);

		el
		.click($.fn.task.expand);

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
