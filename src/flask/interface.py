import numpy as np
import pandas as pd
import os
import sys
import itertools 
#from sqlalchemy.sql.functions import random

sys.path.insert(0, ".")

dt_dir = "./src/flask/data"

from edc_assumptions import Assumptions
from edc_source import Analysis, Drilling_Days, Hole_Casing, Unit_Rate, Cost_Center, header

def inputs(data, drlg_days = None):

    global drlg_input, flat_input, basic_input, casing_depth_input, assumptions

    if drlg_days is None:
        drlg_input = {
            "surface"       : 0 if data["surface_DRLG"] == "" else float(data["surface_DRLG"]),
            "intermediate"  : 0 if data["intermediate_DRLG"] == "" else float(data["intermediate_DRLG"]),
            "prodn_casing"  : 0 if data["production_casing_DRLG"] == "" else float(data["production_casing_DRLG"]),
            "prodn_liner_1" : 0 if data["production_liner_1_DRLG"] == "" else float(data["production_liner_1_DRLG"]),
            "prodn_liner_2" : 0 if data["production_liner_2_DRLG"] == "" else float(data["production_liner_2_DRLG"]),
            "prodn_liner_3" : 0 if data["production_liner_3_DRLG"] == "" else float(data["production_liner_3_DRLG"]),
            "reline"        : 0 if data["reline_DRLG"] == "" else float(data["reline_DRLG"])
        }
    else:
        drlg_input = drlg_days

    flat_input = {
        "surface"       : 0 if data["surface_FLAT"] == "" else float(data["surface_FLAT"]), 
        "intermediate"  : 0 if data["intermediate_FLAT"] == "" else float(data["intermediate_FLAT"]),
        "prodn_casing"  : 0 if data["production_casing_FLAT"] == "" else float(data["production_casing_FLAT"]),
        "prodn_liner_1" : 0 if data["production_liner_1_FLAT"] == "" else float(data["production_liner_1_FLAT"]),
        "prodn_liner_2" : 0 if data["production_liner_2_FLAT"] == "" else float(data["production_liner_2_FLAT"]),
        "prodn_liner_3" : 0 if data["production_liner_3_FLAT"] == "" else float(data["production_liner_3_FLAT"]),
        "reline"        : 0 if data["reline_FLAT"] == "" else float(data["reline_FLAT"])
        }
  
    basic_input = {
        "well_name"                       : str(data["well_name"]), #*
        "rig"                             : str(data["rig"]), # choices: "Rig 1", "Rig 2", "Rig 5", "Rig 12"
        "target_depth"                    : float(data["target_depth"]),   #*
        "rh_or_bh"                        : str(data["rh_bh"]), # choices: "Regular Hole", "Big Hole"
        "double_liner"                    : False if data["double_liner"] == "No" else True,
        "aerated_surface"                 : False if data["aerated_surface"] == "No" else True,
        "aerated_intermediate"            : False if data["aerated_production_intermediate"] == "No" else True,
        "aerated_prodn_casing"            : False if data["aerated_production_casing"] == "No" else True,
        "aerated_prodn_liner_1"           : False if data["aerated_production_liner_1"] == "No" else True,
        "aerated_prodn_liner_2"           : False if data["aerated_production_liner_2"] == "No" else True,
        "regular_bottom_section_for_bh"   : False if data["reg_bottom_bh"] == "No" else True,
        "rent_drill_pipes"                : False if data["rent_drill_pipes"] == "No" else True,
        "mob/demob_drillpipes"            : str(data["mob_demob_drillpipes"]),
        "no_of_Joints"                    : float(data["no_of_joints"]),
        "yes_if_without_pre-installed_csg": False if data["yes_wo_preinstalled_casing"] == "No" else True,
        "prodn_liner_3"                   : False if data["prod_liner_3"] == "No" else True,
        "interisland_rig_move"            : False if data["interisland_rigmove"] == "No" else str(data["interisland_rigmove"]),
        "b23"                             : False,
        "project_loc"                     : str(data["project_location"]), # choices: "BGBU", "LGBU", "NIGBU", "MAGBU"
        "rig_move_from"                   : str(data["rig_move_from"]), # choices: "PROJECT", "PAD", "SAME PAD"
        "rig_move_days"                   : float(data["rig_move_days"]),
        "dhv_1"                           : False if data["dhv_1"] == "No" else True,
        "dhv_2"                           : float(data["dhv_2"]),
        "pwd_fliner1"                     : False if data["pwd_fliner_1"] == "No" else True,
        "pwd_fliner2"                     : False if data["pwd_fliner_2"] == "No" else True,
        "chf"                             : str(data["chf"]), # choices: "DESCO", "TESCO"
        "mud_logging"                     : False if data["mud_logging"] == "No" else True,
        "fe_fliner1"                      : False if data["formation_eval_fliner_1"] == "No" else True,
        "fe_fliner2"                      : False if data["formation_eval_fliner_2"] == "No" else True,
        "reline"                          : False if data["reline"] == "No" else True,
        "forex_ph_us"                     : float(data["forex_php_us"]),
        "diesel_ph_us"                    : float(data["diesel_php_us"])
    }

    hole_case_sizes_asmpt = {
        "hole"  : {
            "bh" : {
                "surface"       : 0 if data["hole_bh_surface"] == "" else float(data["hole_bh_surface"]),
                "intermediate"  : 0 if data["hole_bh_intermediate"] == "" else float(data["hole_bh_intermediate"]),
                "prodn_casing"  : 0 if data["hole_bh_prodn_casing"] == "" else float(data["hole_bh_prodn_casing"]),
                "prodn_liner_1" : 0 if data["hole_bh_prodn_liner_1"] == "" else float(data["hole_bh_prodn_liner_1"]),
                "prodn_liner_2" : 0 if data["hole_bh_prodn_liner_2"] == "" else float(data["hole_bh_prodn_liner_2"]),
                "prodn_liner_3" : 0 if data["hole_bh_prodn_liner_3"] == "" else float(data["hole_bh_prodn_liner_3"]),
            },
            "rh" : {
                "surface"       : 0 if data["hole_rh_surface"] == "" else float(data["hole_rh_surface"]),
                "intermediate"  : 0 if data["hole_rh_intermediate"] == "" else float(data["hole_rh_intermediate"]),
                "prodn_casing"  : 0 if data["hole_rh_prodn_casing"] == "" else float(data["hole_rh_prodn_casing"]),
                "prodn_liner_1" : 0 if data["hole_rh_prodn_liner_1"] == "" else float(data["hole_rh_prodn_liner_1"]),
                "prodn_liner_2" : 0 if data["hole_rh_prodn_liner_2"] == "" else float(data["hole_rh_prodn_liner_2"]),
                "prodn_liner_3" : 0 if data["hole_rh_prodn_liner_3"] == "" else float(data["hole_rh_prodn_liner_3"]),
            }
        },
        "case" : {
            "bh" : {
                "surface"       : 0 if data["case_bh_surface"] == "" else float(data["case_bh_surface"]),
                "intermediate"  : 0 if data["case_bh_intermediate"] == "" else float(data["case_bh_intermediate"]),
                "prodn_casing"  : 0 if data["case_bh_prodn_casing"] == "" else float(data["case_bh_prodn_casing"]),
                "prodn_liner_1" : 0 if data["case_bh_prodn_liner_1"] == "" else float(data["case_bh_prodn_liner_1"]),
                "prodn_liner_2" : 0 if data["case_bh_prodn_liner_2"] == "" else float(data["case_bh_prodn_liner_2"]),
                "prodn_liner_3" : 0 if data["case_bh_prodn_liner_3"] == "" else float(data["case_bh_prodn_liner_3"]),
            },
            "rh" : {
                "surface"       : 0 if data["case_rh_surface"] == "" else float(data["case_rh_surface"]),
                "intermediate"  : 0 if data["case_rh_intermediate"] == "" else float(data["case_rh_intermediate"]),
                "prodn_casing"  : 0 if data["case_rh_prodn_casing"] == "" else float(data["case_rh_prodn_casing"]),
                "prodn_liner_1" : 0 if data["case_rh_prodn_liner_1"] == "" else float(data["case_rh_prodn_liner_1"]),
                "prodn_liner_2" : 0 if data["case_rh_prodn_liner_2"] == "" else float(data["case_rh_prodn_liner_2"]),
                "prodn_liner_3" : 0 if data["case_rh_prodn_liner_3"] == "" else float(data["case_rh_prodn_liner_3"])
            }
        }
    }

    other_hole_case_asmpt = {
        "hole" : {
            "surface"       : 0 if data["other_hole_asmpt_surface"] == "" else float(data["other_hole_asmpt_surface"]),
            "intermediate"  : 0 if data["other_hole_asmpt_intermediate"] == "" else float(data["other_hole_asmpt_intermediate"]),
            "prodn_casing"  : 0 if data["other_hole_asmpt_prodn_casing"] == "" else float(data["other_hole_asmpt_prodn_casing"]),
            "prodn_liner_1" : 0 if data["other_hole_asmpt_prodn_liner_1"] == "" else float(data["other_hole_asmpt_prodn_liner_1"]),
            "prodn_liner_2" : 0 if data["other_hole_asmpt_prodn_liner_2"] == "" else float(data["other_hole_asmpt_prodn_liner_2"]),
            "prodn_liner_3" : 0 if data["other_hole_asmpt_prodn_liner_3"] == "" else float(data["other_hole_asmpt_prodn_liner_3"]),
            "no_label_1"    : 0 if data["other_hole_asmpt_no_label_1"] == "" else float(data["other_hole_asmpt_no_label_1"]),
            "no_label_2"    : 0 if data["other_hole_asmpt_no_label_2"] == "" else float(data["other_hole_asmpt_no_label_2"]),
            "no_label_3"    : 0 if data["other_hole_asmpt_no_label_3"] == "" else float(data["other_hole_asmpt_no_label_3"])
        },
        "case" : {
            "surface"       : 0 if data["other_case_asmpt_surface"] == "" else float(data["other_case_asmpt_surface"]),
            "intermediate"  : 0 if data["other_case_asmpt_intermediate"] == "" else float(data["other_case_asmpt_intermediate"]),
            "prodn_casing"  : 0 if data["other_case_asmpt_prodn_casing"] == "" else float(data["other_case_asmpt_prodn_casing"]),
            "prodn_liner_1" : 0 if data["other_case_asmpt_prodn_liner_1"] == "" else float(data["other_case_asmpt_prodn_liner_1"]),
            "prodn_liner_2" : 0 if data["other_case_asmpt_prodn_liner_2"] == "" else float(data["other_case_asmpt_prodn_liner_2"]),
            "prodn_liner_3" : 0 if data["other_case_asmpt_prodn_liner_3"] == "" else float(data["other_case_asmpt_prodn_liner_3"]),
            "no_label_1"    : 0 if data["other_case_asmpt_no_label_1"] == "" else float(data["other_case_asmpt_no_label_1"]),
            "no_label_2"    : 0 if data["other_case_asmpt_no_label_2"] == "" else float(data["other_case_asmpt_no_label_2"]),
            "no_label_3"    : 0 if data["other_case_asmpt_no_label_3"] == "" else float(data["other_case_asmpt_no_label_3"])
        },
        "id" : {
            "surface"       : 0 if data["other_id_asmpt_surface"] == "" else float(data["other_id_asmpt_surface"]),
            "intermediate"  : 0 if data["other_id_asmpt_intermediate"] == "" else float(data["other_id_asmpt_intermediate"]),
            "prodn_casing"  : 0 if data["other_id_asmpt_prodn_casing"] == "" else float(data["other_id_asmpt_prodn_casing"]),
            "prodn_liner_1" : 0 if data["other_id_asmpt_prodn_liner_1"] == "" else float(data["other_id_asmpt_prodn_liner_1"]),
            "prodn_liner_2" : 0 if data["other_id_asmpt_prodn_liner_2"] == "" else float(data["other_id_asmpt_prodn_liner_2"]),
            "prodn_liner_3" : 0 if data["other_id_asmpt_prodn_liner_3"] == "" else float(data["other_id_asmpt_prodn_liner_3"]),
            "no_label_1"    : 0 if data["other_id_asmpt_no_label_1"] == "" else float(data["other_id_asmpt_no_label_1"]),
            "no_label_2"    : 0 if data["other_id_asmpt_no_label_2"] == "" else float(data["other_id_asmpt_no_label_2"]),
            "no_label_3"    : 0 if data["other_id_asmpt_no_label_3"] == "" else float(data["other_id_asmpt_no_label_3"])
        }
    }
    
    casing_depth_input = {
        "surface"       : 0 if data["casing_surface"] == "" else float(data["casing_surface"]),
        "intermediate"  : 0 if data["casing_intermediate"] == "" else float(data["casing_intermediate"]),
        "prodn_casing"  : 0 if data["casing_production"] == "" else float(data["casing_production"]),
        "prodn_liner_1" : 0 if data["casing_production_liner_1"] == "" else float(data["casing_production_liner_1"]),
        "prodn_liner_2" : 0 if data["casing_production_liner_2"] == "" else float(data["casing_production_liner_2"]),
        "prodn_liner_3" : 0 if data["casing_production_liner_3"] == "" else float(data["casing_production_liner_3"]),
        "reline"        : 0 if data["casing_reline"] == "" else float(data["casing_reline"])
    }

    casing_id = {
        "bh" : {
            "surface"       : 0 if data["casing_id_bh_surface"] == "" else float(data["casing_id_bh_surface"]),
            "intermediate"  : 0 if data["casing_id_bh_intermediate"] == "" else float(data["casing_id_bh_intermediate"]),
            "prodn_casing"  : 0 if data["casing_id_bh_prodn_casing"] == "" else float(data["casing_id_bh_prodn_casing"]),
            "prodn_liner_1" : 0 if data["casing_id_bh_prodn_liner_1"] == "" else float(data["casing_id_bh_prodn_liner_1"]),
            "prodn_liner_2" : 0 if data["casing_id_bh_prodn_liner_2"] == "" else float(data["casing_id_bh_prodn_liner_2"]),
            "prodn_liner_3" : 0 if data["casing_id_bh_prodn_liner_3"] == "" else float(data["casing_id_bh_prodn_liner_3"]),
            "reline"        : 0 if data["casing_id_bh_reline"] == "" else float(data["casing_id_bh_reline"])
        },
        "rh" : {
            "surface"       : 0 if data["casing_id_rh_surface"] == "" else float(data["casing_id_rh_surface"]),
            "intermediate"  : 0 if data["casing_id_rh_intermediate"] == "" else float(data["casing_id_rh_intermediate"]),
            "prodn_casing"  : 0 if data["casing_id_rh_prodn_casing"] == "" else float(data["casing_id_rh_prodn_casing"]),
            "prodn_liner_1" : 0 if data["casing_id_rh_prodn_liner_1"] == "" else float(data["casing_id_rh_prodn_liner_1"]),
            "prodn_liner_2" : 0 if data["casing_id_rh_prodn_liner_2"] == "" else float(data["casing_id_rh_prodn_liner_2"]),
            "prodn_liner_3" : 0 if data["casing_id_rh_prodn_liner_3"] == "" else float(data["casing_id_rh_prodn_liner_3"]),
            "reline"        : 0 if data["casing_id_rh_reline"] == "" else float(data["casing_id_rh_reline"])
        }
    }

    cement_acid = {
        "cement" : {
            "surface"       : 0 if data["surface_cement_plug"] == "" else float(data["surface_cement_plug"]),
            "intermediate"  : 0 if data["intermediate_cement_plug"] == "" else float(data["intermediate_cement_plug"]),
            "prodn_casing"  : 0 if data["production_casing_cement_plug"] == "" else float(data["production_casing_cement_plug"]),
            "prodn_liner_1" : 0 if data["production_liner_1_cement_plug"] == "" else float(data["production_liner_1_cement_plug"]),
            "prodn_liner_2" : 0 if data["production_liner_2_cement_plug"] == "" else float(data["production_liner_2_cement_plug"]),
            "prodn_liner_3" : 0 if data["production_liner_3_cement_plug"] == "" else float(data["production_liner_3_cement_plug"])
        },
        "acid" : {
            "surface"       : False if data["acid_surface"] == "No" else None if data["acid_surface"] == "" else True,
            "intermediate"  : False if data["acid_intermediate"] == "No" else None if data["acid_intermediate"] == "" else True,
            "prodn_casing"  : False if data["acid_prodn_casing"] == "No" else None if data["acid_prodn_casing"] == "" else True,
            "prodn_liner_1" : False if data["acid_prodn_liner_1"] == "No" else None if data["acid_prodn_liner_1"] == "" else True,
            "prodn_liner_2" : False if data["acid_prodn_liner_2"] == "No" else None if data["acid_prodn_liner_2"] == "" else True,
            "prodn_liner_3" : False if data["acid_prodn_liner_3"] == "No" else None if data["acid_prodn_liner_3"] == "" else True
        },
        "top_job" : {
            "surface"       : 0 if data["surface_top_job"] == "" else float(data["surface_top_job"]),
            "intermediate"  : 0 if data["intermediate_top_job"] == "" else float(data["intermediate_top_job"]),
            "prodn_casing"  : 0 if data["production_casing_top_job"] == "" else float(data["production_casing_top_job"]),
            "prodn_liner_1" : 0 if data["production_liner_1_top_job"] == "" else float(data["production_liner_1_top_job"]),
            "prodn_liner_2" : 0 if data["production_liner_2_top_job"] == "" else float(data["production_liner_2_top_job"]),
            "prodn_liner_3" : 0 if data["production_liner_3_top_job"] == "" else float(data["production_liner_3_top_job"])
        }
    }

    # # Other Assumptions
    # tpwsri = {
    #     "Average ROP Day Rate" : None if data["tpwsri_ave_rop_rate"] == "" else float(data["tpwsri_ave_rop_rate"]),
    #     "Base Day Rate" : None if data["tpwsri_base_day_rate"] == "" else float(data["tpwsri_base_day_rate"]),
    #     "Standby Rate" : None if data["tpwsri_standby_rate"] == "" else float(data["tpwsri_standby_rate"]),
    #     "Move Fee" : None if data["tpwsri_movefee"] == "" else float(data["tpwsri_movefee"]),
    #     "Rig Move Rate" :  None if data["tpwsri_rigmove_rate"] == "" else float(data["tpwsri_rigmove_rate"]),
    #     "Additional Payment" : None if data["tpwsri_additional_payment"] == "" else float(data["tpwsri_additional_payment"]),
    #     "Penalty Payment" : None if data["tpwsri_penalty_payment"] == "" else float(data["tpwsri_penalty_payment"]),
    #     "Well Bonus" : None if data["tpwsri_well_bonus"] == "" else float(data["tpwsri_well_bonus"]),
    #     "Well ROP Bonus" : None if data["tpwsri_well_rop_bonus"] == "" else float(data["tpwsri_well_rop_bonus"])
    # }

    # hole_case_sizes_asmpt = {
    #     "hole": {
    #         "bh": {
    #             "surface": 32,
    #             "intermediate": 23,
    #             "prodn_casing": 17,
    #             "prodn_liner_1": 12.25,
    #             "prodn_liner_2":  9.875,
    #             "prodn_liner_3":  7.875,
    #         },
    #         "rh": {
    #             "surface": 26,
    #             "intermediate": 17,
    #             "prodn_casing": 12.25,
    #             "prodn_liner_1":  8.5,
    #             "prodn_liner_2":  6,
    #             "prodn_liner_3": np.nan,
    #         }
    #     },
    #     "case": {
    #         "bh": {
    #             "surface": 26,
    #             "intermediate": 18.625,
    #             "prodn_casing": 13.375,
    #             "prodn_liner_1": 10.75,
    #             "prodn_liner_2":  8.625,
    #             "prodn_liner_3":  7.,
    #         },
    #         "rh": {
    #             "surface": 20,
    #             "intermediate": 13.375,
    #             "prodn_casing":  9.625,
    #             "prodn_liner_1":  7,
    #             "prodn_liner_2":  5,
    #             "prodn_liner_3": np.nan,
    #         }
    #     }
    # }

    # other_hole_case_asmpt = {
    #     "hole": {
    #         "surface": 32,
    #         "intermediate": 23,
    #         "prodn_casing": 17,
    #         "prodn_liner_1": 12.25,
    #         "prodn_liner_2": 12.25,
    #         "prodn_liner_3": 9.875,
    #         "no_label_1": 7.875,
    #         "no_label_2": 8.5,
    #         "no_label_3": 6
    #     },
    #     "case": {
    #         "surface": 26,
    #         "intermediate": 18.625,
    #         "prodn_casing": 13.375,
    #         "prodn_liner_1": 10.75,
    #         "prodn_liner_2":  9.625,
    #         "prodn_liner_3":  8.625,
    #         "no_label_1":  7,
    #         "no_label_2":  7,
    #         "no_label_3":  5
    #     },
    #     "id": {
    #         "surface": 24.5,
    #         "intermediate": 17.467,
    #         "prodn_casing": 12.415,
    #         "prodn_liner_1": 10.05,
    #         "prodn_liner_2":  8.755,
    #         "prodn_liner_3":  8.097,
    #         "no_label_1":  6.366,
    #         "no_label_2":  6.276,
    #         "no_label_3":  4.408
    #     }
    # }

    # casing_depth_input = {
    #     "surface":  100,
    #     "intermediate":  560,
    #     "prodn_casing": 1260,
    #     "prodn_liner_1": 1900,
    #     "prodn_liner_2": 2500,
    #     "prodn_liner_3": np.nan,
    #     "reline": np.nan
    # }

    # casing_id = {
    #     "bh": {
    #         "surface": 24.5,
    #         "intermediate": 17.467,
    #         "prodn_casing": 12.415,
    #         "prodn_liner_1": 10.05,
    #         "prodn_liner_2":  8.097,
    #         "prodn_liner_3":  6.366,
    #         "reline": np.nan
    #     },
    #     "rh": {
    #         "surface": 19.312,
    #         "intermediate": 12.615,
    #         "prodn_casing":  8.755,
    #         "prodn_liner_1":  6.276,
    #         "prodn_liner_2":  4.408,
    #         "prodn_liner_3": np.nan,
    #         "reline": np.nan
    #     }
    # }

    # cement_acid = {
    #     "cement": {
    #         "surface": 1,
    #         "intermediate": 1,
    #         "prodn_casing": 1,
    #         "prodn_liner_1": 1,
    #         "prodn_liner_2": 1,
    #         "prodn_liner_3": np.nan,
    #     },
    #     "acid": {
    #         "surface": False,
    #         "intermediate": False,
    #         "prodn_casing": False,
    #         "prodn_liner_1": None,
    #         "prodn_liner_2": None,
    #         "prodn_liner_3": None,
    #     },
    #     "top_job": {
    #         "surface": 1,
    #         "intermediate": 1,
    #         "prodn_casing": 1,
    #         "prodn_liner_1": 0,
    #         "prodn_liner_2": 0,
    #         "prodn_liner_3": 0,
    #     }
    # }

    # Other Assumptions
    tpwsri = {
        "Average ROP Day Rate": None,
        "Base Day Rate": 1596000,
        "Standby Rate": 1449000,
        "Move Fee": 16721000.00,
        "Rig Move Rate":  20748000.00,
        "Additional Payment": 16105885.68,
        "Penalty Payment": None,
        "Well Bonus": 2000000.00,
        "Well ROP Bonus": None
    }
    """
    Assumptions
    """

    assumptions = [
        hole_case_sizes_asmpt,
        other_hole_case_asmpt,
        casing_depth_input,
        casing_id,
        cement_acid,
        tpwsri
    ]

