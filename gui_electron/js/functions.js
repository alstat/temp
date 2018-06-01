// populates divisions
function showDiv(divClass, div) {
	console.log("Showing div: " + div);
	divList = document.getElementsByClassName(divClass);
	for (var ctr= 0; ctr < divList.length; ctr++) {
		divList[ctr].style.display = (divList[ctr].id == div)? "block" : "none";
	}
}

// getElementById
function $id(id) {
	return document.getElementById(id);
}

// getElementById
function $val(id) {
	return document.getElementById(id).value;
}

function $class(arg) {
	return document.getElementsByClassName(arg)
}

// reads XML file
function readXML(file){
	var TABLE_FOLDER = "tables/";
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open("GET", TABLE_FOLDER + file + ".xml", false);
	xmlhttp.send(null);

	return(xmlhttp.responseXML);
}

function activateReline() {
	console.log("You clicked it!")
	var costDetails = $class("cost-details-table");
	for (var i = 0; i < costDetails.length; ++i) {
		costDetails[i].children[0].children[0].children[14].style.display = "block";
		console.log("Here are the descendants!");
		console.log(costDetails[i]);
		console.log(costDetails[i].children[1]);
		console.log(costDetails[i].children[1].children);
		console.log(costDetails[i].children[1].children.length);
		for (var j = 0; j < costDetails[i].children[1].children.length; ++i) {
			costDetails[i].children[1].children[j].children[14].style.display = "block";
		}
	}
}

// loads the tables
function loadTable(pageName, tableName){
	// populate tables
	console.log("Processing: " + tableName);
	
	pageNode = readXML(pageName);
	tableNode = pageNode.getElementsByTagName(tableName)[0];
	var tableHeader = $id(tableName).createTHead();
	var headerRow = tableHeader.insertRow(0);

	var tableBody = $id(tableName).createTBody();
	
	// Load Header Columns
	for (var i = 0; i < tableNode.children[0].children.length; i++) {
		headerRow.insertCell(-1).innerHTML = "<b> " + tableNode.children[0].children[i].innerHTML + "</b>";
	}

	// Load table rows
	for (var i = 0; i < tableNode.children[1].children.length; i++) {
		// insert row
		// row = $id(tableName).insertRow(-1);
		var row = tableBody.insertRow(-1)
		
		for (var j = 0; j < tableNode.children[1].children[i].children.length; j++) {
			child = tableNode.children[1].children[i].children[j];

			// add cell value
			if (child.attributes.length <= 1) {
				row.insertCell(-1).innerHTML = child.innerHTML;
			} else {
				value  = typeof(child.attributes.value) === "undefined"  ? "" : child.attributes.value.value;
				format = typeof(child.attributes.format) === "undefined" ? "number" : child.attributes.format.value;
				type = child.attributes.type.value;

				if (type != "values") {
					var input = document.createElement("input");
					input.setAttribute("type", format);
					input.setAttribute("value", value);
					input.setAttribute("id", child.attributes.id.value);

					if (typeof(child.attributes.class) != "undefined") {
						input.setAttribute("class", child.attributes.class.value);
					}

					if (typeof(child.attributes.colspan) != "undefined") {
						console.log("colspan not undefined");
						console.log(input.parentNode);
					}

				} else {
					var input = document.createElement("select");
					input.setAttribute("id", child.attributes.id.value);
					options = child.attributes.options.value.split(",");

					for (var k in options) {
						option = document.createElement("option");
						option.append(options[k].trim());
						input.append(option)
					}
				}
				row.insertCell(-1).append(input);
			}
		}
	}
}

function showCoverSheet() {
	showDiv("main_div_panel","div_cover_sheet");
	showDiv("div_panel","div_cover_sheet");
}

function computeCoverSheet(){
	$id("load-page-cover-sheet").style.display = "inline-block";
	var exportTable = $id("export-table-cover-sheets-cost-details");
	console.log(exportTable.value);
	if (exportTable.value === "None") {
		computeCoverSheetValues();
	} else if (exportTable.value === "Cover Sheet") {
		console.log("you want to export " + exportTable.value);
		var folderPath = prompt("Enter the complete path plus the file name without any extension.", "e.g. C:/user/downloads/cover-sheet");

		if (folderPath !== null) {
			computeCoverSheetValues(folderPath);
		}
		console.log("your request was granted, no error :D");
	} else {
		computeCoverSheetValues();
	}
}

function computeOutput(){
	showDiv("main_div_panel","div_output");
	showDiv("div_panel","div_output");
	computeOutputValues();
}

