function filterCostDetails(e){
	
	value = (e.options[e.selectedIndex].value);
	
	var qty_tables = Array.prototype.slice.call( document.getElementsByClassName("by_qty") )
	var cost_tables = Array.prototype.slice.call( document.getElementsByClassName("by_cost") )
	
	if (value == "Quantity") {
		qty_tables.forEach(function(table){ table.style.display = "block"; });
		cost_tables.forEach(function(table){ table.style.display = "none"; });		
	} else if (value == "Cost") {
		qty_tables.forEach(function(table){ table.style.display = "none"; });
		cost_tables.forEach(function(table){ table.style.display = "block"; });		
	} else {
		qty_tables.forEach(function(table){ table.style.display = "block"; });
		cost_tables.forEach(function(table){ table.style.display = "block"; });		
	}
}

function filterCostDetailsByValue(e){

	value = (e.options[e.selectedIndex].id);
	
	var qty_tables = Array.prototype.slice.call( document.getElementsByClassName("by_qty") )
	var cost_tables = Array.prototype.slice.call( document.getElementsByClassName("by_cost") )
	
	if (value == "all") {
		qty_tables.forEach(function(table){ table.style.display = "block"; });
		cost_tables.forEach(function(table){ table.style.display = "block"; });		
	} else {
		qty_tables.forEach(function(table){ table.style.display = "none"; });
		cost_tables.forEach(function(table){ table.style.display = "none"; });
		
		tables = Array.prototype.slice.call( document.getElementsByClassName(value))
		tables.forEach(function(table){ table.style.display = "block"; });	
	}
}