def compute_inputs(data, drlg_days = None):
    inputs(data, drlg_days)

    basic_input["total_days"]         = basic_input["rig_move_days"] + Drilling_Days(drlg_input, flat_input).total()
    basic_input["drilling_days"]      = Drilling_Days(drlg_input, flat_input).cell(basic_input)
    basic_input["target_rop"]         = Drilling_Days(drlg_input, flat_input).target_rop(basic_input)
    basic_input["drilling_row_total"] = Drilling_Days(drlg_input, flat_input).row_total()

def import_excels():
    global transhipment, handling_hauling, transhipment_drillpipes, depreciation, insurance, service_fee, genex
    global wellname, inter_island, rigmove_cost, cement_slb_asmpt2, tpwsi_rr_rigs, average_rop_day_rate, rig1_peripherals, meals_accommodations
    global rigmove, equipment, chf, inventory, fuel_rawdf, cemt_asmpt, ada_cost, rigmove_daily, mud_consumables
    global mdeg_asmpt, rig_move2_asmpt, rig_move1_asmpt

    transhipment            = pd.read_excel(dt_dir + "/transhipment.xlsx")
    handling_hauling        = pd.read_excel(dt_dir + "/handling_hauling.xlsx")
    transhipment_drillpipes = pd.read_excel(dt_dir + "/transhipment_drillpipes.xlsx")
    depreciation            = pd.read_excel(dt_dir + "/depreciation.xlsx")
    insurance               = pd.read_excel(dt_dir + "/insurance.xlsx")
    service_fee             = pd.read_excel(dt_dir + "/service_fee.xlsx")
    genex                   = pd.read_excel(dt_dir + "/genex.xlsx")
    wellname                = pd.read_excel(dt_dir + "/wellname.xlsx")
    inter_island            = pd.read_excel(dt_dir + "/inter_island_cost.xlsx")
    rigmove_cost            = pd.read_excel(dt_dir + "/rigmove_cost.xlsx")
    cement_slb_asmpt2       = pd.read_excel(dt_dir + "/equipmental_rentals.xlsx")
    tpwsi_rr_rigs           = pd.read_excel(dt_dir + "/tpwsi_rr_rigs.xlsx")
    average_rop_day_rate    = pd.read_excel(dt_dir + "/average_rop_day_rate.xlsx")
    rig1_peripherals        = pd.read_excel(dt_dir + "/rig1peripherals.xlsx")
    meals_accommodations    = pd.read_excel(dt_dir + "/meals_accommodations.xlsx")
    rigmove                 = pd.read_excel(dt_dir + "/rigmove.xlsx")
    equipment               = pd.read_excel(dt_dir + "/equipment_rates.xlsx")
    chf                     = pd.read_excel(dt_dir + "/chf.xlsx").set_index("Index")

    inventory               = pd.read_excel(dt_dir + "/inventory.xlsx")
    fuel_rawdf              = pd.read_excel(dt_dir + "/fuel.xlsx")

    cemt_asmpt              = pd.read_excel(dt_dir + "/cement_additives.xlsx").set_index("Index")

    ada_cost                = pd.read_excel(dt_dir + "/ada_cost.xlsx")
    rigmove_daily           = pd.read_excel(dt_dir + "/rigmovedaily.xlsx")
    mud_consumables         = pd.read_excel(dt_dir + "/mud_consumables.xlsx")
    
    mdeg_asmpt              = pd.read_excel(dt_dir + "/mud_engr.xlsx").set_index("Standard Flatspots")
    rig_move1_asmpt         = pd.read_excel(dt_dir + "/rig_move.xlsx")

    return False

