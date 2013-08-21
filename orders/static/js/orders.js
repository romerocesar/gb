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
		$(this).closest('.menu_items').hide();
		return false;	
	});
	$('#add_item_form').submit(function() {
		var name = $(this).find('#id_name').val()
		var price = $(this).find('#id_price').val()
		var description = $(this).find('#id_description').val()
		$.ajax({
			data: $(this).serialize() + "&add_item",
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(response) {
				$(this).find('.ajaxwrapper').html(response);
				$('#myTable').append('<tr> <td>'+name+'</td> <td>'+price+'</td> <td>'+description+'</td> <td><button>delete</button></td> </tr>');
			}
		});
		
		return false;
	});
	
	var pathname = location.pathname.substring(1);
	var parts = pathname.split(/\//);
	var url = parts[parts.length - 1];
    // Will only work if string in href matches with location
        $('ul.nav a[href="./' + url + '"]').parent().addClass('active');
});