function computeCostDetails(){
	var exportTable = $id("export-table-cover-sheets-cost-details");

	if (exportTable.value === "None") {
		computeCostDetailsValues();
	} else if (exportTable.value === "Cost Details" || exportTable.value === "IDS Table") {
		console.log("you want to export " + exportTable.value);
		var folderPath = prompt("Enter the complete path plus the file name without any extension.", "e.g. C:/user/downloads/cost-details");

		if (folderPath !== null) {
			computeCostDetailsValues(folderPath);
		}
	}
	
	return output
}

function populateTable(tableName, tableID, response) {
	var output = response;
	var table = $id(tableID);
	var tBody = table.children[1].children
	console.log(tableName);
	console.log(output);
	var pattern = /qty$/;
	
	if (!pattern.test(tableID)) {
		var nRows = tBody.length 
	} else {
		var nRows = tBody.length + 1;
	}

	var nCols = tBody[0].children.length
	var colLabel = Object.keys(JSON.parse(output[tableName])[0])
	
	for (var i = 0; i < nRows - 1; ++i) {
		for (var j = 3; j < nCols - 1; ++j) {
			tBody[i].children[j].innerHTML = parseFloat(Math.round(JSON.parse(output[tableName])[i][colLabel[j - 3]] * 100) / 100).toFixed(2)
		}	
	}
}

function fillTables() {
	$id("load-page-cover-sheet").style.display = "inline-block";
	computeCostDetails();
}

function fillTotals() {
	var tableIDs = ["fuel_cost_details_cost", "fuel_cost_details_qty", "lubricant_cost_details_cost", "mud_chemicals_cost_details_cost", "mud_chemicals_cost_details_qty", "cement_cost_details_cost", "cement_cost_details_qty", 
		"rockbits_cost_details_smith_cost", "rockbits_cost_details_hughes_cost", "drilling_supplies_cost_details_cost", "drilling_supplies_cost_details_qty", "casing_cost_details_cost", "casing_cost_details_qty", 
		"wellhead_cost_details_cost", "wellhead_cost_details_qty", "cementing_services_cost_details_cost", "cementing_services_cost_details_qty",
		"directional_drilling_cost_details_cost", "directional_drilling_cost_details_qty", "mud_engineering_cost", "mud_engineering_qty", "aerated_drilling_cost", "aerated_drilling_qty", "jars_and_shock_cost", "jars_and_shock_qty",
		"chf_installation_cost", "chf_installation_qty", "mud_logging_services_cost", "mud_logging_services_qty", "casing_running_services_cost", "casing_running_services_qty", "drilling_rig_services_cost", "drill_pipes_cost", "drill_pipes_qty", "completion_test_cost", "completion_test_qty",
		"other_cementing_services_cost", "other_cementing_services_qty", "handling_hauling_cost",
		"equipmental_rental_cost", "equipmental_rental_qty", "rig_allocated_charges_cost"];

	for (k = 0; k < tableIDs.length; ++k) {
		var table = $id(tableIDs[k]);
		var tBody = table.children[1].children
		var nCols = tBody[0].children.length

		var pattern = /qty$/;

		if (!pattern.test(tableIDs[k])) {
			var nRows = tBody.length 
		} else {
			var nRows = tBody.length + 1;
		}
	
		for (var i = 0; i < nRows - 1; ++i) {
			var rowTotal = 0;
			for (var j = 3; j < nCols - 1; ++j) {
				rowTotal += parseFloat(tBody[i].children[j].innerHTML)
			}
			tBody[i].children[nCols - 1].innerHTML = parseFloat(Math.round(rowTotal * 100) / 100).toFixed(2)
		}

		if (!pattern.test(tableIDs[k])) {
			for (var i = 3; i < nCols; ++i) {
				var colTotal = 0;
				for (var j = 0; j < tBody.length - 1; ++j) {
					colTotal += parseFloat(tBody[j].children[i].innerHTML)
				}
				tBody[tBody.length - 1].children[i].innerHTML = parseFloat(Math.round(colTotal * 100) / 100).toFixed(2)
			}
		}
	}
}

function rowNames() {
	console.log("adding appropriate row names.");
	var data = getValues();
	
	var caQty = $id("cement_cost_details_qty");
	var caCost = $id("cement_cost_details_cost");
	if (data["rh_bh"] == "Big Hole") {
		caQty.children[1].children[10].children[0].innerHTML = "13 3/8\" CBP";
		caCost.children[1].children[10].children[0].innerHTML = "13 3/8\" CBP";
	}
}

function exportCoverSheet() {
	console.log("you clicked export cover sheet");
	var folderPath = prompt("Enter Folder Path", "e.g. C:/User/downloads");

	if (folderPath === null || folderPath === "") {
		alert("Error: Invalid Path!")
	} else {
		output = sendRequest(URL_EXPORT_COVER_SHEET, folderPath);
		console.log(output);
	}
	// console.log(folderPath);
}