def compute_cover_sheet(data, output, details = False, drlg_days = None):
    """
    Implementation of Excel"s ROUNDUP function
    """

    rig_move2_asmpt         = pd.read_excel(dt_dir + "/equipment.xlsx")
    import_excels()

    def roundup(x, y = 1):
        if isinstance(x, int) or isinstance(x, float):
            if x > 0:
                return np.ceil(np.ceil(x) / y) * y
            elif x < 0:
                return np.floor(np.floor(x) / y) * y
            else:
                return 0
        elif isinstance(x, np.ndarray) or isinstance(x, pd.core.series.Series):
            out = np.zeros(len(x)); j = 0
            for i in x:
                if i > 0:
                    out[j] = np.ceil(np.ceil(i) / y) * y
                elif i < 0:
                    out[j] = np.floor(np.floor(i) / y) * y
                else:
                    out[j] = 0
                j += 1
            return out
        else:
            raise ValueError("%d is not of type int, float, or numpy.ndarray, check your input." % x)

    print "Compute cover sheet request"
    
    # compute_inputs(data, drlg_days)
    # print "drlg_input before"
    # print drlg_input

    inputs(data, drlg_days)

    # print "drlg_input after"
    # print drlg_input
    basic_input["total_days"]         = basic_input["rig_move_days"] + Drilling_Days(drlg_input, flat_input).total()
    basic_input["drilling_days"]      = Drilling_Days(drlg_input, flat_input).cell(basic_input)
    basic_input["target_rop"]         = Drilling_Days(drlg_input, flat_input).target_rop(basic_input)
    basic_input["drilling_row_total"] = Drilling_Days(drlg_input, flat_input).row_total()

    # output["total_days"]              = basic_input["total_days"]
    # output["drilling_days"]           = basic_input["drilling_days"]
    # output["target_rop"]              = basic_input["target_rop"]

    cement_slb = Assumptions(basic_input, assumptions)
    cemt = cement_slb.cement_slb(data)
    # print os.listdir("./src/flask/data")
    fuel_asmpt      = fuel_rawdf.ix[0:6, 4:13]
    if basic_input["double_liner"]:
        fuel_asmpt      = fuel_rawdf.ix[0:6, 4:15]
    else:
        fuel_asmpt      = fuel_rawdf.ix[0:6, 4:13]
    
    # rckb_asmpt      = pd.read_excel(dt_dir + "/rockbit_1.xlsx").set_index("Rockbits")

    rockbits_dict = {}
    rockbits_dict["Rockbits"] = data["rockbits_input"]["Rockbits"]
    rockbits_dict["PROG SMITH"]    = [0 if data["rockbits_input"]["PROG SMITH"][i] == "" else float(data["rockbits_input"]["PROG SMITH"][i]) for i in np.arange(len(data["rockbits_input"]["PROG SMITH"]))]
    rockbits_dict["ON-STOCK QTY1"] = [0 if data["rockbits_input"]["ON-STOCK QTY1"][i] == "" else float(data["rockbits_input"]["ON-STOCK QTY1"][i]) for i in np.arange(len(data["rockbits_input"]["ON-STOCK QTY1"]))]
    rockbits_dict["PROG HUGHES"]   = [0 if data["rockbits_input"]["PROG HUGHES"][i] == "" else float(data["rockbits_input"]["PROG HUGHES"][i]) for i in np.arange(len(data["rockbits_input"]["PROG HUGHES"]))]
    rockbits_dict["ON-STOCK QTY2"] = [0 if data["rockbits_input"]["ON-STOCK QTY2"][i] == "" else float(data["rockbits_input"]["ON-STOCK QTY2"][i]) for i in np.arange(len(data["rockbits_input"]["ON-STOCK QTY2"]))]
    
    print("###############################")
    print("Converted Values of Prog SMITH")
    print(rockbits_dict)
    
    rckb_asmpt      = pd.DataFrame(rockbits_dict)
    cols = ["Rockbits", "PROG SMITH", "ON-STOCK QTY1", "PROG HUGHES", "ON-STOCK QTY2"]
    rckb_asmpt      = rckb_asmpt[cols]
    rckb_asmpt      = rckb_asmpt.set_index("Rockbits")

    # rckb_unit_scost = np.array(Unit_Rate(basic_input, inventory).rockbits().ix[:, "smith_unit_cost"])
    # rckb_unit_hcost = np.array(Unit_Rate(basic_input, inventory).rockbits().ix[:, "hughes_unit_cost"])
    
    # if basic_input["project_loc"] == "LGBU":
    #     rckb_unit_scost = pd.read_excel(dt_dir + "/rockbit.xlsx").SMITH.values
    #     rckb_unit_hcost = pd.read_excel(dt_dir + "/rockbit.xlsx").HUGHES.values
    # elif basic_input["project_loc"] == "BGBU":
    #     rckb_unit_scost = [1120775.21, 1875294.22, 1058281.27, 1058281.27, 0, 1987152.27, 528683.95, 0, 661020.76, 0, 671510.73, 2029318.35, 423365.88, 0, 502514.32, 567685.23, 1372382.14, 318297.98, 0, 1068633.72, 278670.71, 288234.05, 330605.94, 0, 216414.14, 0, 211888.74, 246265.65]
    #     rckb_unit_hcost = [1120775.21, 1911879.73, 2112234.91, 1334750.81, 1034690.92, 1987152.27, 414438.21, 0.00, 764997.09, 1433412.29, 1901141.67, 1863890.11, 0.00, 1424401.99, 1413994.59, 1301189.19, 1834568.31, 0.00, 763760.06, 0.00, 252716.80, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    # elif basic_input["project_loc"] == "NIGBU":
    #     rckb_unit_scost = [1120775.21, 1892317.88, 1078414.46, 1078414.46, 0, 1984033.59, 532151.31, 0, 660856.15, 0, 664642.25, 1955126.10, 423365.88, 0, 505816.78, 567685.23, 1592178.06, 318297.98, 0, 1137462.36, 278670.71, 288234.05, 330605.94, 0, 221149.22, 0, 211888.74, 246265.65]
    #     rckb_unit_hcost = [1120775.21, 1909133.62, 2112234.91, 1224652.41, 1029200.31, 1984033.59, 414438.21, 0.00, 764997.09, 1433412.29, 1901141.67, 1863890.11, 0.00, 1424401.99, 1413994.59, 1301189.19, 1834568.31, 0.00, 763760.06, 0.00, 252716.80, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    # elif basic_input["project_loc"] == "MAGBU":
    #     rckb_unit_scost = [1120775.21, 1827487.10, 1058281.27, 1058281.27, 0, 1021682.90, 532151.31, 0, 660856.15, 0, 668996.60, 1973405.93, 423365.88, 0, 505816.78, 567685.23, 1411371.64, 318297.98, 0, 1137462.36, 278670.71, 288234.05, 330605.94, 0, 216414.14, 0, 211888.74, 246265.65]
    #     rckb_unit_hcost = [1120775.21, 1916182.32, 2112234.91, 1334750.81, 1034690.92, 1021682.90, 414438.21, 0.00, 764997.09, 1433412.29, 1920511.90, 1863890.11, 0.00, 1424401.99, 1413994.59, 1301189.19, 1590109.70, 0.00, 763760.06, 0.00, 252716.80, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

    # rckb_unit_scost = pd.read_excel(dt_dir + "/rockbit.xlsx").SMITH.values
    # rckb_unit_hcost = pd.read_excel(dt_dir + "/rockbit.xlsx").HUGHES.values
    rckb_qty        = {}.fromkeys(rckb_asmpt.index, False)
    for i in np.arange(16, 19):
        rckb_qty[list(rckb_qty.keys())[i]] = True

    if basic_input["project_loc"] == "LGBU":
        wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead.xlsx")
        # wlhd_last_row           = 103558.77 
    elif basic_input["project_loc"] == "BGBU":
        wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead_BGBU.xlsx")
        # wlhd_last_row           =  103934.64     
    elif basic_input["project_loc"] == "NIGBU":
        wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead_NIGBU.xlsx")
        # wlhd_last_row           =  104122.57     
    elif basic_input["project_loc"] == "MAGBU":
        wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead_MAGBU.xlsx")
        # wlhd_last_row           =  103934.64 

    # np.append(cost, wlhd_last_row)
    # wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead.xlsx")
    rig_move1_asmpt.ix[0, 2 + np.where(rig_move1_asmpt.ix[:, 2:].columns.values == basic_input["rig"].upper())[0][0]]
    rig_move2_asmpt         = rig_move2_asmpt.ix[:, 1:].set_index(rig_move2_asmpt.Equipment)
    rig_move2_asmpt.ix[rig_move2_asmpt.index.values == "50T CRANE", 4]

    if basic_input["project_loc"] == "LGBU":
        big_hole                = pd.read_excel(dt_dir + "/big_hole.xlsx")
        reg_hole                = pd.read_excel(dt_dir + "/regular_hole.xlsx")
    elif basic_input["project_loc"] == "BGBU":
        big_hole                = pd.read_excel(dt_dir + "/big_hole_BGBU.xlsx")
        reg_hole                = pd.read_excel(dt_dir + "/regular_hole_BGBU.xlsx")
    elif basic_input["project_loc"] == "NIGBU":
        big_hole                = pd.read_excel(dt_dir + "/big_hole_NIGBU.xlsx")
        reg_hole                = pd.read_excel(dt_dir + "/regular_hole_NIGBU.xlsx")
    elif basic_input["project_loc"] == "MAGBU":
        big_hole                = pd.read_excel(dt_dir + "/big_hole_MAGBU.xlsx")
        reg_hole                = pd.read_excel(dt_dir + "/regular_hole_MAGBU.xlsx")

    # big_hole                = pd.read_excel(dt_dir + "/big_hole.xlsx")
    # reg_hole                = pd.read_excel(dt_dir + "/regular_hole.xlsx")
    big_hole.ix[ 0, 3] = roundup(Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["surface"] / 11.5) + 3
    big_hole.ix[ 2, 3] = roundup(big_hole.ix[0, 3] / 4.) + 1
    big_hole.ix[ 7, 3] = roundup(Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["intermediate"] / 11.5) + 3
    big_hole.ix[10, 3] = roundup(big_hole.ix[0, 3] / 3.) + 2
    big_hole.ix[11, 3] = roundup((big_hole.ix[7, 3] - big_hole.ix[0, 3]) / 3.) + 3.
    big_hole.ix[16, 3] = roundup(Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["prodn_casing"] / 11.5) + 3
    big_hole.ix[20, 3] = roundup(big_hole.ix[7, 3] / 3.) + 2
    big_hole.ix[21, 3] = roundup((big_hole.ix[16, 3] - big_hole.ix[7, 3]) / 3.) + 3.
    big_hole.ix[26, 3] = roundup((Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["prodn_liner_1"] - Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["prodn_casing"]) / 11.5) + 3
    big_hole.ix[33, 3] = roundup((Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["prodn_liner_2"] - Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["prodn_liner_1"]) / 11.5) + 3
    big_hole.ix[36, 3] = big_hole.ix[26, 3]
    big_hole.ix[43, 3] = big_hole.ix[33, 3]

    reg_hole.ix[ 0, 3] = roundup(Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["surface"] / 11.5) + 3
    reg_hole.ix[ 2, 3] = roundup(reg_hole.ix[0, 3] / 4.) + 1
    reg_hole.ix[ 7, 3] = roundup(Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["intermediate"] / 11.5) + 3
    reg_hole.ix[10, 3] = roundup(reg_hole.ix[0, 3] / 3.) + 2
    reg_hole.ix[11, 3] = roundup((reg_hole.ix[7, 3] - reg_hole.ix[0, 3]) / 3.) + 3.
    reg_hole.ix[16, 3] = roundup(Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["prodn_casing"] / 11.5) + 3
    reg_hole.ix[20, 3] = roundup(reg_hole.ix[7, 3] / 3.) + 2
    reg_hole.ix[21, 3] = roundup((reg_hole.ix[16, 3] - reg_hole.ix[7, 3]) / 3.) + 3.
    reg_hole.ix[26, 3] = roundup((Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["prodn_liner_1"] - Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)["prodn_casing"]) / 11.5) + 3

    # usage of data and output variables
    # refer to EDC Variable Listing - for output key values.. Defaults to 0 if no value provided here
    # IMPORTANT! make sure to convert data variable to numeric type if needed!

    # sample examples...
    head = header(basic_input, assumptions, data, drlg_input, flat_input)
    fuel_costs = [float(data["fuel_cost_item" + str(i)]) for i in np.arange(6)]
    mudchem_costs = [float(data["mudchemicals_cost_item" + str(i)]) for i in np.arange(29)]
    cement_costs = [float(data["cement_additives_cost_item" + str(i)]) for i in np.arange(11)]
    rockbits_smith_costs = [0.0 if data["rockbits_smith_cost_item" + str(i)] == "" else float(data["rockbits_smith_cost_item" + str(i)]) for i in np.arange(28)]
    rockbits_hughes_costs = [0.0 if data["rockbits_hughes_cost_item" + str(i)] == "" else float(data["rockbits_hughes_cost_item" + str(i)]) for i in np.arange(28)]
    drilling_supplies_costs = np.array([0 if data["drilling_supplies_cost_item" + str(i)] == "" else float(data["drilling_supplies_cost_item" + str(i)]) for i in np.arange(2)], dtype = "int")
    wellhead_costs = [0.0 if data["wellhead_cost_item" + str(i)] == "" else float(data["wellhead_cost_item" + str(i)]) for i in np.arange(5)]
    cement_services_costs = [0.0 if data["cementing_services_cost_item" + str(i)] == "" else float(data["cementing_services_cost_item" + str(i)]) for i in np.arange(13)]
    directional_drilling_qty = [0.0 if data["directional_drilling_qty_item" + str(i)] == "" else float(data["directional_drilling_qty_item" + str(i)]) for i in np.arange(32)]
    directional_drilling_costs = [0.0 if data["directional_drilling_cost_item" + str(i)] == "" else float(data["directional_drilling_cost_item" + str(i)]) for i in np.arange(32)]
    mud_engineering_qty = 0.0 if data["mud_engineering_qty_item0"] == "" else float(data["mud_engineering_qty_item0"])
    mud_engineering_costs = 0.0 if data["mud_engineering_cost_item0"] == "" else float(data["mud_engineering_cost_item0"])
    aerated_drilling_costs = [0.0 if data["aerated_drilling_cost_item" + str(i)] == "" else float(data["aerated_drilling_cost_item" + str(i)]) for i in np.arange(21)]
    jars_shock_qty = [0.0 if data["jars_shock_qty_item" + str(i)] == "" else float(data["jars_shock_qty_item" + str(i)]) for i in np.arange(6)]
    jars_shock_costs = [0.0 if data["jars_shock_cost_item" + str(i)] == "" else float(data["jars_shock_cost_item" + str(i)]) for i in np.arange(6)]
    chf_costs = [0.0 if data["chf_installation_cost_item" + str(i)] == "" else float(data["chf_installation_cost_item" + str(i)]) for i in np.arange(9)]
    mud_logging_costs = [0.0 if data["mud_logging_cost_item" + str(i)] == "" else float(data["mud_logging_cost_item" + str(i)]) for i in np.arange(2)]
    casing_running_cost = 0.0 if data["casing_running_cost_item0"] == "" else float(data["casing_running_cost_item0"])
    
    drilling_rig_costs = np.zeros(10)
    for i in np.arange(10):
        if i == 7:
            drilling_rig_costs[i] = 0
        else:
            if data["drilling_rig_cost_item" + str(i)] == "":
                drilling_rig_costs[i] = 0
            else:
                drilling_rig_costs[i] = float(data["drilling_rig_cost_item" + str(i)])

    drill_pipes_qty = [0.0 if data["drill_pipes_qty_item" + str(i)] == "" else float(data["drill_pipes_qty_item" + str(i)]) for i in np.arange(4)]
    drill_pipes_costs = [0.0 if data["drill_pipes_cost_item" + str(i)] == "" else float(data["drill_pipes_cost_item" + str(i)]) for i in np.arange(4)]
    completion_test_costs = [0.0 if data["completion_test_cost_item" + str(i)] == "" else float(data["completion_test_cost_item" + str(i)]) for i in np.arange(2)]
    other_cementing_cost = 0.0 if data["other_cementing_services_cost_item0"] == "" else float(data["other_cementing_services_cost_item0"])
    equipmental_qty = [0.0 if data["equipmental_rental_qty_item" + str(i)] == "" else float(data["equipmental_rental_qty_item" + str(i)]) for i in np.arange(7)]
    equipmental_costs = [0.0 if data["equipmental_rental_cost_item" + str(i)] == "" else float(data["equipmental_rental_cost_item" + str(i)]) for i in np.arange(7)]

    print(drilling_rig_costs)
    
    if details is True:
        output["fuels"]                         = Cost_Center(basic_input, assumptions, head).fuel(fuel_asmpt, drlg_input, flat_input, unit_cost = fuel_costs)##.to_json(orient = "records")
        output["lubricants"]                    = Cost_Center(basic_input, assumptions, head).lubricants(fuel_asmpt, drlg_input, flat_input, unit_cost = fuel_costs).ix[:, 1:]##.to_json(orient = "records")
        output["fuels_qty"]                     = Cost_Center(basic_input, assumptions, head).fuel(fuel_asmpt, drlg_input, flat_input)#.to_json(orient = "records")
    else:
        output["fuels"]                         = roundup(Cost_Center(basic_input, assumptions, head).fuel(fuel_asmpt, drlg_input, flat_input, unit_cost = list(np.repeat(30, 7))).sum().sum(), 1000)
        output["lubricants"]                    = roundup(Cost_Center(basic_input, assumptions, head).lubricants(fuel_asmpt, drlg_input, flat_input, unit_cost = fuel_costs).ix[:, 1:].sum().sum(), 1000)
    
    hole_depth                              = Hole_Casing(basic_input, data, category = "hole_depth").compute(assumptions)
    
    if details is True:
        output["mud_and_chemicals"]             = Cost_Center(basic_input, assumptions, head).mud_chemicals(mud_consumables, hole_depth, casing_depth_input, unit_cost = mudchem_costs).ix[:, 1:]#.to_json(orient = "records")
        output["mud_and_chemicals_qty"]         = Cost_Center(basic_input, assumptions, head).mud_chemicals(mud_consumables, hole_depth, casing_depth_input).ix[:, 1:]#.to_json(orient = "records")
    else:
        output["mud_and_chemicals"]             = roundup(Cost_Center(basic_input, assumptions, head).mud_chemicals(mud_consumables, hole_depth, casing_depth_input, unit_cost = mudchem_costs).ix[:, 1:].sum().sum(), 1000)
    
    # drlg_input["prodn_liner_2"]
    # if basic_input["rh_or_bh"] == "Big Hole":
    #     idx = list(cemt.index)[:len(list(cemt.index)) - 1] + [cement_slb_asmpt2.ix[5, "Equipment"]]
    # else:
    #     idx = list(cemt.index)[:len(list(cemt.index)) - 1] + [cement_slb_asmpt2.ix[7, "Equipment"]]

    # cement_cost = list(cemt.Price)[0:len(list(cemt.Price)) - 1] + list(cement_slb_asmpt2.ix[cement_slb_asmpt2.Equipment == idx[-1], "Unit Price, USD"])
    
    if details is True:
        output["cements_and_additives"]         = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2, unit_cost = cement_costs)#.to_json(orient = "records")
        output["cements_and_additives_qty"]     = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2)#.to_json(orient = "records")
        output["smith"]                         = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rockbits_smith_costs)#.to_json(orient = "records")
        output["hughes"]                        = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rockbits_hughes_costs, category = "HUGHES")#.to_json(orient = "records")
    else:
        output["cements_and_additives"]         = roundup(Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2, unit_cost = cement_costs).sum().sum(), 1000)
        smith                                   = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rockbits_smith_costs).sum().sum()
        hughes                                  = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rockbits_hughes_costs, category = "HUGHES").sum().sum()
        output["rockbits"]                      = roundup(smith + hughes, 1000)

    # if basic_input["rig"] == "Rig 1" or basic_input["rig"] == "Rig 2":
    #     cost_ds = np.array([0, 0], dtype = "int")
    # else:
    #     cost_ds = np.array([2000 * basic_input["forex_ph_us"], 6000 * basic_input["forex_ph_us"]], dtype = "int")
    
    if details is True:
        output["drilling_supplies"]             = Cost_Center(basic_input, assumptions, head).drilling_supplies(data, unit_cost = drilling_supplies_costs).ix[:, 1:]#.to_json(orient = "records")
        output["casings"]                       = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole, unit_cost = True).ix[:, 1:]#.to_json(orient = "records")
        output["drilling_supplies_qty"]         = Cost_Center(basic_input, assumptions, head).drilling_supplies(data, unit_cost = drilling_supplies_costs).ix[:, 1:]#.to_json(orient = "records")
        output["casings_qty"]                   = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole).ix[:, 1:]#.to_json(orient = "records")
    else:
        output["drilling_supplies"]             = roundup(Cost_Center(basic_input, assumptions, head).drilling_supplies(data, unit_cost = drilling_supplies_costs).ix[:, 1:].sum().sum(), 1000)
        output["casings"]                       = roundup(Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole, unit_cost = True).ix[:, 1:].sum().sum(), 1000)

    # if basic_input["rh_or_bh"] == "Big Hole":
    #     cost = wlhd_asmpt.ix[:, "Big Hole Unit cost"].values
    # else:
    #     cost = wlhd_asmpt.ix[:, "Regular Hole Unit cost"].values

    # if basic_input["pwd_fliner1"]:
    #     dd_qty = [2, 2, 4, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1]
    # else:
    #     dd_qty = [2, 2, 4, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1]
        
    # output of directional drilling total cost: 23,804,000 - 165,000
    if details is True:
        output["wellhead"]                      = Cost_Center(basic_input, assumptions, head).wellhead(wlhd_asmpt, unit_cost = wellhead_costs).ix[:, 1:]#.to_json(orient = "records")
        output["wellhead_qty"]                  = Cost_Center(basic_input, assumptions, head).wellhead(wlhd_asmpt).ix[:, 1:]#.to_json(orient = "records")
        output["cementing_services"]            = Cost_Center(basic_input, assumptions, head).cementing(unit_cost = cement_services_costs).ix[:, 1:]#.to_json(orient = "records")
        output["cementing_services_qty"]        = Cost_Center(basic_input, assumptions, head).cementing().ix[:, 1:]#.to_json(orient = "records")
        output["directional_drilling_services"] = Cost_Center(basic_input, assumptions, head).directional_drilling(transhipment, unit_cost = directional_drilling_costs, qty = directional_drilling_qty)#.to_json(orient = "records")
        output["directional_drilling_services_qty"] = Cost_Center(basic_input, assumptions, head).directional_drilling(transhipment, qty = directional_drilling_qty)#.to_json(orient = "records")
        output["mud_engineering"]               = Cost_Center(basic_input, assumptions, head).mud_engineering(qty = mud_engineering_qty, unit_cost =  mud_engineering_costs).ix[:, 1:]#.to_json(orient = "records")
        output["mud_engineering_qty"]           = Cost_Center(basic_input, assumptions, head).mud_engineering(qty = mud_engineering_qty).ix[:, 1:]#.to_json(orient = "records")
        output["aerated_drilling"]              = Cost_Center(basic_input, assumptions, head).aerated_drilling(ada_cost, drlg_input, flat_input, unit_cost = aerated_drilling_costs).ix[:, 1:]#.to_json(orient = "records")
        output["aerated_drilling_qty"]          = Cost_Center(basic_input, assumptions, head).aerated_drilling(ada_cost, drlg_input, flat_input).ix[:, 1:]#.to_json(orient = "records")
        output["jars_and_shock_tools"]          = Cost_Center(basic_input, assumptions, head).jars_shock(transhipment, drlg_input, qty = jars_shock_qty, unit_cost = jars_shock_costs).ix[:, 1:]#.to_json(orient = "records")
        output["jars_and_shock_tools_qty"]      = Cost_Center(basic_input, assumptions, head).jars_shock(transhipment, drlg_input, qty = jars_shock_qty).ix[:, 1:]#.to_json(orient = "records")
    else:
        output["wellhead"]                      = roundup(Cost_Center(basic_input, assumptions, head).wellhead(wlhd_asmpt, unit_cost = wellhead_costs).ix[:, 1:].sum().sum(), 1000)
        output["cementing_services"]            = roundup(Cost_Center(basic_input, assumptions, head).cementing(unit_cost = cement_services_costs).ix[:, 1:].sum().sum(), 1000)
        output["directional_drilling_services"] = roundup(Cost_Center(basic_input, assumptions, head).directional_drilling(transhipment, unit_cost = directional_drilling_costs, qty = directional_drilling_qty).sum().sum(), 1000)
        output["mud_engineering_services"]      = roundup(Cost_Center(basic_input, assumptions, head).mud_engineering(qty = mud_engineering_qty, unit_cost =  mud_engineering_costs).ix[:, 1:].sum().sum(), 1000)
        output["aerated_drilling_services"]     = roundup(Cost_Center(basic_input, assumptions, head).aerated_drilling(ada_cost, drlg_input, flat_input, unit_cost = aerated_drilling_costs).ix[:, 1:].sum().sum(), 1000)
        output["jars_and_shock_tools"]          = roundup(Cost_Center(basic_input, assumptions, head).jars_shock(transhipment, drlg_input, qty = jars_shock_qty, unit_cost = jars_shock_costs).ix[:, 1:].sum().sum(), 1000)

    
    idx = basic_input["project_loc"] == transhipment.ix[:, "LOCATION"]
    # a_chf = chf.columns[2:] == basic_input["project_loc"] 
    # b_chf = chf.columns[2:] == basic_input["project_loc"] + ".1"
    # col_chf1 = a_chf + b_chf
    # col_chf2 = np.array(chf.ix["CHF", 2:] == basic_input["chf"])

    # if basic_input["rh_or_bh"] == "Regular Hole":
    #     cost1_chf = np.array(chf.ix['13-5/8" CHF X 13-3/8" Casing', 2:])[col_chf1 * col_chf2][0]
    # else:
    #     cost1_chf = np.array(chf.ix['20-3/4" CHF X 18-5/8" Casing', 2:])[col_chf1 * col_chf2][0]

    # cost2_chf = np.array(chf.ix["Mob/Demob of Equipment", 2:])[col_chf1 * col_chf2][0]
    # cost3_chf = np.array(chf.ix["Mob/Demob of Personnel", 2:])[col_chf1 * col_chf2][0]
    # cost4_chf = np.array(chf.ix["Service Vehicle (Day Rate)", 2:])[col_chf1 * col_chf2][0]
    # cost5_chf = np.array(chf.ix["Standby Equipment", 2:])[col_chf1 * col_chf2][0]
    # cost6_chf = np.array(chf.ix["Standby Personnel", 2:])[col_chf1 * col_chf2][0]
    # cost7_chf = np.array(chf.ix["Standby Boom Truck", 2:])[col_chf1 * col_chf2][0]
    # cost8_chf = np.array(chf.ix["Standby Personnel and Equipment", 2:])[col_chf1 * col_chf2][0]

    # chf_cost = [cost1_chf, cost2_chf, cost3_chf, cost4_chf, cost5_chf, cost6_chf, cost7_chf, cost8_chf,  50000.00]

    if details is True:
        output["chf_welding_services"]          = Cost_Center(basic_input, assumptions, head).chf_installation(unit_cost = chf_costs).ix[:, 1:]#.to_json(orient = "records")
        output["chf_welding_services_qty"]      = Cost_Center(basic_input, assumptions, head).chf_installation().ix[:, 1:]#.to_json(orient = "records")
        output["mud_logging_services"]          = Cost_Center(basic_input, assumptions, head).mud_logging(drlg_input, flat_input, unit_cost = mud_logging_costs).ix[:, 1:]#.to_json(orient = "records")
        output["mud_logging_services_qty"]      = Cost_Center(basic_input, assumptions, head).mud_logging(drlg_input, flat_input).ix[:, 1:]#.to_json(orient = "records")
        output["casing_running_services"]       = Cost_Center(basic_input, assumptions, head).casing_running(unit_cost =  casing_running_cost)#.to_json(orient = "records")
        output["casing_running_services_qty"]   = Cost_Center(basic_input, assumptions, head).casing_running()#.to_json(orient = "records")
    else:
        output["chf_welding_services"]          = roundup(Cost_Center(basic_input, assumptions, head).chf_installation(unit_cost = chf_costs).ix[:, 1:].sum().sum(), 1000)
        output["mud_logging_services"]          = roundup(Cost_Center(basic_input, assumptions, head).mud_logging(drlg_input, flat_input, unit_cost = mud_logging_costs).ix[:, 1:].sum().sum(), 1000)
        output["casing_running_services"]       = roundup(Cost_Center(basic_input, assumptions, head).casing_running(unit_cost =  casing_running_cost).sum().sum(), 1000)
    
    #start - drilling rig services cost
    # idx_cd = basic_input["rig"] == tpwsi_rr_rigs.ix[:, "Rig"]
    # col_cd = basic_input["project_loc"] == tpwsi_rr_rigs.columns
    # cost1 = np.array(tpwsi_rr_rigs.ix[idx_cd, col_cd]).flatten()[0]

    # idx_ma_m = "Meals" == meals_accommodations.ix[:, "Type"]
    # idx_ma_a = "Accommodation" == meals_accommodations.ix[:, "Type"]
    # col_ma = basic_input["project_loc"] == meals_accommodations.columns

    # if np.sum(idx_ma_m) > 0 and np.sum(idx_ma_a) > 0 and np.sum(col_ma):
    #     meal_daily_rate = meals_accommodations.ix[idx_ma_m, col_ma]
    #     accm_daily_rate = meals_accommodations.ix[idx_ma_a, col_ma]
    # else:
    #     meal_daily_rate = 0
    #     accm_daily_rate = 0
    
    # rig1pe_summary = pd.DataFrame(index = ["3RD PARTY", "CHF", "CEMENT CUTTERS", "OTHERS (BOOMTRUCK DRIVER & SV DRIVER)"], columns = ["DURATION", "MEALS", "ACCOM", "TOTAL COST"])
    # rig1pe_summary.ix[0, "DURATION"] = basic_input["total_days"]
    # rig1pe_summary.ix[1, "DURATION"] = 10.
    # if basic_input["double_liner"]:
    #     rig1pe_summary.ix[2, "DURATION"] = 5 * 4
    # else:
    #     rig1pe_summary.ix[2, "DURATION"] = 4 * 4

    # rig1pe_summary.ix[3, "DURATION"] = basic_input["total_days"]

    # rig1pe_summary.ix[0, "MEALS"] = rig1_peripherals.ix[0:5, "MEAL"].sum()
    # rig1pe_summary.ix[1, "MEALS"] = rig1_peripherals.ix[6:7, "MEAL"].sum()
    # rig1pe_summary.ix[2, "MEALS"] = rig1_peripherals.ix[8, "MEAL"]
    # rig1pe_summary.ix[3, "MEALS"] = rig1_peripherals.ix[10, "MEAL"]

    # rig1pe_summary.ix[0, "ACCOM"] = rig1_peripherals.ix[0:5, "ACCOMMODATION"].sum()
    # rig1pe_summary.ix[1, "ACCOM"] = rig1_peripherals.ix[6:7, "ACCOMMODATION"].sum()
    # rig1pe_summary.ix[2, "ACCOM"] = rig1_peripherals.ix[8, "ACCOMMODATION"]
    # rig1pe_summary.ix[3, "ACCOM"] = rig1_peripherals.ix[10, "ACCOMMODATION"]

    # for i in np.arange(4):
    #     rig1pe_summary.ix[i, "TOTAL COST"] = rig1pe_summary.ix[i, "DURATION"] * (rig1pe_summary.ix[i, "MEALS"] * np.array(meal_daily_rate).flatten()[0] + rig1pe_summary.ix[i, "ACCOM"] * np.array(accm_daily_rate).flatten()[0])

    # if basic_input["rig"] == "Rig 1" or basic_input["rig"] == "Rig 2":
    #     cost2 = assumptions[5]["Base Day Rate"]
    #     cost3 = cost4 = average_rop_day_rate.ix[45 - 30, "0 LTI"]
    #     cost5 = assumptions[5]["Additional Payment"] / 365.
    #     cost6 = assumptions[5]["Well Bonus"]
    #     # target_rop depends on the drilling days
    #     cost7 = average_rop_day_rate.ix[basic_input["target_rop"] - 30, 1]
    #     cost9 = rig1pe_summary.ix[:, "TOTAL COST"].sum() / basic_input["total_days"]
    #     cost10 =  3403000.00 
    # else:
    #     cost2 = cost3 = cost4 = cost5 = cost6 = cost7 = cost9 = cost10 = 0
    # cost8 = 0

    # #end - drilling rig services cost
    # drilling_rig_cost = [cost1, cost2, cost3, cost4, cost5, cost6, cost7, cost8, cost9, cost10]

    # dp_qty = np.zeros(4)
    # if basic_input["rent_drill_pipes"]:
    #     dp_qty[0:2] = basic_input["no_of_Joints"]
    #     dp_qty[2:] = 50

    if details is True:
        output["drilling_rig_services"]         = Cost_Center(basic_input, assumptions, head).drilling_rig_services(drlg_input, flat_input, unit_cost = drilling_rig_costs).ix[:, 1:]#.to_json(orient = "records")
        output["drill_pipes"]                   = Cost_Center(basic_input, assumptions, head).drill_pipes(drlg_input, flat_input, qty = drill_pipes_qty, unit_cost = drill_pipes_costs).ix[:, 1:]#.to_json(orient = "records")
        output["drill_pipes_qty"]               = Cost_Center(basic_input, assumptions, head).drill_pipes(drlg_input, flat_input, qty = drill_pipes_qty).ix[:, 1:]#.to_json(orient = "records")
        output["completion_test_wireline"]      = Cost_Center(basic_input, assumptions, head).completion_test(unit_cost = completion_test_costs).ix[:, 1:]#.to_json(orient = "records")
        output["completion_test_wireline_qty"]  = Cost_Center(basic_input, assumptions, head).completion_test().ix[:, 1:]#.to_json(orient = "records")
    else:
        output["drilling_rig_services"]         = roundup(Cost_Center(basic_input, assumptions, head).drilling_rig_services(drlg_input, flat_input, unit_cost = drilling_rig_costs).ix[:, 2:].sum().sum(), 1000)
        output["drill_pipes"]                   = roundup(Cost_Center(basic_input, assumptions, head).drill_pipes(drlg_input, flat_input, qty = drill_pipes_qty, unit_cost = drill_pipes_costs).ix[:, 1:].sum().sum(), 1000)
        output["completion_test_wireline"]      = roundup(Cost_Center(basic_input, assumptions, head).completion_test(unit_cost = completion_test_costs ).ix[:, 1:].sum().sum(), 1000)

    cement_out                              = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2)

    # if basic_input["project_loc"] == "LGBU":
    #     other_cementing_cost = 13
    # elif basic_input["project_loc"] == "BGBU":
    #     other_cementing_cost = 16
    # elif basic_input["project_loc"] == "NIGBU":
    #     other_cementing_cost = 15
    # elif basic_input["project_loc"] == "MAGBU":
    #     other_cementing_cost = 10

    trans_table                             = Cost_Center(basic_input, assumptions, head).transhipment_cost(handling_hauling, transhipment_drillpipes)
    if details is True:
        output["other_cementing_services"]      = Cost_Center(basic_input, assumptions, head).other_cementing_services(cement_out, unit_cost = other_cementing_cost).ix[:1, 1:]#.to_json(orient = "records")
        output["other_cementing_services_qty"]  = Cost_Center(basic_input, assumptions, head).other_cementing_services(cement_out).ix[:1, 1:]#.to_json(orient = "records")
        output["handling_hauling_towing"]       = Cost_Center(basic_input, assumptions, head).handling(drlg_input, flat_input, asmpt1 = trans_table.ix[:, "TOTAL"].sum())#.to_json(orient = "records")
    else:
        output["other_cementing_services"]      = roundup(Cost_Center(basic_input, assumptions, head).other_cementing_services(cement_out, unit_cost = other_cementing_cost).ix[:1, 1:].sum().sum(), 1000)
        output["handling_hauling_towing"]       = roundup(Cost_Center(basic_input, assumptions, head).handling(drlg_input, flat_input, asmpt1 = trans_table.ix[:, "TOTAL"].sum()).sum().sum(), 1000)
    
    drilling_rig_table                      = Cost_Center(basic_input, assumptions, head).drilling_rig_services(drlg_input, flat_input, unit_cost = drilling_rig_costs).ix[:, 1:].sum()
    
    rig_mobilization_index = ["40 FT HI-BED TRAILER", "40 FT SEMI-LOW BED TRAILER (35T)", "35 FT LOW BED TRAILER (60T)", "50T CRANE", "70T CRANE", "180T CRANE", "PAYLOADER", "FORKLOADER", "TOWING EQUIPMENT", "BOOM TRUCK", "5TUT PUMP", "INTERISLAND RIGMOVE (ALLOCATED)"]
    idx1_rm = basic_input["project_loc"] == handling_hauling.index
    idx2_rm = rig_mobilization_index[1] == rigmove.ix[:, "ITEM"]
    idx3_rm = rig_mobilization_index[2] == rigmove.ix[:, "ITEM"]
    idx4_rm = rig_mobilization_index[3] == equipment.ix[:, "Equipment Rental"]
    idx5_rm = rig_mobilization_index[4] == equipment.ix[:, "Equipment Rental"]
    idx6_rm = rig_mobilization_index[5] == equipment.ix[:, "Equipment Rental"]
    idx7_rm = rig_mobilization_index[6] == rigmove.ix[:, "ITEM"]
    idx8_rm = rig_mobilization_index[7] == rigmove.ix[:, "ITEM"]
    idx9_rm = rig_mobilization_index[8] == rigmove.ix[:, "ITEM"]
    idx10_rm = rig_mobilization_index[9] == rigmove.ix[:, "ITEM"]
    idx11_rm = rig_mobilization_index[10] == equipment.ix[:, "Equipment Rental"]

    cost1_rm = np.array(handling_hauling.ix[idx1_rm, "40ft HBT"]).flatten()[0]
    cost2_rm = np.array(rigmove.ix[idx2_rm, "UNIT COST"]).flatten()[0]
    cost3_rm = np.array(rigmove.ix[idx3_rm, "UNIT COST"]).flatten()[0]
    cost4_rm = np.array(equipment.ix[idx4_rm, "UNIT RATES"]).flatten()[0]
    cost5_rm = np.array(equipment.ix[idx5_rm, "UNIT RATES"]).flatten()[0]
    cost6_rm = np.array(equipment.ix[idx6_rm, "UNIT RATES"]).flatten()[0]
    cost7_rm = np.array(rigmove.ix[idx7_rm, "UNIT COST"]).flatten()[0]
    cost8_rm = np.array(rigmove.ix[idx8_rm, "UNIT COST"]).flatten()[0]
    cost9_rm = np.array(rigmove.ix[idx9_rm, "UNIT COST"]).flatten()[0]
    cost10_rm = np.array(rigmove.ix[idx10_rm, "UNIT COST"]).flatten()[0]
    cost11_rm = np.array(equipment.ix[idx11_rm, "UNIT RATES"]).flatten()[0]

    rm_cost = [cost1_rm, cost2_rm, cost3_rm, cost4_rm, cost5_rm, cost6_rm, cost7_rm, cost8_rm, cost9_rm, cost10_rm, cost11_rm, 0]
    # output["rig_mobilization_charges"]      = np.array(Cost_Center(basic_input, assumptions).rig_mobilization(asmpt1 = rig_move1_asmpt, asmpt2 = rig_move2_asmpt, asmpt3 = rigmove_cost, asmpt4 = drilling_rig_table.rigmove, unit_cost = rm_cost, total = True))[0]
    if details is True:
        output["rig_mobilization_charges"]      = Cost_Center(basic_input, assumptions, head).rig_mobilization(asmpt1 = rig_move1_asmpt, asmpt2 = rig_move2_asmpt, asmpt3 = rigmove_cost, asmpt4 = drilling_rig_table.rigmove, unit_cost = rm_cost)#.to_json(orient = "records")
    else:
        output["rig_mobilization_charges"]      = roundup(Cost_Center(basic_input, assumptions, head).rig_mobilization(asmpt1 = rig_move1_asmpt, asmpt2 = rig_move2_asmpt, asmpt3 = rigmove_cost, asmpt4 = drilling_rig_table.rigmove, unit_cost = rm_cost, total = True), 1000)
        
    # print type(Cost_Center(basic_input, assumptions).rig_mobilization(asmpt1 = rig_move1_asmpt, asmpt2 = rig_move2_asmpt, asmpt3 = rigmove_cost, asmpt4 = drilling_rig_table.rigmove, unit_cost = rm_cost, total = True))
    if basic_input["project_loc"] == "LGBU":
        er_qty = [1, 1, 0, 0, 2, 2, 1]
    elif basic_input["project_loc"] == "BGBU":
        er_qty = [0, 0, 0, 0, 0, 1, 1]
    elif basic_input["project_loc"] == "NIGBU":
        er_qty = [1, 1, 0, 0, 2, 2, 1]
    elif basic_input["project_loc"] == "MAGBU":
        er_qty = [1, 1, 0, 0, 2, 2, 1]

    equipment_rental                        = Cost_Center(basic_input, assumptions, head).equipment_rental(rig_move2_asmpt, equipment, drlg_input, flat_input, unit_cost = equipmental_costs, qty = equipmental_qty).ix[:, 1:].sum().sum()
    #output["rig_allocated_charges"]         = Cost_Center(basic_input, assumptions).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island).ix[:, 1:].sum().sum()

    if details is True:    
        output["equipment_rental"]              = Cost_Center(basic_input, assumptions, head).equipment_rental(rig_move2_asmpt, equipment, drlg_input, flat_input, unit_cost =  equipmental_costs, qty = equipmental_qty).ix[:, 1:]#.to_json(orient = "records")
        output["equipment_rental_qty"]          = Cost_Center(basic_input, assumptions, head).equipment_rental(rig_move2_asmpt, equipment, drlg_input, flat_input, qty = equipmental_qty).ix[:, 1:]#.to_json(orient = "records")
        output["rig_allocated_charges"]         = Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:]#.to_json(orient = "records")
    else:
        output["rig_oml_daily_rate"]            = roundup(Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:].sum(1).ix[0, :], 1000)
        output["depreciation"]                  = roundup(Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:].sum(1).ix[1, :], 1000)
        output["insurance"]                     = roundup(Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:].sum(1).ix[2, :], 1000)
        output["genex_daily_rate"]              = roundup(Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:].sum(1).ix[3, :], 1000)
        output["thermaprime"]                   = roundup(Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:].sum(1).ix[4, :], 1000)
        output["DG"]                            = roundup(Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:].sum(1).ix[5, :], 1000)
        output["interisland_cost"]              = roundup(Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:].sum(1).ix[6, :], 1000)

        output["total"]                         = np.sum(output.values())
        output["materials_total"]               = np.sum([output[key] for key in ["fuels", "lubricants", "mud_and_chemicals", "cements_and_additives", "rockbits", "drilling_supplies", "casings", "wellhead"]])
        output["services_total"]                = np.sum([output[key] for key in ["cementing_services", "directional_drilling_services", "mud_engineering_services", "aerated_drilling_services", "jars_and_shock_tools", "chf_welding_services", "mud_logging_services", "casing_running_services", "drilling_rig_services", "drill_pipes", "completion_test_wireline", "other_cementing_services", "handling_hauling_towing", "rig_mobilization_charges"]])
        output["rig_allocated_total"]           = np.sum([output[key] for key in ["rig_oml_daily_rate", "depreciation", "insurance", "genex_daily_rate", "thermaprime", "DG", "interisland_cost"]])

    print("Output of Handling Hauling Towing")
    print(output["handling_hauling_towing"])
    # print(data["rockbits_input"])
    # print(rockbits_df)
    # print(rockbits_df.set_index("Rockbits"))
    # rockbits_df.to_csv("rockbits.csv")

    if data["export_cover_cost_tables"] == "Cover Sheet" and details is False:
        cover_sheet_index = [
            "fuels", "lubricants", "mud_and_chemicals", "cements_and_additives", "rockbits", "drilling_supplies", "casings", "wellhead",
            "cementing_services", "directional_drilling_services", "mud_engineering_services", "aerated_drilling_services", "jars_and_shock_tools", "chf_welding_services", "mud_logging_services", "casing_running_services", "drilling_rig_services", "drill_pipes", "completion_test_wireline", "other_cementing_services", "handling_hauling_towing", "rig_mobilization_charges",
            "rig_oml_daily_rate", "depreciation", "insurance", "genex_daily_rate", "thermaprime", "DG", "interisland_cost"
        ]

        cover_sheet_values = [output[key] for key in cover_sheet_index]

        cover_sheet_table = [("Items", cover_sheet_index), ("Cost", cover_sheet_values)]
        pd.DataFrame.from_items(cover_sheet_table).to_csv(data["export_cover_cost_file_path"] + ".csv")
        return output
    elif data["export_cover_cost_tables"] == "Cost Details" and details is True:
        cost_details_index = [
            "fuels", "lubricants", "mud_and_chemicals", "cements_and_additives", "smith", "hughes", "drilling_supplies", "casings", "wellhead",
            "cementing_services", "directional_drilling_services", "mud_engineering", "aerated_drilling", 
            "jars_and_shock_tools", "chf_welding_services", "mud_logging_services", "casing_running_services", "drilling_rig_services", "drill_pipes", "completion_test_wireline", "other_cementing_services", "handling_hauling_towing", "equipment_rental", "rig_allocated_charges"
        ]

        qnty_details_index = [
            "fuels_qty", "mud_and_chemicals_qty", "cements_and_additives_qty", "drilling_supplies_qty", "casings_qty", "wellhead_qty",
            "cementing_services_qty", "directional_drilling_services_qty", "mud_engineering_qty", "aerated_drilling_qty", 
            "jars_and_shock_tools_qty", "chf_welding_services_qty", "mud_logging_services_qty", "casing_running_services_qty", "drill_pipes_qty", "completion_test_wireline_qty", "other_cementing_services_qty", "equipment_rental_qty"
        ]

        cost_details_tables = [output[key] for key in cost_details_index]
        qnty_details_tables = [output[key] for key in qnty_details_index]
        
        df_cost = pd.concat(cost_details_tables)
        df_qnty = pd.concat(qnty_details_tables)

        cols_order = ["rigmove", "d_surface", "f_surface", "d_intermediate", "f_intermediate", "d_prodn_casing", "f_prodn_casing", "d_prodn_liner_1", "f_prodn_liner_1", "d_prodn_liner_2", "f_prodn_liner_2"]
        
        df_cost = df_cost[cols_order]
        df_qnty = df_qnty[cols_order]

        df_cost.to_csv(data["export_cover_cost_file_path"] + "-cost.csv")
        df_qnty.to_csv(data["export_cover_cost_file_path"] + "-qnty.csv")
        
        # pd.concat(cost_details_tables).to_csv(data["export_cover_cost_file_path"] + "_cost.csv")
        # pd.concat(qnty_details_tables).to_csv(data["export_cover_cost_file_path"] + "_qnty.csv")

        all_index = cost_details_index + qnty_details_index
        
        output_json = {}
        for key in all_index:
            output_json[key] = output[key].to_json(orient = "records")
        
        return output_json
    elif data["export_cover_cost_tables"] == "IDS Table" and details is True:
        cost_details_index = [
            "fuels", "lubricants", "mud_and_chemicals", "cements_and_additives", "smith", "hughes", "drilling_supplies", "casings", "wellhead",
            "cementing_services", "directional_drilling_services", "mud_engineering", "aerated_drilling", 
            "jars_and_shock_tools", "chf_welding_services", "mud_logging_services", "casing_running_services", "drilling_rig_services", "drill_pipes", "completion_test_wireline", "other_cementing_services", "handling_hauling_towing", "equipment_rental", "rig_allocated_charges"
        ]

        qnty_details_index = [
            "fuels_qty", "mud_and_chemicals_qty", "cements_and_additives_qty", "drilling_supplies_qty", "casings_qty", "wellhead_qty",
            "cementing_services_qty", "directional_drilling_services_qty", "mud_engineering_qty", "aerated_drilling_qty", 
            "jars_and_shock_tools_qty", "chf_welding_services_qty", "mud_logging_services_qty", "casing_running_services_qty", "drill_pipes_qty", "completion_test_wireline_qty", "other_cementing_services_qty", "equipment_rental_qty"
        ]

        cost_details_tables = [output[key] for key in cost_details_index]
        qnty_details_tables = [output[key] for key in qnty_details_index]

        df_ids_cost = pd.concat(cost_details_tables).ix[:, 1:].sum(axis = 1)
        df_ids_qnty = pd.concat(qnty_details_tables).ix[:, 1:].sum(axis = 1)

        df_ids_cost.columns = ["Index", "Total Cost"]
        df_ids_qnty.columns = ["Index", "Total Quantities"]

        df_ids_cost.to_csv(data["export_cover_cost_file_path"] + "-ids-cost.csv")
        df_ids_qnty.to_csv(data["export_cover_cost_file_path"] + "-ids-qnty.csv")

        # pd.concat(cost_details_tables).ix[:, 1:].sum(axis = 1).to_csv(data["export_cover_cost_file_path"] + "-ids-cost.csv")
        # pd.concat(qnty_details_tables).ix[:, 1:].sum(axis = 1).to_csv(data["export_cover_cost_file_path"] + "-ids-qnty.csv")

        all_index = cost_details_index + qnty_details_index
        
        output_json = {}
        for key in all_index:
            output_json[key] = output[key].to_json(orient = "records")
        
        return output_json
    elif data["export_cover_cost_tables"] == "None" and details is False:
        return output
    elif data["export_cover_cost_tables"] == "None" and details is True:
        cost_details_index = [
            "fuels", "lubricants", "mud_and_chemicals", "cements_and_additives", "smith", "hughes", "drilling_supplies", "casings", "wellhead",
            "cementing_services", "directional_drilling_services", "mud_engineering", "aerated_drilling", 
            "jars_and_shock_tools", "chf_welding_services", "mud_logging_services", "casing_running_services", "drilling_rig_services", "drill_pipes", "completion_test_wireline", "other_cementing_services", "handling_hauling_towing", "equipment_rental", "rig_allocated_charges"
        ]

        qnty_details_index = [
            "fuels_qty", "mud_and_chemicals_qty", "cements_and_additives_qty", "drilling_supplies_qty", "casings_qty", "wellhead_qty",
            "cementing_services_qty", "directional_drilling_services_qty", "mud_engineering_qty", "aerated_drilling_qty", 
            "jars_and_shock_tools_qty", "chf_welding_services_qty", "mud_logging_services_qty", "casing_running_services_qty", "drill_pipes_qty", "completion_test_wireline_qty", "other_cementing_services_qty", "equipment_rental_qty"
        ]

        all_index = cost_details_index + qnty_details_index
        
        output_json = {}
        for key in all_index:
            output_json[key] = output[key].to_json(orient = "records")

        return output_json
    else:
        return output

