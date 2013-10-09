function objetify_form(array) {
	//This function takes an array = $.serializeArray()
	//and returns a JSON
	var obj = {}
	for (var i=0; i < array.length; i++) {
		obj[array[i].name] = array[i].value;
	}
	return obj;
};

function tabsfunc() {
	//This function sets the tabs with jQuery UI
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
					"action": function(obj) {$('#insert_item_modal_button').click()}
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
  
 function tabledisplay() {
	//This function add the the tablesorter and tableFilter to the table of items
	//In the item edit view
	$('#myTable').tablesorter({
		sortList: [[0,0], [1,0]],
		headers: {
			3: { sorter: false }
		}
	}).tableFilter();
 };
 
 function item_insert_table() {
	//This function add the the tablesorter and tableFilter to the table of items
	//In the menu edit view
	$('#insert_item_table').tablesorter({
		sortList: [[0,0]]
	}).tableFilter();
	$('#selectable').selectable({
		filter: "td"
	});
 };
 
 function new_menu(){
	//This function adds the new menu in the tabs
	//In the menu edit view
	var name = $('#tabs').children('ul').children('li:last-child').children('a').text();
	var id = $('#tabs').children('ul').children('li:last-child').children('p').text();
	menus.push(eval('({"data": [{"state": "open", "data": "' + name + '", "attr": {"id": "' + id + '", "rel": "root"}, "children": []}]})'));
};
$(document).ready(function() {

    tabledisplay();
	
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
	
	$('.save_edit_button').submit(function() {
		var name = $(this).parent().siblings('.item_name').text();
		var price = $(this).parent().siblings('.item_price').text();
		var description = $(this).parent().siblings('.item_description').text();
		var form = objetify_form($(this).serializeArray());
		$.ajax({
			data: {
				'csrfmiddlewaretoken': form.csrfmiddlewaretoken,
				'item_id': form.item_id,
				'name': name,
				'price': price,
				'description': description,
				'save_edit': ''
			},
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(response) {
				$('#myTable').tablesorter();
				$('#myTable').tablesorter();
			}
		});
		return false;
	});
	
	$('#add_item_form').submit(function() {
		$.ajax({
			data: $(this).serialize() + "&add_item",
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(response) {
				$('#table_div').load(' #myTable', function(){tabledisplay()});
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
					$('#tabs_container').load(' #tabs', function(){tabsfunc(); new_menu(); treemaker(); });					
				}
			});
		return false;
	});
	
	$('#save_menu_form').submit(function() {
		var tree = $('.jstree[aria-expanded="true"]').jstree("get_json", -1);
		var token = $(this).serializeArray()[0];
		$.ajax({
			data: {
				'csrfmiddlewaretoken': token.value,
				'save_menu': '',
				'tree': JSON.stringify(tree)
				},
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(response) {
				alert("This menu has been saved");
			}
		});
		return false;
	});
	
	$('#active_menu_form').submit(function() {
		var tree = $('.jstree[aria-expanded="true"]').jstree("get_json", -1);
		var token = $(this).serializeArray()[0];
		$.ajax({
			data: {
				'csrfmiddlewaretoken': token.value,
				'active_menu': '',
				'tree': JSON.stringify(tree)
				},
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(response) {
				alert("This menu has been set as the Active Menu");
			}
		});
		return false;
	});
	
	$('#insert_item_button').click(function() {
		$('.ui-selected').each(function(){
			$('.jstree[aria-expanded="true"]').jstree("create", null, "inside", {"data": $(this).children('span').text(), "attr": {"rel": "item", "id": $(this).children('p').text()}}, false, true);
		});
	});
	
	var parts = location.pathname.split("/");
	var url = parts[parts.length - 1];
    // Will only work if string in href matches with location
        $('ul.nav a[href="./' + url + '"]').parent().addClass('active');
		
tabsfunc();
treemaker();
item_insert_table()
});
