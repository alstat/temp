DATE_CONSTANT = 24 * 60 * 60 * 1000;

//var commafy = require("commafy");
var coverSheetColumns = getCoverSheetValues();
var permutationValues = getPermutationValues();

function calcFormulas() {
	// add onchange listeners to
	setListenerDrillSchedule();

	// additional formulas to compute before loading
	computeDrillSchedule();
}

function setListenerDrillSchedule(){
	rows = ($id("drilling_schedule").rows);
	mytable = $id("drilling_schedule");

	rows[1].children[1].children[0].addEventListener("change", function (evt) {
		computeDrillSchedule();
	});
	rows[1].children[3].children[0].addEventListener("change", function (evt) {
		computeDrillSchedule();}
	);
	rows[1].children[2].children[0].readOnly = true;

	for (var i = 2; i < rows.length; i++) {
		rows[i].children[3].children[0].addEventListener("change", function (evt) {
			computeDrillSchedule();
		});
		rows[i].children[1].children[0].readOnly = true;
		rows[i].children[2].children[0].readOnly = true;
	}
}

function computeDrillSchedule() {
	rows = ($id("drilling_schedule").rows);
	rows[1].children[2].children[0].value = addDays(rows[1].children[1].children[0].id, rows[1].children[3].children[0].id);

	for (var i = 2; i < rows.length; i++) {
		rows[i].children[1].children[0].value = nextDay(rows[i-1].children[2].children[0].id);
		rows[i].children[2].children[0].value = addDays(rows[i].children[1].children[0].id, rows[i].children[3].children[0].id);
	}
}

function addDays(startDay, duration) {
	// no values (blank); return empty value
	if ($val(duration) == "") return "";
	try {
		newDate = new Date(new Date(Date.parse($val(startDay))).getTime() + ($val(duration)-1) * DATE_CONSTANT);
	} catch(err) {
		alert("error"); 
		return ""
	}
	if (isNaN(newDate)) return "";

	month = parseInt(newDate.getMonth()) + 1
	month = month < 9 ? "0" + month : month;

	day = parseInt(newDate.getDate())
	day =  day < 9 ? "0" + day : day;

	output =  month + "/" + day + "/" + newDate.getFullYear() ;

	return output;
}

function nextDay(startDay){

	// no values (blank); return empty value
	if($val(startDay) == "") return "";

	newDate = new Date(new Date(Date.parse($val(startDay))).getTime() + 1 * DATE_CONSTANT);

	month = parseInt(newDate.getMonth()) + 1
	month = month < 9 ? "0" + month : month;

	day = parseInt(newDate.getDate())
	day =  day < 9 ? "0" + day : day;

	output =  month + "/" + day + "/" + newDate.getFullYear() ;

	return output;
}

function commafy(value) {
    var str = value.toString().split(".");
    if (str[0].length >= 5) {
        str[0] = str[0].replace(/(\d)(?=(\d{3})+$)/g, "$1,");
    }
    if (str[1] && str[1].length >= 5) {
        str[1] = str[1].replace(/(\d{3})/g, "$1 ");
    }
    return str.join(".").split(" ")[0];
}