def compute_hole_casing(data):
    """
    Computes the Hole and Casing Summary

    # Arguments:
        data: dict, json input from the client
        output: dict, the output of the server
    """

    compute_inputs(data)
    output = {}
    output["hole-size"] = Hole_Casing(basic_input, data, category = 'size').compute(assumptions)[0]
    output["case-size"] = nan_checker(Hole_Casing(basic_input, data, category = 'size').compute(assumptions)[1])
    output["hole-depth"] = nan_checker(Hole_Casing(basic_input, data, category = 'hole_depth').compute(assumptions))
    output["case-id"] = nan_checker(Hole_Casing(basic_input, data, category = 'case_id').compute(assumptions))
    output["hole-length"] = Hole_Casing(basic_input, data, category = 'hole_length').compute(assumptions)

    print(output["hole-size"])
    print(output["case-size"])
    return output

def nan_checker(d):
    """
    Checks if numpy.nan is present in dict and converts it to None

    Flask jsonify() function cannot handle numpy.nan
    """
    
    if type(d) is dict:
        for k in d.keys():
            if np.isnan(d[k]):
                d[k] = None
    elif type(d) is list:
        for k in np.arange(len(d)):
            if np.isnan(d[k]):
                d[k] = None

    return d

def compute_afe_costs(data, output, type_ = "rop"):
    """
    Computes the AFE Costs

    # Arguments:
        data: dict, json input from the client
        output: dict, the output of the server
        type_: string, the type of the computation (options: "rop" or "cd")
    """
    # compute_inputs(data)
    
    # casing_depth_input = {
    #     "surface"       : 0 if data["analysis_" + type_ + "_sh_cd"] == "" else float(data["analysis_" + type_ + "_sh_cd"]),
    #     "intermediate"  : 0 if data["analysis_" + type_ + "_ih_cd"] == "" else float(data["analysis_" + type_ + "_ih_cd"]),
    #     "prodn_casing"  : 0 if data["analysis_" + type_ + "_dh_cd"] == "" else float(data["analysis_" + type_ + "_dh_cd"]),
    #     "prodn_liner_1" : 0 if data["analysis_" + type_ + "_ph1_cd"] == "" else float(data["analysis_" + type_ + "_ph1_cd"]),
    #     "prodn_liner_2" : 0 if data["analysis_" + type_ + "_ph2_cd"] == "" else float(data["analysis_" + type_ + "_ph2_cd"]),
    # }

    # assumptions[2] = casing_depth_input    

    surf_range = surface_day_range(data, type_ = type_)
    intr_range = intermediate_day_range(data, type_ = type_)
    prod_range = prodn_casing_day_range(data, type_ = type_)
    prl1_range = prodn_liner_1_day_range(data, type_ = type_)
    prl2_range = prodn_liner_2_day_range(data, type_ = type_)

    range_list = [surf_range, intr_range, prod_range, prl1_range, prl2_range]
    
    if data["run_option"] == "All":
        compute_afe_cost_helper(range_list, output, data, phase = "surface")
        compute_afe_cost_helper(range_list, output, data, phase = "intermediate")
        compute_afe_cost_helper(range_list, output, data, phase = "prodn-casing")
        compute_afe_cost_helper(range_list, output, data, phase = "prodn-liner-1")
        compute_afe_cost_helper(range_list, output, data, phase = "prodn-liner-2")
    else:
        compute_afe_cost_helper(range_list, output, data, phase = "given")

    print output
    return output
    