function incrementDepth() {
	$id("load-page-permutation-casing").style.display = "block";

	var incrementDepths = checkerHelper("analysis-base-cd-inc");

	var suff = ["b", "1", "2", "3"];
	var phases = ["sh", "ih", "dh", "ph1", "ph2"];
	for (var i = 0; i < suff.length - 1; ++i) {
		for (var j = 0; j < phases.length; ++j) {
			var val = parseInt($id("analysis-" + phases[j] + "-cd-" + suff[i]).value);

			if (phases[j] === "dh" || phases[j] === "ph2") {
				var val = parseInt($id("analysis-" + phases[j] + "-cd-b").value);
				$id("analysis-" + phases[j] + "-cd-" + suff[i + 1]).value = val;
			} else {
				$id("analysis-" + phases[j] + "-cd-" + suff[i + 1]).value = val + parseInt(incrementDepths);
			}
		}
	}

	$id("load-page-permutation-casing").style.display = "none";
}

function computeBaseDaysDepth() {
	$id("load-page-permutation-casing").style.display = "block";

	var ropVal = $id("change-rop").value.slice($id("change-rop").value.length - 1);
	var phases = ["sh", "ih", "dh", "ph1", "ph2"];
	var suff = ["b", "1", "2", "3"];

	for (var i = 0; i < phases.length; ++i) {
		for (var j = 0; j < suff.length; ++j) {
			if (phases[i] === "sh") {
				var val = 0
			} else {
				var val = $id("analysis-" + phases[i - 1] + "-cd-" + suff[j]).value;
				console.log("Here po");
				console.log($id("analysis-" + phases[i - 1] + "-cd-" + suff[j]).value)
			}	
			console.log("analysis-cd-" + phases[i] + "-day-" + suff[j]);
			console.log("analysis-rop-" + phases[i] + "-inc-" + suff[j])
			$id("analysis-cd-" + phases[i] + "-day-" + suff[j]).value = Math.ceil(($id("analysis-" + phases[i] + "-cd-" + suff[j]).value - val) / $id("analysis-rop-" + phases[i] + "-inc-" + ropVal).value);
			console.log("Here is the ROP used : ROP"+ropVal);
		}	
	}
	$id("load-page-permutation-casing").style.display = "none";
}

function computeAFECosts(type = "rop") {
	// Arguments
	// 		type: string, type of computation (either 'rop' or 'cd')
	if (type === "rop") {
		$id("load-page-permutation").style.display = "block";
	} else {
		$id("load-page-permutation-casing").style.display = "block";
	}

	function callback(output, type) {
		if ($val("run-option") === "All") {
			var phases = ["sh", "ih", "dh", "ph1", "ph2"];
			var outPhases = ["surface", "intermediate", "prodn-casing", "prodn-liner-1", "prodn-liner-2"];
			var suff = ["1", "2"];
			for (var i = 0; i < suff.length; ++i) {
				for (var j = 0; j < phases.length; ++j) {
					$id("analysis-" + type + "-" + phases[j] + "-afe-" + suff[i]).value = commafy(output[outPhases[j]]["afe"][i]);
					$id("analysis-" + type + "-" + phases[j] + "-afe-" + suff[i]).title = tooltipHelper(output, outPhases, i, j);
					$id("analysis-" + type + "-" + phases[j] + "-trop-" + suff[i]).value = output[outPhases[j]]["total-rop"][i];
				}
			}
			
			if (type === "rop") {
				$id("load-page-permutation").style.display = "none";
			} else {
				$id("load-page-permutation-casing").style.display = "none";
			}
		} else {
			var suff = ["b", "1", "2", "3"];
			for (var i = 0; i < suff.length; ++i) {
				console.log("Here is the output");
				console.log($id("analysis-rop-afe-day-" + suff[i]).value);
				console.log(commafy(output["given"]["afe"][i]));
				$id("analysis-" + type + "-afe-day-" + suff[i]).value = commafy(output["given"]["afe"][i]);
				$id("analysis-" + type + "-rop-day-" + suff[i]).value = commafy(output["given"]["total-rop"][i]);
			}
			console.log(output);
			if (type === "rop") {
				$id("load-page-permutation").style.display = "none";
			} else {
				$id("load-page-permutation-casing").style.display = "none";
			}
		}
	}

	var data = getValues();
	data["rockbits_input"] = rockbitsInput();
	sendRequest(URL_COMPUTE_AFE_COSTS + "/" + type, data, callback);
}

