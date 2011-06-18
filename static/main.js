$(document).ready(function(){
	
	$('#desk tbody td').sortable({
		connectWith: '#desk tbody td',
		items: 'div.task',
		placeholder: 'task placeholder'
	});
	$('div.task').task();

});

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