def compute_afe_cost_helper(inp, out, data, phase = "surface"):
    
    out[phase] = {}
    out[phase]["afe"] = []
    out[phase]["drlg-days"] = {}
    out[phase]["total-rop"] = []
    print(data)
    for i in np.arange(0, 4):
        if data["run_option"] == "All":    
            d_days = {
                "surface" : inp[0][i] if phase == "surface" else inp[0][0],
                "intermediate" : inp[1][i] if phase == "intermediate" else inp[1][0],
                "prodn_casing" : inp[2][i] if phase == "prodn-casing" else inp[2][0],
                "prodn_liner_1" : inp[3][i] if phase == "prodn-liner-1" else inp[3][0],
                "prodn_liner_2" : inp[4][i] if phase == "prodn-liner-2" else inp[4][0]
            }
        else:
            d_days = {
                "surface" : inp[0][i],
                "intermediate" : inp[1][i],
                "prodn_casing" : inp[2][i],
                "prodn_liner_1" : inp[3][i],
                "prodn_liner_2" : inp[4][i]
            }

        out[phase]["afe"] += [compute_cover_sheet(data, {}, False, d_days)["total"]]
        out[phase]["drlg-days"]["Scenario " + str(i)] = d_days
        out[phase]["total-rop"] += [Drilling_Days(d_days, flat_input).target_rop(basic_input)]

    if data["run_option"] == "All":
        afe_sorted = np.sort(out[phase]["afe"]).tolist()
        idx_sorted = np.argsort(out[phase]["afe"]).tolist()
        rop_sorted = [out[phase]["total-rop"][i] for i in idx_sorted]

        out[phase]["afe"] = afe_sorted
        out[phase]["total-rop"] = rop_sorted
        # print "This is the output of total ROP."
        # print out[phase]["total-rop"]
        # print "This ithe sorted index"
        # print idx_sorted

        j = 0; drlg_days_sorted = {}
        for i in idx_sorted:
            drlg_days_sorted["Scenario " + str(j)] = out[phase]["drlg-days"]["Scenario " + str(i)]
            j += 1

        for i in np.arange(0, 4):
            out[phase]["drlg-days"]["Scenario " + str(i)] = drlg_days_sorted["Scenario " + str(i)]

        return out
    else:
        return out