// function computeAFECostsDepth() {
// 	$id("load-page-permutation-casing").style.display = "block";

// 	function callback(output) {
// 		var phases = ["sh", "ih", "dh", "ph1", "ph2"];
// 		var outPhases = ["surface", "intermediate", "prodn-casing", "prodn-liner-1", "prodn-liner-2"];
// 		console.log(output)
// 		var suff = ["1", "2"];
// 		for (var i = 0; i < suff.length; ++i) {
// 			for (var j = 0; j < phases.length; ++j) {
// 				$id("analysis-cd-" + phases[j] + "-afe-" + suff[i]).value = commafy(output[outPhases[j]]["afe"][i]);
// 				$id("analysis-cd-" + phases[j] + "-afe-" + suff[i]).title = tooltipHelper(output, outPhases, i, j);
// 				$id("analysis-cd-" + phases[j] + "-trop-" + suff[i]).value = output[outPhases[j]]["total-rop"][i];
// 			}
// 		}
// 		$id("load-page-permutation-casing").style.display = "none";
// 	}

// 	var data = getValues();
// 	sendRequest(URL_COMPUTE_AFE_COSTS, data, callback);
// }

function holeCasing() {
	$id("load-page-main").style.display = "inline-block";
	function callback(output) {
		phases = ["sh", "ih", "dh", "ph1", "ph2", "ph3", "reline"];
		outids = ["surface", "intermediate", "prodn_casing", "prodn_liner_1", "prodn_liner_2", "prodn_liner_3", "reline"];
		groups = ["hole-size", "case-size", "hole-depth", "case-id", "hole-length"];

		for (var j = 0; j < groups.length; ++j) {
			for (var i = 0; i < phases.length; ++i) {
				console.log(phases[i] + "-" + groups[j]);
				console.log($id(phases[i] + "-" + groups[j]).value);
				$id(phases[i] + "-" + groups[j]).value = output[groups[j]][outids[i]]
			}
		}
		$id("load-page-main").style.display = "none";
		console.log("Leaving ----");
	}

	var data = getValues();
	sendRequest(URL_HOLE_CASING, data, callback);
}

function tooltipHelper(output, phases, i, j) {
	sh = "SH = " + output[phases[j]]["drlg-days"]["Scenario " + i]["surface"] + "; ";
	ih = "IH = " + output[phases[j]]["drlg-days"]["Scenario " + i]["intermediate"] + "; ";
	dh = "DH = " + output[phases[j]]["drlg-days"]["Scenario " + i]["prodn_casing"] + "; ";
	p1 = "PH1 = " + output[phases[j]]["drlg-days"]["Scenario " + i]["prodn_liner_1"] + "; ";
	p2 = "PH2 = " + output[phases[j]]["drlg-days"]["Scenario " + i]["prodn_liner_2"] + "; ";
	td = "DD = " + drlgDays(output, phases, i, j) + "; ";
	fd = "FD = " + flatDays() + ";";
	
	return sh + ih + dh + p1 + p2 + td + fd;
}

function drlgDays(output, phases, i, j) {
	var ids = ["surface", "intermediate", "prodn_casing", "prodn_liner_1", "prodn_liner_2"];
	var sum = 0;
	for (var k = 0; k < ids.length; ++k) {
		sum += output[phases[j]]["drlg-days"]["Scenario " + i][ids[k]];
	}

	return sum;
}

function flatDays() {
	var ids = ["surface", "intermediate", "production_casing", "production_liner_1", "production_liner_2"];
	var sum = 0;
	for (var i = 0; i < ids.length; ++i) {
		sum += parseInt($id(ids[i] + "_FLAT").value);
	}

	return sum;
}

function computeBaslineROP() {

	$id("load-page-permutation").style.display = "block";

	var incrementRop = checkerHelper("analysis-base-rop-inc");

	function callback(output) {
		var suff = ["b", "1", "2", "3"];

		for (i = 0; i < suff.length; ++i) {
			$id("analysis-rop-sh-inc-" + suff[i]).value = Math.ceil(output["surface"]) + parseInt(suff[i] == "b" ? 0 : incrementRop * i);
			$id("analysis-rop-ih-inc-" + suff[i]).value = Math.ceil(output["intermediate"]) + parseInt(suff[i] == "b" ? 0 : incrementRop * i);
			$id("analysis-rop-dh-inc-" + suff[i]).value = Math.ceil(output["prodn_casing"]) + parseInt(suff[i] == "b" ? 0 : incrementRop * i);
			$id("analysis-rop-ph1-inc-" + suff[i]).value = Math.ceil(output["prodn_liner_1"]) + parseInt(suff[i] == "b" ? 0 : incrementRop * i);
			$id("analysis-rop-ph2-inc-" + suff[i]).value = Math.ceil(output["prodn_liner_2"]) + parseInt(suff[i] == "b" ? 0 : incrementRop * i);
		}
		
		$id("load-page-permutation").style.display = "none";
	}
	var data = getValues();
	sendRequest(URL_COMPUTE_BASELINE_ROP, data, callback);
}

