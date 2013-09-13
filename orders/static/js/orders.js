function tabsfunc() {
    $( "#tabs" ).tabs().addClass( "ui-tabs-vertical ui-helper-clearfix" );
    $( "#tabs li" ).removeClass( "ui-corner-top" ).addClass( "ui-corner-left" );
  };

function treemaker(){  
  	for (var i=0; i<menus.length; i++){
		var j = i + 1;
		$("#tabs-"+ j +"").jstree({
		"json_data": menus[i],
		"types": {

			"valid_children" : ["root"],
			"types": {
				"root" : {
					"valid_children": ["section", "subsection"],
					"icon": {
						"image": "http://static.jstree.com/v.1.0rc/_docs/_drive.png"
					},
					"start_drag" : false,
                    "move_node" : false,
                    "delete_node" : false,
                    "remove" : false
				},
				"section": {
					"valid_children" : ["section", "subsection"]
				},
				"subsection": {
					"valid_children": ["item"]
				},
				"item": {
					"valid_children": "none",
					"icon": {
						"image": "http://static.jstree.com/v.1.0rc/_demo/file.png"
					},
					"rename" : false
				}
			}
		},
		"themes": {
			"theme": "apple"
		},
		"plugins" : [ "themes", "json_data", "ui", "dnd", "crrm", "contextmenu", "hotkeys", "unique", "types", "sort" ],
		"contextmenu": {
			"items": {
				"ccp": false,
				"create": false,
				"rename": false,
				"remove": false,
				"Create": {
					"label": "Create",
					"separator_after": true,
					"submenu": {
						"Section": {
							"label": "Section",
							"action": function (obj) {
								this.create(obj, "inside", {"data": "New Section", "state": "open", "attr":{"rel": "section"}}); 
							}
						},
						"Sub": {
							"label": "Sub-Section",
							"action": function (obj) {
								this.create(obj, "inside", {"data": "New Sub-Section", "state": "open", "attr":{"rel": "subsection"}}); 
							}
						}
					}
				},
				"Insert": {
					"label": "Insert Item",
					"separator_after": true,
					"action": function(obj){alert("Display all the items to select from them")} 
				},
				"Rename" : {
					"label" : "Rename",
					"action" : function (obj) { this.rename(obj); }
				},
				"Remove": {
					"label": "Remove",
					"action": function(obj) { this.remove(obj); }
				}
			}
		}
		});
	};
};  
  
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
	$('#add_menu_form').submit(function() {
		var title = $(this).find('#tab_title').val()
			$.ajax({
				data: $(this).serialize() + "&add_menu",
				type: $(this).attr('method'),
				url: $(this).attr('action'),
				success: function(response) {
					$('#tabs_container').load(' #tabs', function(){tabsfunc(); treemaker();});

					//$('#tabs').children('ul').append('<li class="ui-state-default ui-corner-left" role="tab" tabindex="-1" aria-controls="tabs-3" aria-labelledby="ui-id-3" aria-selected="false">'+title+'</li>');
				}
			});
		return false;
	});
	
	
	var parts = location.pathname.split("/");
	var url = parts[parts.length - 1];
    // Will only work if string in href matches with location
        $('ul.nav a[href="./' + url + '"]').parent().addClass('active');
		
tabsfunc();
treemaker();
});