def surface_day_range(data, type_ = "rop"):    
    return [float(data["analysis_" + type_ + "_sh_day_" + i]) for i in ["b", "1", "2", "3"]]
    
def intermediate_day_range(data, type_ = "rop"):
    return [float(data["analysis_" + type_ + "_ih_day_" + i]) for i in ["b", "1", "2", "3"]]

def prodn_casing_day_range(data, type_ = "rop"):
    return [float(data["analysis_" + type_ + "_dh_day_" + i]) for i in ["b", "1", "2", "3"]]

def prodn_liner_1_day_range(data, type_ = "rop"):
    return [float(data["analysis_" + type_ + "_ph1_day_" + i]) for i in ["b", "1", "2", "3"]]

def prodn_liner_2_day_range(data, type_ = "rop"):
    return [float(data["analysis_" + type_ + "_ph2_day_" + i]) for i in ["b", "1", "2", "3"]]

def compute_analysis_depth_baseline(data, type_ = "depth"):
    """
    # Arguments
        data: json, received from client
        type_: string, type of the computation
    """
    print "request for depth baseline computation received"
    for inc in np.arange(1, 4):
        depth_keys = ["analysis_" + phase + "_cd_" + str(inc) for phase in ["sh", "ih", "dh", "ph1", "ph2"]];
        output = compute_analysis_rop_baseline(data, depth_keys = depth_keys)
        print "This is the output"
        print output
    #
    # inputs(data)
    #
    # basic_input["total_days"]         = basic_input["rig_move_days"] + Drilling_Days(drlg_input, flat_input).total()
    # basic_input["drilling_days"]      = Drilling_Days(drlg_input, flat_input).cell(basic_input)
    # basic_input["target_rop"]         = Drilling_Days(drlg_input, flat_input).target_rop(basic_input)
    # basic_input["drilling_row_total"] = Drilling_Days(drlg_input, flat_input).row_total()
    #
    # casing_depth_input = {
    #     "surface"      : 0 if data["analysis_sh_cd"] == "" else float(data["analysis_sh_cd"]),
    #     "intermediate" : 0 if data["analysis_ih_cd"] == "" else float(data["analysis_ih_cd"]),
    #     "prodn_casing" : 0 if data["analysis_dh_cd"] == "" else float(data["analysis_dh_cd"]),
    #     "prodn_liner_1": 0 if data["analysis_ph1_cd"] == "" else float(data["analysis_ph1_cd"]),
    #     "prodn_liner_2": 0 if data["analysis_ph2_cd"] == "" else float(data["analysis_ph2_cd"])
    # }
    #
    # assumptions[2] = casing_depth_input
    #
    # if type_ == "depth":