function checkerHelper(id) {
		
	var incrementTable = $id(id);
	var incrTableRows = incrementTable.children[1].children;

	var incrTableChecker = new Array();
	for (var i = 0; i < incrTableRows[0].children.length; ++i) {
		var innerChecker = new Array();
		for (var j = 0; j < incrTableRows.length; ++j) {
			innerChecker[j] = incrTableRows[j].children[i].children[0].value == "" ? 0 : 1;
		}
		incrTableChecker[i] = innerChecker;
	}

	Array.prototype.sum = function () {
		var rowSums = [];
		for (var i = 0; i < this.length; ++i) {
			rowSums[i] = this[i].reduce(function(previous, current) {
				return previous + current;
			});
		}
		return rowSums;
	}

	if (id === "analysis-base-rop-inc") {
		var label = "ROP"; var val = "10"
	} else if (id === "analysis-base-cd-inc") {
		label = "Depth"; var val = "100"
	}
	if (incrTableChecker.sum()[0] > 0 && incrTableChecker.sum()[0] != incrTableChecker[0].length) {
		alert("Complete your input in " + label + "1 per Section for all rows, given " + incrTableChecker.sum()[0] + " input(s) only, expected " + incrTableChecker[0].length + " inputs. Otherwise, leave it blank.");
	} else if (incrTableChecker.sum()[1] > 0 && incrTableChecker.sum()[1] != incrTableChecker[1].length) {
		alert("Complete your input in " + label + "2 per Section for all rows, given " + incrTableChecker.sum()[1] + " input(s) only, expected " + incrTableChecker[0].length + " inputs. Otherwise, leave it blank.");
	} else if (incrTableChecker.sum()[2] > 0 && incrTableChecker.sum()[2] != incrTableChecker[2].length) {
		alert("Complete your input in " + label + "3 per Section for all rows, given " + incrTableChecker.sum()[2] + " input(s) only, expected " + incrTableChecker[0].length + " inputs. Otherwise, leave it blank.");
	} else {
		return prompt("Enter increment for each " + label, val);
	}

}

function computeBaseDaysROP() {
	$id("load-page-permutation").style.display = "block";	

	function callback(output) {
		var suff = ["b", "1", "2", "3"];
		for (i = 0; i < suff.length; ++i) {
			$id("analysis-rop-sh-day-" + suff[i]).value = Math.ceil(output["rop-" + suff[i]]["surface"]);
			$id("analysis-rop-ih-day-" + suff[i]).value = Math.ceil(output["rop-" + suff[i]]["intermediate"]);
			$id("analysis-rop-dh-day-" + suff[i]).value = Math.ceil(output["rop-" + suff[i]]["prodn_casing"]);
			$id("analysis-rop-ph1-day-" + suff[i]).value = Math.ceil(output["rop-" + suff[i]]["prodn_liner_1"]);
			$id("analysis-rop-ph2-day-" + suff[i]).value = Math.ceil(output["rop-" + suff[i]]["prodn_liner_2"]);
		}
		$id("load-page-permutation").style.display = "none";	
	}

	var data = getValues();
	sendRequest(URL_COMPUTE_BASELINE_DAYS, data, callback);
}

function roundUp(num, precision) {
	precision = Math.pow(10, precision)
	return Math.ceil(num * precision) / precision
}

function targetROPEtc() {
	$id("load-page-main").style.display = "inline-block";
	function callback(output) {
		$id("total_days").value = output["total_days"]
		$id("drilling_days").value = output["drilling_days"]
		$id("target_rop").value = output["target_rop"]
		$id("load-page-main").style.display = "none";
		console.log("Leaving ----");
	}
	
	var data = getValues();
	sendRequest(URL_TARGET_ROP_ETC, data, callback);
}

