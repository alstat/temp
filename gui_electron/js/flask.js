URL = "http://127.0.0.1:5000"

URL_TARGET_ROP_ETC = URL + "/compute_target_rop_etc"
URL_COMPUTE_BASELINE_ROP = URL + "/compute_baseline_rop"
URL_COMPUTE_BASELINE_DAYS = URL + "/compute_baseline_days"
URL_COMPUTE_BASELINE_DEPTH = URL + "/compute_baseline_depth"
URL_COMPUTE_AFE_COSTS = URL + "/compute_afe_costs"
URL_COVER_SHEET = URL + "/compute_cover_sheet"
URL_COST_DETAILS = URL + "/compute_cost_details"
URL_EXPORT_COVER_SHEET = URL + "/export_cover_sheet"
URL_PERMUTATION = URL + "/compute_permutation"
URL_PERMUTATION_COUNT = URL + "/get_permutations"
URL_TARGET_ROP = URL + "/compute_target_rop"
URL_HOLE_CASING = URL + "/compute_hole_casing"
URL_ROCKBITS_INPUT = URL + "/export_rockbits_input"
URL_BASELINE_COSTS = URL + "/compute_baseline_costs"
// URL_CEMENT_ADDITIVES_COST = URL + "/compute_cement_additives_cost"


function sendRequest(URL, data, callback) {
	console.log("Entering ----");
	$id("load-page-main").style.display = "inline-block";
	var xhr = new XMLHttpRequest();

	xhr.open("POST", URL, true);
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.send(JSON.stringify(data));
	xhr.onreadystatechange = function () {
		if (this.readyState === 4 && this.status === 200) {
			var output = JSON.parse(this.responseText);
			var pattern = /\//;
			var splitURL = URL.split(pattern);

			if (splitURL.length === 5) {
				var type = splitURL.slice(splitURL.length - 1)[0];
				callback(output, type);
			} else {
				callback(output);
			}
			$id("load-page-main").style.display = "none";
			console.log("Leaving ----");
		}
	}
}