def compute_analysis_rop_baseline(data, depth_keys = None, type_ = "rop"):
    """
    # Arguments
        data: json, received from client
        type_: string, type of the computation
    """
    inputs(data)
    
    basic_input["total_days"]         = basic_input["rig_move_days"] + Drilling_Days(drlg_input, flat_input).total()
    basic_input["drilling_days"]      = Drilling_Days(drlg_input, flat_input).cell(basic_input)
    basic_input["target_rop"]         = Drilling_Days(drlg_input, flat_input).target_rop(basic_input)
    basic_input["drilling_row_total"] = Drilling_Days(drlg_input, flat_input).row_total()

    if depth_keys is None:
        depth_keys = ["analysis_rop_sh_cd", "analysis_rop_ih_cd", "analysis_rop_dh_cd", "analysis_rop_ph1_cd", "analysis_rop_ph2_cd"]
    
    casing_depth_input = {
        "surface"       : 0 if data[depth_keys[0]] == "" else float(data[depth_keys[0]]),
        "intermediate"  : 0 if data[depth_keys[1]] == "" else float(data[depth_keys[1]]),
        "prodn_casing"  : 0 if data[depth_keys[2]] == "" else float(data[depth_keys[2]]),
        "prodn_liner_1" : 0 if data[depth_keys[3]] == "" else float(data[depth_keys[3]]),
        "prodn_liner_2" : 0 if data[depth_keys[4]] == "" else float(data[depth_keys[4]])
    }

    assumptions[2] = casing_depth_input

    # Compute the Baseline ROP per Section
    if type_ is "rop":
        analysis = Analysis(basic_input, assumptions, drlg_input)
        return analysis.rop_sec
    elif type_ is "days":
        output = {}
        for i in ["b", "1", "2", "3"]:
            inc_rop = {
                "surface"       : 0 if data["analysis_rop_sh_inc_" + i]  == "" else float(data["analysis_rop_sh_inc_" + i]),
                "intermediate"  : 0 if data["analysis_rop_ih_inc_" + i]  == "" else float(data["analysis_rop_ih_inc_" + i]),
                "prodn_casing"  : 0 if data["analysis_rop_dh_inc_" + i]  == "" else float(data["analysis_rop_dh_inc_" + i]),
                "prodn_liner_1" : 0 if data["analysis_rop_ph1_inc_" + i] == "" else float(data["analysis_rop_ph1_inc_" + i]),
                "prodn_liner_2" : 0 if data["analysis_rop_ph2_inc_" + i] == "" else float(data["analysis_rop_ph2_inc_" + i])
            }

            output["rop-" + i] = Analysis(basic_input, assumptions, rop_sec = inc_rop).drlg_days()
        
        return output
    else:
        raise ValueError("Entered " + type_ + ", please choose only: 'rop' or 'days'.")

def compute_target_rop_etc(data, output):
    inputs(data)

    output["total_days"]         = basic_input["rig_move_days"] + Drilling_Days(drlg_input, flat_input).total()
    output["drilling_days"]      = Drilling_Days(drlg_input, flat_input).cell(basic_input)
    output["target_rop"]         = Drilling_Days(drlg_input, flat_input).target_rop(basic_input)
    output["drilling_row_total"] = Drilling_Days(drlg_input, flat_input).row_total()

    return output

