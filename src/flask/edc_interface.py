import numpy as np
import pandas as pd
import os
import sys
import itertools
import re

sys.path.insert(0, ".")
dt_dir = "./data"

# comment out this line during production
# os.chdir("/Users/al-ahmadgaidasaad/Documents/WORK/NEURAL-MECHANICS/DEV/edc/src/flask")

from edc_source import Drilling_Days, Hole_Casing, Cost_Center, header
from edc_assumptions import Assumptions
from edc_interface_inputs import inputs
from edc_cost import Unit_Rate

def roundup(x, y = 1):
    """
    Implementation of Excel's ROUNDUP function
    """
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

def compute_basic_input(data):
    """
    Interface for Computing Necessary Items in Basic Input
    """
    global inventory

    inputs(data)

    basic_input['total_days']         = basic_input['rig_move_days'] + Drilling_Days(drlg_input, flat_input).total()
    basic_input['drilling_days']      = Drilling_Days(drlg_input, flat_input).cell(basic_input)
    basic_input['target_rop']         = Drilling_Days(drlg_input, flat_input).target_rop(basic_input)
    basic_input['drilling_row_total'] = Drilling_Days(drlg_input, flat_input).row_total()

    inventory       = pd.read_excel(dt_dir + '/inventory.xlsx')