function rockbitsInput() {
	var table = $id("rockbits_input");
	var rows = table.children[1].children;

	var col1 = [];
	var col2 = [];
	var col3 = [];
	var col4 = [];
	var col5 = [];
	var out = {};
	for (var i = 0; i < rows.length; ++i) {
		col1.push(rows[i].children[0].innerHTML + " " + rows[i].children[1].innerHTML);
		col2.push(rows[i].children[2].children[0].value);
		col3.push(rows[i].children[3].children[0].value);
		col4.push(rows[i].children[4].children[0].value);
		col5.push(rows[i].children[5].children[0].value);
	}
				
	out["Rockbits"] = col1
	out["PROG SMITH"] = col2
	out["ON-STOCK QTY1"] = col3
	out["PROG HUGHES"] = col4
	out["ON-STOCK QTY2"] = col5

	return out
	// console.log(out);

	// sendRequest(URL_ROCKBITS_INPUT, out, () => console.log("send request for rockbits input."));
}

function computeCoverSheetValues(filePath = ""){
	var data = getValues();
	data["rockbits_input"] = rockbitsInput();

	if (filePath !== null || filePath !== "") {
		data["export_cover_cost_file_path"] = filePath
		console.log("file path is " + data["export_cover_cost_file_path"]);
	}

	function callback(output) {
		for (var i = 0; i < coverSheetColumns.length; i++) {
			if (coverSheetColumns[i] in output) value = output[coverSheetColumns[i]];
				else value = 0.00
	
			$id(coverSheetColumns[i]).innerHTML = commafy(value);
		} 
		document.getElementById("load-page-cover-sheet").style.display = "none";
	}

	sendRequest(URL_COVER_SHEET, data, callback);
}

function computeCostDetailsValues(filePath = "") {
	console.log("You clicked the cost details button");
	var data = getValues();
	data["rockbits_input"] = rockbitsInput();

	if (filePath !== null || filePath !== "") {
		data["export_cover_cost_file_path"] = filePath
		console.log("file path is " + data["export_cover_cost_file_path"]);
	}
	console.log("Here is the filepath: " + data["export_cover_cost_file_path"]);
	function callback(output) {
		var tableNames = ["fuels", "fuels_qty", "lubricants", "mud_and_chemicals", "mud_and_chemicals_qty", 
			"cements_and_additives", "cements_and_additives_qty", "smith", "hughes", "drilling_supplies", 
			"drilling_supplies_qty", "casings", "casings_qty", "wellhead", "wellhead_qty", "cementing_services", 
			"cementing_services_qty", "directional_drilling_services", "directional_drilling_services_qty", 
			"mud_engineering", "mud_engineering_qty", "aerated_drilling", "aerated_drilling_qty", "jars_and_shock_tools", "jars_and_shock_tools_qty",
			"chf_welding_services", "chf_welding_services_qty", "mud_logging_services", "mud_logging_services_qty", 
			"casing_running_services", "casing_running_services_qty", "drilling_rig_services", "drill_pipes", 
			"drill_pipes_qty", "completion_test_wireline", "completion_test_wireline_qty",
			"other_cementing_services", "other_cementing_services_qty", "handling_hauling_towing",
			"equipment_rental", "equipment_rental_qty", "rig_allocated_charges"];
		var tableIDs   = ["fuel_cost_details_cost", "fuel_cost_details_qty", "lubricant_cost_details_cost", 
			"mud_chemicals_cost_details_cost", "mud_chemicals_cost_details_qty", "cement_cost_details_cost", 
			"cement_cost_details_qty", "rockbits_cost_details_smith_cost", "rockbits_cost_details_hughes_cost", 
			"drilling_supplies_cost_details_cost", "drilling_supplies_cost_details_qty", "casing_cost_details_cost", 
			"casing_cost_details_qty", "wellhead_cost_details_cost", "wellhead_cost_details_qty", "cementing_services_cost_details_cost", 
			"cementing_services_cost_details_qty", "directional_drilling_cost_details_cost", "directional_drilling_cost_details_qty",
			"mud_engineering_cost", "mud_engineering_qty", "aerated_drilling_cost", "aerated_drilling_qty", "jars_and_shock_cost", "jars_and_shock_qty",
			"chf_installation_cost", "chf_installation_qty", "mud_logging_services_cost", "mud_logging_services_qty", 
			"casing_running_services_cost", "casing_running_services_qty", "drilling_rig_services_cost", "drill_pipes_cost", "drill_pipes_qty", "completion_test_cost", "completion_test_qty",
			"other_cementing_services_cost", "other_cementing_services_qty", "handling_hauling_cost",
			"equipmental_rental_cost", "equipmental_rental_qty", "rig_allocated_charges_cost"];

		for (var k = 0; k < tableNames.length; ++k) {
			console.log("processing " + tableNames[k]);
			populateTable(tableNames[k], tableIDs[k], output);
			console.log("done processing " + tableNames[k]);
			console.log("index is " + k);
		}

		fillTotals();
		// fuelCosts();
		// lubricantsCosts();
		document.getElementById("load-page-cover-sheet").style.display = "none";
	}
	console.log(data);
	sendRequest(URL_COST_DETAILS, data, callback);
	// console.log(output["fuels"]);
}