def compute_baseline_costs(data, type_, output):
    """
    Handles Computation of Baseline Costs
    """
    print("Request Received For Computation of Baseline Costs")
    print(type_)
    inputs(data)

    cement_slb_asmpt2       = pd.read_excel(dt_dir + "/equipmental_rentals.xlsx")
    inventory               = pd.read_excel(dt_dir + "/inventory.xlsx")
    
    basic_input["total_days"]         = basic_input["rig_move_days"] + Drilling_Days(drlg_input, flat_input).total()
    basic_input["drilling_days"]      = Drilling_Days(drlg_input, flat_input).cell(basic_input)
    basic_input["target_rop"]         = Drilling_Days(drlg_input, flat_input).target_rop(basic_input)
    basic_input["drilling_row_total"] = Drilling_Days(drlg_input, flat_input).row_total()

    if type_ == "cement_additives":
        cement_slb = Assumptions(basic_input, assumptions)
        cemt = cement_slb.cement_slb(data)

        if basic_input["rh_or_bh"] == "Big Hole":
            idx = list(cemt.index)[:len(list(cemt.index)) - 1] + [cement_slb_asmpt2.ix[5, "Equipment"]]
        else:
            idx = list(cemt.index)[:len(list(cemt.index)) - 1] + [cement_slb_asmpt2.ix[7, "Equipment"]]

        costs = list(cemt.Price)[0:len(list(cemt.Price)) - 1] + list(cement_slb_asmpt2.ix[cement_slb_asmpt2.Equipment == idx[-1], "Unit Price, USD"])
        return costs
    
    elif type_ == "rockbits":
        rckb_unit_scost = np.array(Unit_Rate(basic_input, inventory).rockbits().ix[:, "smith_unit_cost"]).tolist()
        rckb_unit_hcost = np.array(Unit_Rate(basic_input, inventory).rockbits().ix[:, "hughes_unit_cost"]).tolist()
        costs = [nan_checker(rckb_unit_scost), nan_checker(rckb_unit_hcost)]

        return costs
    
    elif type_ == "drilling_supplies":        
        if basic_input["rig"] == "Rig 1" or basic_input["rig"] == "Rig 2":
            costs = np.array([0, 0], dtype = "int").tolist()
        else:
            costs = np.array([2000 * basic_input["forex_ph_us"], 6000 * basic_input["forex_ph_us"]], dtype = "int").tolist()

        return costs
    
    elif type_ == "wellhead":
        if basic_input["project_loc"] == "LGBU":
            wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead.xlsx")
            wlhd_last_row           = 103558.77 
        elif basic_input["project_loc"] == "BGBU":
            wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead_BGBU.xlsx")
            wlhd_last_row           =  103934.64     
        elif basic_input["project_loc"] == "NIGBU":
            wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead_NIGBU.xlsx")
            wlhd_last_row           =  104122.57     
        elif basic_input["project_loc"] == "MAGBU":
            wlhd_asmpt              = pd.read_excel(dt_dir + "/wellhead_MAGBU.xlsx")
            wlhd_last_row           =  103934.64 

        if basic_input["rh_or_bh"] == "Big Hole":
            cost = wlhd_asmpt.ix[:, "Big Hole Unit cost"].values
        else:
            cost = wlhd_asmpt.ix[:, "Regular Hole Unit cost"].values

        costs = np.append(cost, wlhd_last_row).tolist()
        
        return costs
    
    elif type_ == "cementing_services":
        return [961.17*0.975, 27.55*0.975, 21.35*0.975, 76.21*0.975, 280*0.975, 280*0.975, 316.25*0.975, 77*0.975, 316.25*0.975, 552*0.975, 207*0.975, 207*0.975, 862.5*0.975]

    elif type_ == "directional_drilling":
        costs = [552.50, 552.50, 455.00, 3.25, 130.00, 3.25, 97.50, 3.25, 3.25, 2038.40, 162.50, 0, 0, 219.96, 219.96, 219.96, 232.18, 247.00, 200.20, 130.00, 130.00, 130.00, 260.00, 219.96, 219.96, 24957.00, 24957.00, 60, 60, 850.00, 850.00, 9375.00]

        if basic_input["pwd_fliner1"]:
            qty = [2.0, 2.0, 4.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        else:
            qty = [2.0, 2.0, 4.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                  
        return [qty, costs]
    
    elif type_ == "mud_engineering":
        cost = 472.50
        qty = 2
        return [qty, cost]
    
    elif type_ == "aerated_drilling":
        return nan_checker([3203.50, 2214.50, 67000.00, 67000.00, 1097.50, 351.25, 2900.00, np.nan, 879.78, 1173.04, 244.24, 391.30, 236.50, 258.00, np.nan, 1450.00, 1050.00, 950.00, 950.00, 7500.00, 800.00])
        
    elif type_ == "jars_shock":
        return [145.00, 135.00, 135.00, 135.00, 65.00, 3100.00]
    
    elif type_ == "chf_installation":
        chf = pd.read_excel(dt_dir + "/chf.xlsx").set_index("Index")
        a_chf = chf.columns[2:] == basic_input["project_loc"] 
        b_chf = chf.columns[2:] == basic_input["project_loc"] + ".1"
        col_chf1 = a_chf + b_chf
        col_chf2 = np.array(chf.ix["CHF", 2:] == basic_input["chf"])

        if basic_input["rh_or_bh"] == "Regular Hole":
            cost1_chf = np.array(chf.ix['13-5/8" CHF X 13-3/8" Casing', 2:])[col_chf1 * col_chf2][0]
        else:
            cost1_chf = np.array(chf.ix['20-3/4" CHF X 18-5/8" Casing', 2:])[col_chf1 * col_chf2][0]

        cost2_chf = np.array(chf.ix["Mob/Demob of Equipment", 2:])[col_chf1 * col_chf2][0]
        cost3_chf = np.array(chf.ix["Mob/Demob of Personnel", 2:])[col_chf1 * col_chf2][0]
        cost4_chf = np.array(chf.ix["Service Vehicle (Day Rate)", 2:])[col_chf1 * col_chf2][0]
        cost5_chf = np.array(chf.ix["Standby Equipment", 2:])[col_chf1 * col_chf2][0]
        cost6_chf = np.array(chf.ix["Standby Personnel", 2:])[col_chf1 * col_chf2][0]
        cost7_chf = np.array(chf.ix["Standby Boom Truck", 2:])[col_chf1 * col_chf2][0]
        cost8_chf = np.array(chf.ix["Standby Personnel and Equipment", 2:])[col_chf1 * col_chf2][0]
        
        return nan_checker([cost1_chf, cost2_chf, cost3_chf, cost4_chf, cost5_chf, cost6_chf, cost7_chf, cost8_chf,  50000.00])

    elif type_ == "mud_logging":
        return [931.20, 820.80]
    
    elif type_ == "casing_running":
        return [69300 / 31.]
    
    elif type_ == "drilling_rig":
        tpwsi_rr_rigs = pd.read_excel(dt_dir + "/tpwsi_rr_rigs.xlsx")
        meals_accommodations = pd.read_excel(dt_dir + "/meals_accommodations.xlsx")
        rig1_peripherals = pd.read_excel(dt_dir + "/rig1peripherals.xlsx")
        average_rop_day_rate = pd.read_excel(dt_dir + "/average_rop_day_rate.xlsx")

        idx_cd = basic_input["rig"] == tpwsi_rr_rigs.ix[:, "Rig"]
        col_cd = basic_input["project_loc"] == tpwsi_rr_rigs.columns
        cost1 = np.array(tpwsi_rr_rigs.ix[idx_cd, col_cd]).flatten()[0]

        idx_ma_m = "Meals" == meals_accommodations.ix[:, "Type"]
        idx_ma_a = "Accommodation" == meals_accommodations.ix[:, "Type"]
        col_ma = basic_input["project_loc"] == meals_accommodations.columns

        if np.sum(idx_ma_m) > 0 and np.sum(idx_ma_a) > 0 and np.sum(col_ma):
            meal_daily_rate = meals_accommodations.ix[idx_ma_m, col_ma]
            accm_daily_rate = meals_accommodations.ix[idx_ma_a, col_ma]
        else:
            meal_daily_rate = 0
            accm_daily_rate = 0
        
        rig1pe_summary = pd.DataFrame(index = ["3RD PARTY", "CHF", "CEMENT CUTTERS", "OTHERS (BOOMTRUCK DRIVER & SV DRIVER)"], columns = ["DURATION", "MEALS", "ACCOM", "TOTAL COST"])
        rig1pe_summary.ix[0, "DURATION"] = basic_input["total_days"]
        rig1pe_summary.ix[1, "DURATION"] = 10.
        if basic_input["double_liner"]:
            rig1pe_summary.ix[2, "DURATION"] = 5 * 4
        else:
            rig1pe_summary.ix[2, "DURATION"] = 4 * 4

        rig1pe_summary.ix[3, "DURATION"] = basic_input["total_days"]

        rig1pe_summary.ix[0, "MEALS"] = rig1_peripherals.ix[0:5, "MEAL"].sum()
        rig1pe_summary.ix[1, "MEALS"] = rig1_peripherals.ix[6:7, "MEAL"].sum()
        rig1pe_summary.ix[2, "MEALS"] = rig1_peripherals.ix[8, "MEAL"]
        rig1pe_summary.ix[3, "MEALS"] = rig1_peripherals.ix[10, "MEAL"]

        rig1pe_summary.ix[0, "ACCOM"] = rig1_peripherals.ix[0:5, "ACCOMMODATION"].sum()
        rig1pe_summary.ix[1, "ACCOM"] = rig1_peripherals.ix[6:7, "ACCOMMODATION"].sum()
        rig1pe_summary.ix[2, "ACCOM"] = rig1_peripherals.ix[8, "ACCOMMODATION"]
        rig1pe_summary.ix[3, "ACCOM"] = rig1_peripherals.ix[10, "ACCOMMODATION"]

        for i in np.arange(4):
            rig1pe_summary.ix[i, "TOTAL COST"] = rig1pe_summary.ix[i, "DURATION"] * (rig1pe_summary.ix[i, "MEALS"] * np.array(meal_daily_rate).flatten()[0] + rig1pe_summary.ix[i, "ACCOM"] * np.array(accm_daily_rate).flatten()[0])

        if basic_input["rig"] == "Rig 1" or basic_input["rig"] == "Rig 2":
            cost2 = assumptions[5]["Base Day Rate"]
            cost3 = cost4 = average_rop_day_rate.ix[45 - 30, "0 LTI"]
            cost5 = assumptions[5]["Additional Payment"] / 365.
            cost6 = assumptions[5]["Well Bonus"]
            # target_rop depends on the drilling days
            cost7 = average_rop_day_rate.ix[basic_input["target_rop"] - 30, 1]
            cost9 = rig1pe_summary.ix[:, "TOTAL COST"].sum() / basic_input["total_days"]
            cost10 =  3403000.00 
        else:
            cost2 = cost3 = cost4 = cost5 = cost6 = cost7 = cost9 = cost10 = 0

        cost8 = 0

        costs = [cost1, cost2, cost3, cost4, cost5, cost6, cost7, cost8, cost9, cost10]
        return nan_checker(costs)
    
    elif type_ == "drill_pipes":
        qty = np.zeros(4)
        if basic_input["rent_drill_pipes"]:
            qty[0:2] = basic_input["no_of_Joints"]
            qty[2:] = 50
        
        costs = [1.50, 47.02, 3250*0.05, 3250*0.02]
        return [qty.tolist(), costs]
    
    elif type_ == "completion_test":
        return [2500000, 1100000]
    
    elif type_ == "other_cementing":
        if basic_input["project_loc"] == "LGBU":
            return 13
        elif basic_input["project_loc"] == "BGBU":
            return 16
        elif basic_input["project_loc"] == "NIGBU":
            return 15
        elif basic_input["project_loc"] == "MAGBU":
            return 10
    
    elif type_ == "equipmental_rental":
        handling_hauling = pd.read_excel(dt_dir + "/handling_hauling.xlsx")
        equipment = pd.read_excel(dt_dir + "/equipment_rates.xlsx")
        rigmove = pd.read_excel(dt_dir + "/rigmove.xlsx")

        rig_mobilization_index = ["40 FT HI-BED TRAILER", "40 FT SEMI-LOW BED TRAILER (35T)", "35 FT LOW BED TRAILER (60T)", "50T CRANE", "70T CRANE", "180T CRANE", "PAYLOADER", "FORKLOADER", "TOWING EQUIPMENT", "BOOM TRUCK", "5TUT PUMP", "INTERISLAND RIGMOVE (ALLOCATED)"]
        
        if basic_input["project_loc"] == "LGBU":
            qty = [1, 1, 0, 0, 2, 2, 1]
        elif basic_input["project_loc"] == "BGBU":
            qty = [0, 0, 0, 0, 0, 1, 1]
        elif basic_input["project_loc"] == "NIGBU":
            qty = [1, 1, 0, 0, 2, 2, 1]
        elif basic_input["project_loc"] == "MAGBU":
            qty = [1, 1, 0, 0, 2, 2, 1]

        idx4_rm = rig_mobilization_index[3] == equipment.ix[:, "Equipment Rental"]        
        idx5_rm = rig_mobilization_index[4] == equipment.ix[:, "Equipment Rental"]        
        idx6_rm = rig_mobilization_index[5] == equipment.ix[:, "Equipment Rental"]        
        idx8_rm = rig_mobilization_index[7] == rigmove.ix[:, "ITEM"]
        idx11_rm = rig_mobilization_index[10] == equipment.ix[:, "Equipment Rental"]
        
        cost4_rm = np.array(equipment.ix[idx4_rm, "UNIT RATES"]).flatten()[0]        
        cost5_rm = np.array(equipment.ix[idx5_rm, "UNIT RATES"]).flatten()[0]        
        cost6_rm = np.array(equipment.ix[idx6_rm, "UNIT RATES"]).flatten()[0]
        cost8_rm = np.array(rigmove.ix[idx8_rm, "UNIT COST"]).flatten()[0]
        cost11_rm = np.array(equipment.ix[idx11_rm, "UNIT RATES"]).flatten()[0]
        
        costs = [cost4_rm, cost5_rm, cost6_rm, 0, cost11_rm, cost8_rm, 0]

        return [qty, nan_checker(costs)]

def compute_permutation(data, output):
    try:
        print "compute permutation request"

        input = data["basic_input_values"]
        permutation = data["permutation"]

        rop = [50, 60, 55, 45]
        print(permutation)
        print(rop)
        print("(****)")

        output = {}
        output["name"] =  str(permutation[0]) + "-" + str(permutation[1]) + "-" + str(permutation[2]) +  "-" + str(permutation[3]) +  "-" + str(permutation[4]) +  "-" + str(permutation[5])
		
        for rop in rop:
            input["target_rop"] = rop
            input["casing_surface"] = permutation[0]
            input["casing_intermediate"] = permutation[1]
            input["casing_production"] = permutation[2]
            input["casing_production_liner_1"] = permutation[3]
            input["casing_production_liner_2"] = permutation[4]
            input["casing_production_liner_3"] = permutation[5]


            cover_sheet_result = compute_cover_sheet(input, {})

            print("Total: " + str(cover_sheet_result["total"]))

            output["rop_" + str(rop) +"_total"] = cover_sheet_result["total"]

        return output

    except Exception as e:
        print e.message

def compute_permutation_count(data, output):
    try:
        print "compute permutation request"
        
        input = data["basic_input_values"]
        permutation = data["permutation"]

        print(permutation)
        print("(****)")

        surface          = [0]
        intermediate     = [0]
        prod_casing      = [0]
        prod_liner_1     = [0]
        prod_liner_2     = [0]
        prod_liner_3     = [0]


        if permutation["surface_from"] != "":
            surface = list(range(int(permutation["surface_from"]), int(permutation["surface_to"]) + 1, int(permutation["surface_increment"])))

        if permutation["intermediate_from"] != "":
            intermediate = list(range(int(permutation["intermediate_from"]), int(permutation["intermediate_to"]) + 1, int(permutation["intermediate_increment"])))

        if permutation["production_casing_from"] != "":
            prod_casing = list(range(int(permutation["production_casing_from"]), int(permutation["production_casing_to"]) + 1, int(permutation["production_casing_increment"])))

        if permutation["production_liner_1_from"] != "":
            prod_liner_1 = list(range(int(permutation["production_liner_1_from"]), int(permutation["production_liner_1_to"]) + 1,int(permutation["production_liner_1_increment"])))

        if permutation["production_liner_2_from"] != "":
            prod_liner_2 = list(range(int(permutation["production_liner_2_from"]), int(permutation["production_liner_2_to"]) + 1,int(permutation["production_liner_2_increment"])))

        if permutation["production_liner_3_from"] != "":
            prod_liner_3 = list(range(int(permutation["production_liner_3_from"]), int(permutation["production_liner_3_to"]) + 1,int(permutation["production_liner_3_increment"])))

        permutations = list(itertools.product(surface, intermediate, prod_casing, prod_liner_1, prod_liner_2, prod_liner_3))

        print("Number of permutations: " + str(len(permutations)))
        output["permutations"] = permutations
        
        return output
		
    except Exception as e:
        print e.message

def compute_cost_details(data, output):
    output = compute_cover_sheet(data = data, output = output, details = True)
    return output

def export_cover_sheet(data, output):
    output = export