def compute_cover_sheet(data, output, details = False):
    """
    Interface for Computing the Cover Sheet
    """

    compute_basic_input(data)

    """
    Header
    """
    head = header(basic_input, assumptions, drlg_input, flat_input)

    """
    Assumptions
    """
    fuel_asmpt        = Assumptions(basic_input, assumptions).fuel(dt_dir + '/fuel.xlsx')
    
    mud_consumables   = Assumptions(basic_input, assumptions).mud_chemicals(dt_dir + '/mud_consumables.xlsx')
    hole_depth        = Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)

    cemt              = Assumptions(basic_input, assumptions).cement_additives()
    cement_slb_asmpt2 = Assumptions(basic_input, assumptions).cement_additives_asmpt(dt_dir + '/equipmental_rentals.xlsx')

    rckb_asmpt        = Assumptions(basic_input, assumptions).cement_additives(dt_dir + '/rockbit_1.xlsx')
    rckb_qty          = {}.fromkeys(rckb_asmpt.index, False)
    for i in np.arange(16, 19):
        rckb_qty[list(rckb_qty.keys())[i]] = True

    path1             = [dt_dir + '/big_hole.xlsx', dt_dir + '/big_hole_BGBU.xlsx', dt_dir + '/big_hole_NIGBU.xlsx', dt_dir + '/big_hole_MAGBU.xlsx']
    path2             = [dt_dir + '/regular_hole.xlsx', dt_dir + '/regular_hole_BGBU.xlsx', dt_dir + '/regular_hole_NIGBU.xlsx', dt_dir + '/regular_hole_MAGBU.xlsx']
    big_reg_hole      = Assumptions(basic_input, assumptions).casings(path1, path2)
    big_hole          = big_reg_hole[0]
    reg_hole          = big_reg_hole[1]

    """
    Unit Cost
    """
    fuel_cost            = Unit_Rate(basic_input, assumptions, inventory).fuel()
    lubricants_cost      = Unit_Rate(basic_input, assumptions, inventory).lubricants()
    mud_consumables_cost = Unit_Rate(basic_input, assumptions, inventory).mud_chemicals()
    cement_cost          = Unit_Rate(basic_input, assumptions, inventory).cement_additives(dt_dir + '/equipmental_rentals.xlsx')
    rckb_unit_scost      = np.array(Unit_Rate(basic_input, inventory).rockbits().ix[:, 'smith_unit_cost'])
    rckb_unit_hcost      = np.array(Unit_Rate(basic_input, inventory).rockbits().ix[:, 'hughes_unit_cost'])
    cost_ds              = Unit_Rate(basic_input, assumptions, inventory).drilling_supplies()

    if details is True:
        output['fuels']                         = Cost_Center(basic_input, assumptions, head).fuel(fuel_asmpt, drlg_input, flat_input, unit_cost = fuel_cost).to_json(orient = 'records')
        output['lubricants']                    = Cost_Center(basic_input, assumptions, head).lubricants(fuel_asmpt, drlg_input, flat_input, unit_cost = lubricants_cost).ix[:, 1:].to_json(orient = 'records')
        output['fuels_qty']                     = Cost_Center(basic_input, assumptions, head).fuel(fuel_asmpt, drlg_input, flat_input).to_json(orient = 'records')

        output['mud_and_chemicals']             = Cost_Center(basic_input, assumptions, head).mud_chemicals(mud_consumables, hole_depth, casing_depth_input, unit_cost = mud_consumables_cost).ix[:, 1:].to_json(orient = 'records')
        output['mud_and_chemicals_qty']         = Cost_Center(basic_input, assumptions, head).mud_chemicals(mud_consumables, hole_depth, casing_depth_input).ix[:, 1:].to_json(orient = 'records')

        output['cements_and_additives']         = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2, unit_cost = cement_cost).to_json(orient = 'records')
        output['cements_and_additives_qty']     = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2).to_json(orient = 'records')        

        output['smith']                         = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rckb_unit_scost).to_json(orient = 'records')
        output['hughes']                        = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rckb_unit_hcost, category = 'HUGHES').to_json(orient = 'records')

        output['drilling_supplies']             = Cost_Center(basic_input, assumptions, head).drilling_supplies(unit_cost = cost_ds).ix[:, 1:].to_json(orient = 'records')        
        output['drilling_supplies_qty']         = Cost_Center(basic_input, assumptions, head).drilling_supplies(unit_cost = cost_ds).ix[:, 1:].to_json(orient = 'records')

        output['casings']                       = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole, unit_cost = True).ix[:, 1:].to_json(orient = 'records')
        output['casings_qty']                   = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole).ix[:, 1:].to_json(orient = 'records')
        
    else:
        output['fuels']                         = roundup(Cost_Center(basic_input, assumptions, head).fuel(fuel_asmpt, drlg_input, flat_input, unit_cost = fuel_cost).sum().sum(), 1000)
        
        output['lubricants']                    = roundup(Cost_Center(basic_input, assumptions, head).lubricants(fuel_asmpt, drlg_input, flat_input, unit_cost = lubricants_cost).ix[:, 1:].sum().sum(), 1000)
    
        output['mud_and_chemicals']             = roundup(Cost_Center(basic_input, assumptions, head).mud_chemicals(mud_consumables, hole_depth, casing_depth_input, unit_cost = mud_consumables_cost).ix[:, 1:].sum().sum(), 1000)

        output['cements_and_additives']         = roundup(Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2, unit_cost = cement_cost).sum().sum(), 1000)

        smith                                   = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rckb_unit_scost).sum().sum()
        hughes                                  = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rckb_unit_hcost, category = 'HUGHES').sum().sum()
        output['rockbits']                      = roundup(smith + hughes, 1000)
        
        output['drilling_supplies']             = roundup(Cost_Center(basic_input, assumptions, head).drilling_supplies(unit_cost = cost_ds).ix[:, 1:].sum().sum(), 1000)
        output['casings']                       = roundup(Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole, unit_cost = True).ix[:, 1:].sum().sum(), 1000)

        

    if details is True:
        output['drilling_supplies']             = Cost_Center(basic_input, assumptions, head).drilling_supplies(unit_cost = cost_ds).ix[:, 1:].to_json(orient = 'records')
        output['casings']                       = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole, unit_cost = True).ix[:, 1:].to_json(orient = 'records')
        output['drilling_supplies_qty']         = Cost_Center(basic_input, assumptions, head).drilling_supplies(unit_cost = cost_ds).ix[:, 1:].to_json(orient = 'records')
        output['casings_qty']                   = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole).ix[:, 1:].to_json(orient = 'records')
    else:
        output['drilling_supplies']             = roundup(Cost_Center(basic_input, assumptions, head).drilling_supplies(unit_cost = cost_ds).ix[:, 1:].sum().sum(), 1000)
        output['casings']                       = roundup(Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole, unit_cost = True).ix[:, 1:].sum().sum(), 1000)