function fuelCosts() {
	for (var i = 0; i < $id("fuel_cost_details_qty").children[1].children.length; ++i) {
		$id("fuel-qty-item" + i).value = 1
	}
	for (var i = 0; i < $id("fuel_cost_details_cost").children[1].children.length - 1; ++i) {
		$id("fuel-cost-item" + i).value = $id("diesel_php_us").value
	}
}

function lubricantsCosts() {
	if ($id("rig").value === "Rig 5") {
		$id("lubricant-cost-item0").value = 5 / 100.
	} else {
		$id("lubricant-cost-item0").value = 0 / 100.	
	}
}

function fuelCostQty() {
	/*
	Handles Fuel Costs and Quantities
	*/
	
	// fuel quantities
	for (var i = 0; i < $id("fuel_cost_details_qty").children[1].children.length; ++i) {
		$id("fuel-qty-item" + i).value = 1
	}

	// fuel cost
	// i upper limit must be subtracted by 1 since there is no total for the costs
	for (var i = 0; i < $id("fuel_cost_details_cost").children[1].children.length - 1; ++i) {
		$id("fuel-cost-item" + i).value = $id("diesel_php_us").value
	}

	function callback() {
		console.log("Done!");
	}

	sendRequest(URL_FUEL_COST, data, callback);
}

function cementAdditiveCosts(output) {
	/*
	Handles Computation of Cement Additive Costs
	*/	

	for (var i = 0; i < output.length; ++i) {
		$id("cement-additives-cost-item" + i).value = output[i];
	}
}

function rockbitsCosts(output) {
	/*
	Handles Computation of Rockbits Costs
	*/

	for (var i = 0; i < output[0].length; ++i) {
		$id("rockbits-smith-cost-item" + i).value = output[0][i];
	}

	for (var i = 0; i < output[1].length; ++i) {
		$id("rockbits-hughes-cost-item" + i).value = output[1][i];
	}
}

function drillingSuppliesCosts(output) {
	/*
	Handles Computation of Drilling Supplies
	*/
	for (var i = 0; i < output.length; ++i) {
		$id("drilling-supplies-cost-item" + i).value = output[i];
	}
}

function wellheadCosts(output) {
	/*
	Handles Computation of the Wellhead Costs
	*/
	for (var i = 0; i < output.length; ++i) {
		$id("wellhead-cost-item" + i).value = output[i];
	}
}

function cementingServicesCosts(output) {
	/*
	Handles Computation of Cementing Services Costs
	*/
	for (var i = 0; i < output.length; ++i) {
		$id("cementing-services-cost-item" + i).value = output[i];
	}
}

function directionalDrillingCosts(output) {
	/*
	Handles Computationo of Quantity and Costs of directional drilling
	*/
	for (var i = 0; i < output[0].length; ++i) {
		$id("directional-drilling-qty-item" + i).value = output[0][i];
	}

	for (var i = 0; i < output[1].length; ++i) {
		$id("directional-drilling-cost-item" + i).value = output[1][i];
	}
}

function mudEngineeringCosts(output) {
	/*
	Handles Computation of Mud Engineering Costs and Quantity
	*/
	$id("mud-engineering-qty-item0").value = output[0];
	$id("mud-engineering-cost-item0").value = output[1];
}

function aeratedDrillingCosts(output) {
	/*
	Handles Computation of Aerated Drilling
	*/
	for (var i = 0; i < output.length; ++i) {
		$id("aerated-drilling-cost-item" + i).value = output[i];
	}
}

function jarsShockCosts(output) {
	/*
	Handles Computation of Jars and Shock
	*/	
	for (var i = 0; i < output.length; ++i) {
		$id("jars-shock-cost-item" + i).value = output[i];
	}
}

function chfCosts(output) {
	/*
	Handles Computation of CHF Installation
	*/
	for (var i = 0; i < output.length; ++i) {
		$id("chf-installation-cost-item" + i).value = output[i];
	}
}

function mudLoggingCosts(output) {
	/*
	Handles Computation of Mud Logging Costs
	*/
	for (var i = 0; i < output.length; ++i) {
		$id("mud-logging-cost-item" + i).value = output[i];
	}
}

function casingRunningCosts(output) {
	/*
	Handles Computation of Casing Running Services Costs
	*/
	$id("casing-running-cost-item0").value = output[0];
}

function drillingRigCosts(output) {
	/*
	Handles Computation of Drilling Rig Services Costs
	*/
	for (var i = 0; i < output.length; ++i) {
		if (i === 7) {
			console.log("skipping " + i);
		} else {
			$id("drilling-rig-cost-item" + i).value = output[i];
		}
	}
}

