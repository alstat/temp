def inputs(data):
    global drlg_input, flat_input, basic_input, casing_depth_input, assumptions

    drlg_input = {
        'surface'       : 0 if data['surface_DRLG'] == '' else float(data['surface_DRLG']),
        'intermediate'  : 0 if data['intermediate_DRLG'] == '' else float(data['intermediate_DRLG']),
        'production'    : 0 if data['production_casing_DRLG'] == '' else float(data['production_casing_DRLG']),
        'prodn_liner_1' : 0 if data['production_liner_1_DRLG'] == '' else float(data['production_liner_1_DRLG']),
        'prodn_liner_2' : 0 if data['production_liner_2_DRLG'] == '' else float(data['production_liner_2_DRLG']),
        'prodn_liner_3' : 0 if data['production_liner_3_DRLG'] == '' else float(data['production_liner_3_DRLG']),
        'reline'        : 0 if data['reline_DRLG'] == '' else float(data['reline_DRLG'])
    }

    flat_input = {
        'surface'       : 0 if data['surface_FLAT'] == '' else float(data['surface_FLAT']), 
        'intermediate'  : 0 if data['intermediate_FLAT'] == '' else float(data['intermediate_FLAT']),
        'production'    : 0 if data['production_casing_FLAT'] == '' else float(data['production_casing_FLAT']),
        'prodn_liner_1' : 0 if data['production_liner_1_FLAT'] == '' else float(data['production_liner_1_FLAT']),
        'prodn_liner_2' : 0 if data['production_liner_2_FLAT'] == '' else float(data['production_liner_2_FLAT']),
        'prodn_liner_3' : 0 if data['production_liner_3_FLAT'] == '' else float(data['production_liner_3_FLAT']),
        'reline'        : 0 if data['reline_FLAT'] == '' else float(data['reline_FLAT'])
        }
  
    basic_input = {
        'well_name'                       : str(data['well_name']), #*
        'rig'                             : str(data['rig']), # choices: 'Rig 1', 'Rig 2', 'Rig 5', 'Rig 12'
        'target_depth'                    : float(data['target_depth']),   #*
        'rh_or_bh'                        : str(data['rh_bh']), # choices: 'Regular Hole', 'Big Hole'
        'double_liner'                    : False if data['double_liner'] == 'No' else True,
        'aerated_surface'                 : False if data['aerated_surface'] == 'No' else True,
        'aerated_intermediate'            : False if data['aerated_production_intermediate'] == 'No' else True,
        'aerated_prodn_casing'            : False if data['aerated_production_casing'] == 'No' else True,
        'aerated_prodn_liner_1'           : False if data['aerated_production_liner_1'] == 'No' else True,
        'aerated_prodn_liner_2'           : False if data['aerated_production_liner_2'] == 'No' else True,
        'regular_bottom_section_for_bh'   : False if data['reg_bottom_bh'] == 'No' else True,
        'rent_drill_pipes'                : False if data['rent_drill_pipes'] == 'No' else True,
        'mob/demob_drillpipes'            : str(data['mob_demob_drillpipes']),
        'no_of_Joints'                    : float(data['no_of_joints']),
        'yes_if_without_pre-installed_csg': False if data['yes_wo_preinstalled_casing'] == 'No' else True,
        'prodn_liner_3'                   : False if data['prod_liner_3'] == 'No' else True,
        'interisland_rig_move'            : False if data['interisland_rigmove'] == 'No' else str(data['interisland_rigmove']),
        'b23'                             : False,
        'project_loc'                     : str(data['project_location']), # choices: 'BGBU', 'LGBU', 'NIGBU', 'MAGBU'
        'rig_move_from'                   : str(data['rig_move_from']), # choices: 'PROJECT', 'PAD', 'SAME PAD'
        'rig_move_days'                   : float(data['rig_move_days']),
        'dhv_1'                           : False if data['dhv_1'] == 'No' else True,
        'dhv_2'                           : float(data['dhv_2']),
        'pwd_fliner1'                     : False if data['pwd_fliner_1'] == 'No' else True,
        'pwd_fliner2'                     : False if data['pwd_fliner_2'] == 'No' else True,
        'chf'                             : str(data['chf']), # choices: 'DESCO', 'TESCO'
        'mud_logging'                     : False if data['mud_logging'] == 'No' else True,
        'fe_fliner1'                      : False if data['formation_eval_fliner_1'] == 'No' else True,
        'fe_fliner2'                      : False if data['formation_eval_fliner_2'] == 'No' else True,
        'reline'                          : False if data['reline'] == 'No' else True,
        'forex_ph_us'                     : float(data['forex_php_us']),
        'diesel_ph_us'                    : float(data['diesel_php_us'])
    }

    # basic_input = {
    #     'well_name'                       : data['well_name'], #*
    #     'rig'                             : data['rig'], # choices: 'Rig 1', 'Rig 2', 'Rig 5', 'Rig 12'
    #     'target_depth'                    : float(data['target_depth']),   #*
    #     'rh_or_bh'                        : data['rh_bh'], # choices: 'Regular Hole', 'Big Hole'
    #     'double_liner'                    : False if data['double_liner'] == 'No' else True,
    #     'aerated_surface'                 : False if data['aerated_surface'] == 'No' else True,
    #     'aerated_intermediate'            : False if data['aerated_production_intermediate'] == 'No' else True,
    #     'aerated_prodn_casing'            : False if data['aerated_production_casing'] == 'No' else True,
    #     'aerated_prodn_liner_1'           : False if data['aerated_production_liner_1'] == 'No' else True,
    #     'aerated_prodn_liner_2'           : False if data['aerated_production_liner_2'] == 'No' else True,
    #     'regular_bottom_section_for_bh'   : False if data['reg_bottom_bh'] == 'No' else True,
    #     'rent_drill_pipes'                : False if data['rent_drill_pipes'] == 'No' else True,
    #     'mob/demob_drillpipes'            : data['mob_demob_drillpipes'],
    #     'no_of_Joints'                    : float(data['no_of_joints']),
    #     'yes_if_without_pre-installed_csg': False if data['yes_wo_preinstalled_casing'] == 'No' else True,
    #     'prodn_liner_3'                   : False if data['prod_liner_3'] == 'No' else True,
    #     'interisland_rig_move'            : False,
    #     'b23'                             : False,
    #     'project_loc'                     : data['project_location'], # choices: 'BGBU', 'LGBU', 'NIGBU', 'MAGBU'
    #     'rig_move_from'                   : data['rig_move_from'], # choices: 'PROJECT', 'PAD', 'SAME PAD'
    #     'rig_move_days'                   : float(data['rig_move_days']),
    #     'dhv_1'                           : False if data['dhv_1'] == 'No' else True,
    #     'dhv_2'                           : float(data['dhv_2']),
    #     'pwd_fliner1'                     : False if data['pwd_fliner_1'] == 'No' else True,
    #     'pwd_fliner2'                     : False if data['pwd_fliner_2'] == 'No' else True,
    #     'chf'                             : data['chf'], # choices: 'DESCO', 'TESCO'
    #     'mud_logging'                     : False if data['mud_logging'] == 'No' else True,
    #     'fe_fliner1'                      : False if data['formation_eval_fliner_1'] == 'No' else True,
    #     'fe_fliner2'                      : False if data['formation_eval_fliner_2'] == 'No' else True,
    #     'reline'                          : False if data['reline'] == 'No' else True,
    #     'forex_ph_us'                     : 50.,
    #     'diesel_ph_us'                    : 30.
    # }

    # hole_case_sizes_asmpt = {
    #     'hole'  : {
    #         'bh' : {
    #             'surface'       : 0 if data['hole_bh_surface'] == '' else float(data['hole_bh_surface']),
    #             'intermediate'  : 0 if data['hole_bh_intermediate'] == '' else float(data['hole_bh_intermediate']),
    #             'prodn_casing'  : 0 if data['hole_bh_prodn_casing'] == '' else float(data['hole_bh_prodn_casing']),
    #             'prodn_liner_1' : 0 if data['hole_bh_prodn_liner_1'] == '' else float(data['hole_bh_prodn_liner_1']),
    #             'prodn_liner_2' : 0 if data['hole_bh_prodn_liner_2'] == '' else float(data['hole_bh_prodn_liner_2']),
    #             'prodn_liner_3' : 0 if data['hole_bh_prodn_liner_3'] == '' else float(data['hole_bh_prodn_liner_3']),
    #         },
    #         'rh' : {
    #             'surface'       : 0 if data['hole_rh_surface'] == '' else float(data['hole_rh_surface']),
    #             'intermediate'  : 0 if data['hole_rh_intermediate'] == '' else float(data['hole_rh_intermediate']),
    #             'prodn_casing'  : 0 if data['hole_rh_prodn_casing'] == '' else float(data['hole_rh_prodn_casing']),
    #             'prodn_liner_1' : 0 if data['hole_rh_prodn_liner_1'] == '' else float(data['hole_rh_prodn_liner_1']),
    #             'prodn_liner_2' : 0 if data['hole_rh_prodn_liner_2'] == '' else float(data['hole_rh_prodn_liner_2']),
    #             'prodn_liner_3' : 0 if data['hole_rh_prodn_liner_3'] == '' else float(data['hole_rh_prodn_liner_3']),
    #         }
    #     },
    #     'case' : {
    #         'bh' : {
    #             'surface'       : 0 if data['case_bh_surface'] == '' else float(data['case_bh_surface']),
    #             'intermediate'  : 0 if data['case_bh_intermediate'] == '' else float(data['case_bh_intermediate']),
    #             'prodn_casing'  : 0 if data['case_bh_prodn_casing'] == '' else float(data['case_bh_prodn_casing']),
    #             'prodn_liner_1' : 0 if data['case_bh_prodn_liner_1'] == '' else float(data['case_bh_prodn_liner_1']),
    #             'prodn_liner_2' : 0 if data['case_bh_prodn_liner_2'] == '' else float(data['case_bh_prodn_liner_2']),
    #             'prodn_liner_3' : 0 if data['case_bh_prodn_liner_3'] == '' else float(data['case_bh_prodn_liner_3']),
    #         },
    #         'rh' : {
    #             'surface'       : 0 if data['case_rh_surface'] == '' else float(data['case_rh_surface']),
    #             'intermediate'  : 0 if data['case_rh_intermediate'] == '' else float(data['case_rh_intermediate']),
    #             'prodn_casing'  : 0 if data['case_rh_prodn_casing'] == '' else float(data['case_rh_prodn_casing']),
    #             'prodn_liner_1' : 0 if data['case_rh_prodn_liner_1'] == '' else float(data['case_rh_prodn_liner_1']),
    #             'prodn_liner_2' : 0 if data['case_rh_prodn_liner_2'] == '' else float(data['case_rh_prodn_liner_2']),
    #             'prodn_liner_3' : 0 if data['case_rh_prodn_liner_3'] == '' else float(data['case_rh_prodn_liner_3'])
    #         }
    #     }
    # }

    # other_hole_case_asmpt = {
    #     'hole' : {
    #         'surface'       : 0 if data['other_hole_asmpt_surface'] == '' else float(data['other_hole_asmpt_surface']),
    #         'intermediate'  : 0 if data['other_hole_asmpt_intermediate'] == '' else float(data['other_hole_asmpt_intermediate']),
    #         'prodn_casing'  : 0 if data['other_hole_asmpt_prodn_casing'] == '' else float(data['other_hole_asmpt_prodn_casing']),
    #         'prodn_liner_1' : 0 if data['other_hole_asmpt_prodn_liner_1'] == '' else float(data['other_hole_asmpt_prodn_liner_1']),
    #         'prodn_liner_2' : 0 if data['other_hole_asmpt_prodn_liner_2'] == '' else float(data['other_hole_asmpt_prodn_liner_2']),
    #         'prodn_liner_3' : 0 if data['other_hole_asmpt_prodn_liner_3'] == '' else float(data['other_hole_asmpt_prodn_liner_3']),
    #         'no_label_1'    : 0 if data['other_hole_asmpt_no_label_1'] == '' else float(data['other_hole_asmpt_no_label_1']),
    #         'no_label_2'    : 0 if data['other_hole_asmpt_no_label_2'] == '' else float(data['other_hole_asmpt_no_label_2']),
    #         'no_label_3'    : 0 if data['other_hole_asmpt_no_label_3'] == '' else float(data['other_hole_asmpt_no_label_3'])
    #     },
    #     'case' : {
    #         'surface'       : 0 if data['other_case_asmpt_surface'] == '' else float(data['other_case_asmpt_surface']),
    #         'intermediate'  : 0 if data['other_case_asmpt_intermediate'] == '' else float(data['other_case_asmpt_intermediate']),
    #         'prodn_casing'  : 0 if data['other_case_asmpt_prodn_casing'] == '' else float(data['other_case_asmpt_prodn_casing']),
    #         'prodn_liner_1' : 0 if data['other_case_asmpt_prodn_liner_1'] == '' else float(data['other_case_asmpt_prodn_liner_1']),
    #         'prodn_liner_2' : 0 if data['other_case_asmpt_prodn_liner_2'] == '' else float(data['other_case_asmpt_prodn_liner_2']),
    #         'prodn_liner_3' : 0 if data['other_case_asmpt_prodn_liner_3'] == '' else float(data['other_case_asmpt_prodn_liner_3']),
    #         'no_label_1'    : 0 if data['other_case_asmpt_no_label_1'] == '' else float(data['other_case_asmpt_no_label_1']),
    #         'no_label_2'    : 0 if data['other_case_asmpt_no_label_2'] == '' else float(data['other_case_asmpt_no_label_2']),
    #         'no_label_3'    : 0 if data['other_case_asmpt_no_label_3'] == '' else float(data['other_case_asmpt_no_label_3'])
    #     },
    #     'id' : {
    #         'surface'       : 0 if data['other_id_asmpt_surface'] == '' else float(data['other_id_asmpt_surface']),
    #         'intermediate'  : 0 if data['other_id_asmpt_intermediate'] == '' else float(data['other_id_asmpt_intermediate']),
    #         'prodn_casing'  : 0 if data['other_id_asmpt_prodn_casing'] == '' else float(data['other_id_asmpt_prodn_casing']),
    #         'prodn_liner_1' : 0 if data['other_id_asmpt_prodn_liner_1'] == '' else float(data['other_id_asmpt_prodn_liner_1']),
    #         'prodn_liner_2' : 0 if data['other_id_asmpt_prodn_liner_2'] == '' else float(data['other_id_asmpt_prodn_liner_2']),
    #         'prodn_liner_3' : 0 if data['other_id_asmpt_prodn_liner_3'] == '' else float(data['other_id_asmpt_prodn_liner_3']),
    #         'no_label_1'    : 0 if data['other_id_asmpt_no_label_1'] == '' else float(data['other_id_asmpt_no_label_1']),
    #         'no_label_2'    : 0 if data['other_id_asmpt_no_label_2'] == '' else float(data['other_id_asmpt_no_label_2']),
    #         'no_label_3'    : 0 if data['other_id_asmpt_no_label_3'] == '' else float(data['other_id_asmpt_no_label_3'])
    #     }
    # }
    
    casing_depth_input = {
        'surface'       : 0 if data['casing_surface'] == '' else float(data['casing_surface']),
        'intermediate'  : 0 if data['casing_intermediate'] == '' else float(data['casing_intermediate']),
        'prodn_casing'  : 0 if data['casing_production'] == '' else float(data['casing_production']),
        'prodn_liner_1' : 0 if data['casing_production_liner_1'] == '' else float(data['casing_production_liner_1']),
        'prodn_liner_2' : 0 if data['casing_production_liner_2'] == '' else float(data['casing_production_liner_2']),
        'prodn_liner_3' : 0 if data['casing_production_liner_3'] == '' else float(data['casing_production_liner_3']),
        'reline'        : 0 if data['casing_reline'] == '' else float(data['casing_reline'])
    }

    # casing_id = {
    #     'bh' : {
    #         'surface'       : 0 if data['casing_id_bh_surface'] == '' else float(data['casing_id_bh_surface']),
    #         'intermediate'  : 0 if data['casing_id_bh_intermediate'] == '' else float(data['casing_id_bh_intermediate']),
    #         'prodn_casing'  : 0 if data['casing_id_bh_prodn_casing'] == '' else float(data['casing_id_bh_prodn_casing']),
    #         'prodn_liner_1' : 0 if data['casing_id_bh_prodn_liner_1'] == '' else float(data['casing_id_bh_prodn_liner_1']),
    #         'prodn_liner_2' : 0 if data['casing_id_bh_prodn_liner_2'] == '' else float(data['casing_id_bh_prodn_liner_2']),
    #         'prodn_liner_3' : 0 if data['casing_id_bh_prodn_liner_3'] == '' else float(data['casing_id_bh_prodn_liner_3']),
    #         'reline'        : 0 if data['casing_id_bh_reline'] == '' else float(data['casing_id_bh_reline'])
    #     },
    #     'rh' : {
    #         'surface'       : 0 if data['casing_id_rh_surface'] == '' else float(data['casing_id_rh_surface']),
    #         'intermediate'  : 0 if data['casing_id_rh_intermediate'] == '' else float(data['casing_id_rh_intermediate']),
    #         'prodn_casing'  : 0 if data['casing_id_rh_prodn_casing'] == '' else float(data['casing_id_rh_prodn_casing']),
    #         'prodn_liner_1' : 0 if data['casing_id_rh_prodn_liner_1'] == '' else float(data['casing_id_rh_prodn_liner_1']),
    #         'prodn_liner_2' : 0 if data['casing_id_rh_prodn_liner_2'] == '' else float(data['casing_id_rh_prodn_liner_2']),
    #         'prodn_liner_3' : 0 if data['casing_id_rh_prodn_liner_3'] == '' else float(data['casing_id_rh_prodn_liner_3']),
    #         'reline'        : 0 if data['casing_id_rh_reline'] == '' else float(data['casing_id_rh_reline'])
    #     }
    # }

    cement_acid = {
        'cement' : {
            'surface'       : 0 if data['surface_cement_plug'] == '' else float(data['surface_cement_plug']),
            'intermediate'  : 0 if data['intermediate_cement_plug'] == '' else float(data['intermediate_cement_plug']),
            'prodn_casing'  : 0 if data['production_casing_cement_plug'] == '' else float(data['production_casing_cement_plug']),
            'prodn_liner_1' : 0 if data['production_liner_1_cement_plug'] == '' else float(data['production_liner_1_cement_plug']),
            'prodn_liner_2' : 0 if data['production_liner_2_cement_plug'] == '' else float(data['production_liner_2_cement_plug']),
            'prodn_liner_3' : 0 if data['production_liner_3_cement_plug'] == '' else float(data['production_liner_3_cement_plug'])
        },
        'acid' : {
            'surface'       : False if data['acid_surface'] == 'No' else None if data['acid_surface'] == '' else True,
            'intermediate'  : False if data['acid_intermediate'] == 'No' else None if data['acid_intermediate'] == '' else True,
            'prodn_casing'  : False if data['acid_prodn_casing'] == 'No' else None if data['acid_prodn_casing'] == '' else True,
            'prodn_liner_1' : False if data['acid_prodn_liner_1'] == 'No' else None if data['acid_prodn_liner_1'] == '' else True,
            'prodn_liner_2' : False if data['acid_prodn_liner_2'] == 'No' else None if data['acid_prodn_liner_2'] == '' else True,
            'prodn_liner_3' : False if data['acid_prodn_liner_3'] == 'No' else None if data['acid_prodn_liner_3'] == '' else True
        },
        'top_job' : {
            'surface'       : 0 if data['surface_top_job'] == '' else float(data['surface_top_job']),
            'intermediate'  : 0 if data['intermediate_top_job'] == '' else float(data['intermediate_top_job']),
            'prodn_casing'  : 0 if data['production_casing_top_job'] == '' else float(data['production_casing_top_job']),
            'prodn_liner_1' : 0 if data['production_liner_1_top_job'] == '' else float(data['production_liner_1_top_job']),
            'prodn_liner_2' : 0 if data['production_liner_2_top_job'] == '' else float(data['production_liner_2_top_job']),
            'prodn_liner_3' : 0 if data['production_liner_3_top_job'] == '' else float(data['production_liner_3_top_job'])
        }
    }

    # # Other Assumptions
    # tpwsri = {
    #     'Average ROP Day Rate' : None if data['tpwsri_ave_rop_rate'] == '' else float(data['tpwsri_ave_rop_rate']),
    #     'Base Day Rate' : None if data['tpwsri_base_day_rate'] == '' else float(data['tpwsri_base_day_rate']),
    #     'Standby Rate' : None if data['tpwsri_standby_rate'] == '' else float(data['tpwsri_standby_rate']),
    #     'Move Fee' : None if data['tpwsri_movefee'] == '' else float(data['tpwsri_movefee']),
    #     'Rig Move Rate' :  None if data['tpwsri_rigmove_rate'] == '' else float(data['tpwsri_rigmove_rate']),
    #     'Additional Payment' : None if data['tpwsri_additional_payment'] == '' else float(data['tpwsri_additional_payment']),
    #     'Penalty Payment' : None if data['tpwsri_penalty_payment'] == '' else float(data['tpwsri_penalty_payment']),
    #     'Well Bonus' : None if data['tpwsri_well_bonus'] == '' else float(data['tpwsri_well_bonus']),
    #     'Well ROP Bonus' : None if data['tpwsri_well_rop_bonus'] == '' else float(data['tpwsri_well_rop_bonus'])
    # }

    hole_case_sizes_asmpt = {
        'hole': {
            'bh': {
                'surface': 32,
                'intermediate': 23,
                'prodn_casing': 17,
                'prodn_liner_1': 12.25,
                'prodn_liner_2':  9.875,
                'prodn_liner_3':  7.875,
            },
            'rh': {
                'surface': 26,
                'intermediate': 17,
                'prodn_casing': 12.25,
                'prodn_liner_1':  8.5,
                'prodn_liner_2':  6,
                'prodn_liner_3': np.nan,
            }
        },
        'case': {
            'bh': {
                'surface': 26,
                'intermediate': 18.625,
                'prodn_casing': 13.375,
                'prodn_liner_1': 10.75,
                'prodn_liner_2':  8.625,
                'prodn_liner_3':  7.,
            },
            'rh': {
                'surface': 20,
                'intermediate': 13.375,
                'prodn_casing':  9.625,
                'prodn_liner_1':  7,
                'prodn_liner_2':  5,
                'prodn_liner_3': np.nan,
            }
        }
    }

    other_hole_case_asmpt = {
        'hole': {
            'surface': 32,
            'intermediate': 23,
            'prodn_casing': 17,
            'prodn_liner_1': 12.25,
            'prodn_liner_2': 12.25,
            'prodn_liner_3': 9.875,
            'no_label_1': 7.875,
            'no_label_2': 8.5,
            'no_label_3': 6
        },
        'case': {
            'surface': 26,
            'intermediate': 18.625,
            'prodn_casing': 13.375,
            'prodn_liner_1': 10.75,
            'prodn_liner_2':  9.625,
            'prodn_liner_3':  8.625,
            'no_label_1':  7,
            'no_label_2':  7,
            'no_label_3':  5
        },
        'id': {
            'surface': 24.5,
            'intermediate': 17.467,
            'prodn_casing': 12.415,
            'prodn_liner_1': 10.05,
            'prodn_liner_2':  8.755,
            'prodn_liner_3':  8.097,
            'no_label_1':  6.366,
            'no_label_2':  6.276,
            'no_label_3':  4.408
        }
    }

    # casing_depth_input = {
    #     'surface':  100,
    #     'intermediate':  560,
    #     'prodn_casing': 1260,
    #     'prodn_liner_1': 1900,
    #     'prodn_liner_2': 2500,
    #     'prodn_liner_3': np.nan,
    #     'reline': np.nan
    # }

    casing_id = {
        'bh': {
            'surface': 24.5,
            'intermediate': 17.467,
            'prodn_casing': 12.415,
            'prodn_liner_1': 10.05,
            'prodn_liner_2':  8.097,
            'prodn_liner_3':  6.366,
            'reline': np.nan
        },
        'rh': {
            'surface': 19.312,
            'intermediate': 12.615,
            'prodn_casing':  8.755,
            'prodn_liner_1':  6.276,
            'prodn_liner_2':  4.408,
            'prodn_liner_3': np.nan,
            'reline': np.nan
        }
    }

    # cement_acid = {
    #     'cement': {
    #         'surface': 1,
    #         'intermediate': 1,
    #         'prodn_casing': 1,
    #         'prodn_liner_1': 1,
    #         'prodn_liner_2': 1,
    #         'prodn_liner_3': np.nan,
    #     },
    #     'acid': {
    #         'surface': False,
    #         'intermediate': False,
    #         'prodn_casing': False,
    #         'prodn_liner_1': None,
    #         'prodn_liner_2': None,
    #         'prodn_liner_3': None,
    #     },
    #     'top_job': {
    #         'surface': 1,
    #         'intermediate': 1,
    #         'prodn_casing': 1,
    #         'prodn_liner_1': 0,
    #         'prodn_liner_2': 0,
    #         'prodn_liner_3': 0,
    #     }
    # }

    # Other Assumptions
    tpwsri = {
        'Average ROP Day Rate': None,
        'Base Day Rate': 1596000,
        'Standby Rate': 1449000,
        'Move Fee': 16721000.00,
        'Rig Move Rate':  20748000.00,
        'Additional Payment': 16105885.68,
        'Penalty Payment': None,
        'Well Bonus': 2000000.00,
        'Well ROP Bonus': None
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