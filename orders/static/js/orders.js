$(document).ready(function() {
    $('#myTable').tablesorter({
		sortList: [[0,0], [1,0]],
		headers: {
			3: { sorter: false }
		}
	}).tableFilter();
	$('.delete_button').submit(function() {
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(response) {
				$(this).find('.ajaxwrapper').html(response);
			}
		});
		$(this).closest('.menu_items').remove();
		return false;
		
	});
});
