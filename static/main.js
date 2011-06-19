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
					<td><h6><strong>open</strong></h6></td>\
					<td class="progress"><h6><strong>in progress</strong></h6></td>\
					<td class="ready"><h6><strong>done</strong></h6></td>\
				</tr></tbody>', item).appendTo('#desk table');
				
				$('#desk tbody td').sortable({
					connectWith: story.find('tbody td'),
					items: 'div.task',
					placeholder: 'task placeholder'
				});
			}

			story.find('h3').text(item.title);
		}
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
