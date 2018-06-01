//load on startup!
window.onload = function () {
	showDiv("main_div_panel", "main_div_basic_inputs");
	showDiv("div_panel", "div_main_inputs");

	loadTable("main_inputs", "casing_depth");
	loadTable("main_inputs", "other_inputs");
	loadTable("other_inputs", "inputs_1");
	loadTable("rockbits_input", "rockbits_input");

	loadTable("other_inputs", "hole_case_asmpt");
	loadTable("other_inputs", "other_hole_case_asmpt");
	loadTable("other_inputs", "casing_id");
	loadTable("other_inputs", "cement_acid");
	loadTable("other_inputs", "tpwsri");

	loadTable("hole_casing_summary", "hole_casing_summary");

	loadTable("drilling_schedule", "drilling_schedule");

	loadTable("cover_sheet", "cover_sheet_1");
	loadTable("cover_sheet", "cover_sheet_2");
	loadTable("cover_sheet", "cover_sheet_3");

	loadTable("permutation", "analysis-base-rop");
	loadTable("permutation", "analysis-base-rop-inc");

	loadTable("permutation", "analysis-base-rop-days");
	loadTable("permutation", "analysis-rop-afe");
	loadTable("permutation", "analysis-base-rop-given");

	loadTable("permutation_casing_depth", "analysis-base-cd");
	loadTable("permutation_casing_depth", "analysis-base-cd-inc");
	loadTable("permutation_casing_depth", "analysis-base-cd-days");
	loadTable("permutation_casing_depth", "analysis-cd-afe");
	loadTable("permutation_casing_depth", "analysis-base-casing-given");

	// loadTable("output", "output");\]
	
	loadTable("cost_details/fuel", "fuel_cost_details_qty");
	loadTable("cost_details/fuel", "fuel_cost_details_cost");
	
	loadTable("cost_details/lubricant", "lubricant_cost_details_cost");
	
	loadTable("cost_details/mud_chemicals", "mud_chemicals_cost_details_qty");
	loadTable("cost_details/mud_chemicals", "mud_chemicals_cost_details_cost");
	
	loadTable("cost_details/cement", "cement_cost_details_qty");
	loadTable("cost_details/cement", "cement_cost_details_cost");
	
	loadTable("cost_details/rockbits", "rockbits_cost_details_smith_cost");
	loadTable("cost_details/rockbits", "rockbits_cost_details_hughes_cost");
	
	loadTable("cost_details/drilling_supplies", "drilling_supplies_cost_details_qty");
	loadTable("cost_details/drilling_supplies", "drilling_supplies_cost_details_cost");
	
	loadTable("cost_details/casing", "casing_cost_details_qty");
	loadTable("cost_details/casing", "casing_cost_details_cost");
	
	loadTable("cost_details/wellhead", "wellhead_cost_details_qty");
	loadTable("cost_details/wellhead", "wellhead_cost_details_cost");

	loadTable("cost_details/cementing_services", "cementing_services_cost_details_qty");
	loadTable("cost_details/cementing_services", "cementing_services_cost_details_cost");
	
	loadTable("cost_details/directional_drilling", "directional_drilling_cost_details_qty");
	loadTable("cost_details/directional_drilling", "directional_drilling_cost_details_cost");
	
	loadTable("cost_details/mud_engineering", "mud_engineering_qty");
	loadTable("cost_details/mud_engineering", "mud_engineering_cost");
	
	loadTable("cost_details/aerated_drilling", "aerated_drilling_qty");
	loadTable("cost_details/aerated_drilling", "aerated_drilling_cost");

	loadTable("cost_details/jars_and_shock", "jars_and_shock_qty");
	loadTable("cost_details/jars_and_shock", "jars_and_shock_cost");

	loadTable("cost_details/chf_installation", "chf_installation_qty");
	loadTable("cost_details/chf_installation", "chf_installation_cost");

	loadTable("cost_details/mud_logging_services", "mud_logging_services_qty");
	loadTable("cost_details/mud_logging_services", "mud_logging_services_cost");

	loadTable("cost_details/casing_running_services", "casing_running_services_qty");
	loadTable("cost_details/casing_running_services", "casing_running_services_cost");

	loadTable("cost_details/drilling_rig_services", "drilling_rig_services_cost");

	loadTable("cost_details/drill_pipes", "drill_pipes_qty");
	loadTable("cost_details/drill_pipes", "drill_pipes_cost");

	loadTable("cost_details/completion_test", "completion_test_qty");
	loadTable("cost_details/completion_test", "completion_test_cost");

	loadTable("cost_details/other_cementing_services", "other_cementing_services_qty");
	loadTable("cost_details/other_cementing_services", "other_cementing_services_cost");

	loadTable("cost_details/equipmental_rental", "equipmental_rental_qty");
	loadTable("cost_details/equipmental_rental", "equipmental_rental_cost");

	loadTable("cost_details/handling_hauling", "handling_hauling_cost");

	loadTable("cost_details/rig_allocated_charges", "rig_allocated_charges_cost");

	loadTable("output", "output-surface");
	loadTable("output", "output-intermediate");
	loadTable("output", "output-prodn_casing");
	loadTable("output", "output-prodn_liner_1");
	loadTable("output", "output-prodn_liner_2");

	calcFormulas();

	// load_permutation_button_handler();

	//load chart values in Drilling schedule
	initDualAxis("chart-header");
	loadChartData();
	
	// $id("surface_DRLG").oninput = targetROP()
	// $id("intermediate_DRLG").oninput = targetROP()
	// $id("production_casing_DRLG").oninput = targetROP()
	// $id("production_liner_1_DRLG").oninput = targetROP()
	// $id("production_liner_2_DRLG").oninput = targetROP()
	// $id("production_liner_3_DRLG").oninput = targetROP()
	
	// $id("surface_FLAT").oninput = targetROP()
	// $id("intermediate_FLAT").oninput = targetROP()
	// $id("production_casing_FLAT").oninput = targetROP()
	// $id("production_liner_1_FLAT").oninput = targetROP()
	// $id("production_liner_2_FLAT").oninput = targetROP()
	// $id("production_liner_3_FLAT").oninput = targetROP()
	// var dat = rowNames();
	// console.log(dat);	
}