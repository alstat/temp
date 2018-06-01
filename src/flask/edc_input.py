"""
Default Values
--------------
"""

drlg_input = {
    'surface': 2,
    'intermediate': 5,
    'prodn_casing': 10,
    'prodn_liner_1': 6,
    'prodn_liner_2': 5,
    'prodn_liner_3': np.nan,
    'reline': np.nan
}

flat_input = {
    'surface': 4,
    'intermediate': 4,
    'prodn_casing': 3,
    'prodn_liner_1': 2,
    'prodn_liner_2': 7,
    'prodn_liner_3': np.nan,
    'reline': np.nan
}

basic_input = {
    'well_name': '438D',  # *
    'rig': 'Rig 2',  # choices: 'Rig 1', 'Rig 2', 'Rig 5', 'Rig 12'
    'target_depth': 2500,  # *
    'rh_or_bh': 'Big Hole',  # choices: 'Regular Hole', 'Big Hole'
    'double_liner': True,
    'aerated_surface': True,
    'aerated_intermediate': True,
    'aerated_prodn_casing': True,
    'aerated_prodn_liner_1': True,
    'aerated_prodn_liner_2': True,
    'regular_bottom_section_for_bh': False,
    'rent_drill_pipes': False,
    'mob/demob_drillpipes': 'WITHIN SITE',  # WITHIN SITE or IMPORT, N/A
    'no_of_Joints': 311,  # *
    'yes_if_without_pre-installed_csg': True,
    'prodn_liner_3': False, # RIG 1 (LGBU - MAGBU), RIG 1 (LGBU - NIGBU), RIG 2 (NIGBU - BGBU), RIG 2 (NIGBU - MAGBU), Rig 12 (NIGBU - MAGBU)
    'interisland_rig_move': False,
    'b23': False,
    'project_loc': 'LGBU',  # choices: 'BGBU', 'LGBU', 'NIGBU', 'MAGBU'
    'rig_move_from': 'PAD',  # choices: 'PROJECT', 'PAD', 'SAME PAD'
    'rig_move_days': 13,
    'dhv_1': False,
    'dhv_2': 0,
    'pwd_fliner1': True,
    'pwd_fliner2': True,
    'chf': 'TESCO',  # choices: 'DESCO', 'TESCO'
    'mud_logging': True,
    'fe_fliner1': False,
    'fe_fliner2': False,
    'reline': False,
    'forex_ph_us': 51.,
    'diesel_ph_us': 36.
}

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

casing_depth_input = {
    'surface':  100,
    'intermediate':  560,
    'prodn_casing': 1260,
    'prodn_liner_1': 1900,
    'prodn_liner_2': 2500,
    'prodn_liner_3': np.nan,
    'reline': np.nan
}

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

cement_acid = {
    'cement': {
        'surface': 1,
        'intermediate': 1,
        'prodn_casing': 1,
        'prodn_liner_1': 1,
        'prodn_liner_2': 1,
        'prodn_liner_3': np.nan,
    },
    'acid': {
        'surface': False,
        'intermediate': False,
        'prodn_casing': False,
        'prodn_liner_1': None,
        'prodn_liner_2': None,
        'prodn_liner_3': None,
    },
    'top_job': {
        'surface': 1,
        'intermediate': 1,
        'prodn_casing': 1,
        'prodn_liner_1': 0,
        'prodn_liner_2': 0,
        'prodn_liner_3': 0,
    }
}

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
