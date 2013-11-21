$("form input[type=submit]").click(function() {
	//This function sets clicked=true to the input button clicked of the form
    $("input[type=submit]", $(this).parents("form")).removeAttr("clicked");
    $(this).attr("clicked", "true");
});

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

function customMenu(node) {
	//This is the context menu of the jstree

	// The default set of all items
	var items = {
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
		"Edit" : {
			"label": "Edit",
			"submenu": {
				"Cut": {
					"label" : "Cut",
					"action" : function(obj) { this.cut(obj); }
				},
				"Copy" : {
					"label" : "Copy",
					"action": function(obj) { this.copy(obj); }
				},
				"Paste": {
					"label": "Paste",
					"action": function(obj) { this.paste(obj); }
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
		},
		"Edit_Item": {
			"label": "Edit Item",
			"action": function(obj) { 
				//Fills the form with the selected item data
				$('#edit_item_form').find('#id_id').val($('.jstree-clicked').parent().attr('id'));
				$('#edit_item_form').find('#id_name').val($('.jstree-clicked').parent().attr('name'));
				$('#edit_item_form').find('#id_price').val($('.jstree-clicked').parent().attr('price'));
				$('#edit_item_form').find('#id_description').val($('.jstree-clicked').parent().attr('description'));
				$('#edit_item_modal_button').click();
			}
		}
	};
	// Cases for each type of node
	switch ($(node).attr('rel')) {
		case 'root':
			delete items.Insert;
			delete items.Edit.submenu.Cut;
			delete items.Edit.submenu.Copy;
			delete items.Edit.submenu.Remove;
			delete items.Edit_Item;
		break;
		
		case 'section':
			delete items.Insert;
			delete items.Edit_Item;
		break;
		
		case 'subsection':
			delete items.Create
			delete items.Edit_Item;
		break;
		
		case 'item':
			delete items.Create
			delete items.Insert;
			delete items.Edit.submenu.Paste;
			delete items.Edit.submenu.Rename;
		break;
	};
	
	return items;
}
  
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
		"plugins" : [ "themes", "json_data", "ui", "dnd", "crrm", "contextmenu", "hotkeys", "unique", "types" ],
		"contextmenu": {"items": customMenu	},
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
				'edit_item': ''
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
	
	$('#edit_item_form').submit(function() {
		var form = objetify_form($(this).serializeArray());
		$.ajax({
			data: $(this).serialize() + "&edit_item" + "&item_form",
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(response) {
				$('li[id="' + form.item_id + '"]').attr('name', form.name).attr('price', form.price).attr('description', form.description);
				$('li[id="' + form.item_id + '"]').children('a').html('<ins class="jstree-icon">&nbsp;</ins>' + form.name)
				$('#insert_item_loader').load(' #insert_item_table_container', function(){item_insert_table()});
				$('#edit_item_modal').modal('toggle');
			}
		});	
		return false;
	});
	
	$('#create_item_form').submit(function() {
		var button_pressed = $("input[type=submit][clicked=true]").val();
		$.ajax({
			data: $(this).serialize() + "&create_item" + "&item_form",
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(response) {
				$('#table_div').load(' #myTable', function(){tabledisplay()});
				$('#insert_item_loader').load(' #insert_item_table_container', function(){item_insert_table()});
				if (button_pressed == "Create") {
					$('#create_item_modal').modal('toggle');
				}
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
			$('.jstree[aria-expanded="true"]').jstree(
				"create",
				null,
				"inside",
				{
					"data": $(this).children('#item_insert_name').text(),
					"attr": {
						"rel": "item",
						"id": $(this).children('#item_insert_id').text(),
						"name": $(this).children('#item_insert_name').text(),
						"price": $(this).children('#item_insert_price').text(),
						"description": $(this).children('#item_insert_description').text()
					}
				},
				false,
				true
			);
		});
		$('#insert_item_modal').modal('toggle');
	});
	
	var parts = location.pathname.split("/");
	var url = parts[parts.length - 1];
    // Will only work if string in href matches with location
        $('ul.nav a[href="./' + url + '"]').parent().addClass('active');
		
	tabsfunc();
	treemaker();
	item_insert_table()
});