function drillPipesCosts(output) {
	/*
	Handles Computation of Drill Pipes
	*/
	for (var i = 0; i < output[0].length; ++i) {
		$id("drill-pipes-qty-item" + i).value = output[0][i];
	}

	for (var i = 0; i < output[1].length; ++i) {
		$id("drill-pipes-cost-item" + i).value = output[1][i];		
	}
}

function completionTestCosts(output) {
	/*
	Handles Computation of Completion Test Cost
	*/
	for (var i = 0; i < output[0].length; ++i) {
		$id("completion-test-cost-item" + i).value = output[0][i];
	}
}

function otherCementingCosts(output) {
	/*
	Handles Computation of Other Cementing Services Cost
	*/
	$id("other-cementing-services-cost-item0").value = output;
}

function equipmentalRentalCosts(output) {
	/*
	Handles Computation of Equipmental Rental Costs
	*/
	console.log("You are here!");
	console.log(output);
	for (var i = 0; i < output[0].length; ++i) {
		$id("equipmental-rental-qty-item" + i).value = output[0][i];
	}

	for (var i = 0; i < output[1].length; ++i) {
		$id("equipmental-rental-cost-item" + i).value = output[1][i];		
	}
}

function baselineCostsHelper(type) {
	/*
	Handles Computation of Baseline Costs

	Arguments:
		type: string - default 'fuel', type of the tables/item.
					 - options are the following:
						 * fuel
						 * lubricants
						 * cement_additives
						 * 
	*/
	var data = getValues();

	function callback(output, type) {
		if (type === "fuel") {
			fuelCosts();
		} else if (type === "lubricants") {
			lubricantsCosts();
		} else if (type === "cement_additives") {
			cementAdditiveCosts(output);
		} else if (type === "rockbits") {
			rockbitsCosts(output);
		} else if (type === "drilling_supplies") {
			drillingSuppliesCosts(output);
		} else if (type === "wellhead") {
			wellheadCosts(output);
		} else if (type === "cementing_services") {
			cementingServicesCosts(output);
		} else if (type === "directional_drilling") {
			directionalDrillingCosts(output);
		} else if (type === "mud_engineering") {
			mudEngineeringCosts(output);
		} else if (type === "aerated_drilling") {
			aeratedDrillingCosts(output);
		} else if (type === "jars_shock") {
			jarsShockCosts(output);
		} else if (type === "chf_installation") {
			chfCosts(output);
		} else if (type === "mud_logging") {
			mudLoggingCosts(output);
		} else if (type === "casing_running") {
			casingRunningCosts(output);
		} else if (type === "drilling_rig") {
			drillingRigCosts(output);
		} else if (type === "drill_pipes") {
			drillPipesCosts(output);
		} else if (type === "completion_test") {
			completionTestCosts(output);
		} else if (type === "other_cementing") {
			otherCementingCosts(output);
		} else if (type === "equipmental_rental") {
			equipmentalRentalCosts(output);
		}
		$id("load-page-main").style.display = "none";
		console.log("Leaving ----");
	}

	if (type === "fuel" || type === "lubricants") {
		callback({}, type);
	} else {
		sendRequest(URL_BASELINE_COSTS + "/" + type, data, callback);
	}
}

function baselineCosts() {
	$id("load-page-main").style.display = "inline-block";
	var items = [
		"fuel", "lubricants", "cement_additives", "rockbits", "drilling_supplies", "wellhead", 
		"cementing_services", "directional_drilling", "mud_engineering", "aerated_drilling", "jars_shock",
		"chf_installation", "mud_logging", "casing_running", "drilling_rig", "drill_pipes", "completion_test",
		"other_cementing", "equipmental_rental"
	];

	for (var i = 0; i < items.length; ++i) {
		baselineCostsHelper(items[i]);
	}
}

function computeAllBaseline() {
	targetROPEtc();
	holeCasing();
	baselineCosts()
}

// function computePermutations() {
// 	var basicInputValues = getValues();
// 	var data = {};

// 	data["basicInputValues"] = basicInputValues;
// 	data["permutation"] = {};
// 	console.log(data)
// 	console.log(basicInputValues)
// 	console.log(permutationValues)

// 	//get permutation values from getValues.js
// 	for (var i = 0; i < permutationValues.length; i++) {
// 		data["permutation"][permutationValues[i]] = $val(permutationValues[i])
// 	}

// 	console.log(data);
// 	output = sendRequest(URL_PERMUTATION_COUNT, data);

// 	return output;
// }