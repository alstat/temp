import numpy as np
import pandas as pd
import os

os.chdir("/Users/al-ahmadgaidasaad/Documents/WORK/NEURAL-MECHANICS/EDC/src/flask")
from edc_assumptions import Assumptions
from edc_source import Drilling_Days, Hole_Casing, Unit_Rate, Cost_Center, header

in_dir = "/Users/al-ahmadgaidasaad/Documents/WORK/NEURAL-MECHANICS/EDC/src/flask/edc_input.py"
dt_dir = "/Users/al-ahmadgaidasaad/Documents/work/neural-mechanics/EDC/src/flask/data"

exec(open(in_dir).read())

"""
Implementation of Excel's ROUNDUP function
"""
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

"""
Compute Basic Input Values
"""
basic_input['total_days']         = basic_input['rig_move_days'] + Drilling_Days(drlg_input, flat_input).total()
basic_input['drilling_days']      = Drilling_Days(drlg_input, flat_input).cell(basic_input)
basic_input['target_rop']         = Drilling_Days(drlg_input, flat_input).target_rop(basic_input)
basic_input['drilling_row_total'] = Drilling_Days(drlg_input, flat_input).row_total()

"""
Hole Casing Summary
""" 
Hole_Casing(basic_input, category = 'size').compute(assumptions)[1]
Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)
Hole_Casing(basic_input, category = 'case_id').compute(assumptions)
Hole_Casing(basic_input, category = 'hole_length').compute(assumptions)

"""
-------------------------
COST DETAILS COMPUTATIONS
-------------------------
"""

"""
Compute Assumptions
"""
cement_slb = Assumptions(basic_input, assumptions)
cemt = cement_slb.cement_slb()

"""
Import Input Data
"""
inventory       = pd.read_excel(dt_dir + '/inventory.xlsx')
fuel_rawdf      = pd.read_excel(dt_dir + '/fuel.xlsx')
if basic_input['double_liner']:
    fuel_asmpt      = fuel_rawdf.ix[0:6, 4:15]
else:
    fuel_asmpt      = fuel_rawdf.ix[0:6, 4:13]

cemt_asmpt      = pd.read_excel(dt_dir + '/cement_additives.xlsx').set_index('Index')
rckb_asmpt      = pd.read_excel(dt_dir + '/rockbit_1.xlsx').set_index('Rockbits')

rckb_unit_scost = np.array(Unit_Rate(basic_input, inventory).rockbits().ix[:, 'smith_unit_cost'])
rckb_unit_hcost = np.array(Unit_Rate(basic_input, inventory).rockbits().ix[:, 'hughes_unit_cost'])
# print rckb_unit_hcost
# print rckb_unit_scost
# if basic_input['project_loc'] == 'LGBU':
#     rckb_unit_scost = pd.read_excel(dt_dir + '/rockbit.xlsx').SMITH.values
#     rckb_unit_hcost = pd.read_excel(dt_dir + '/rockbit.xlsx').HUGHES.values
# elif basic_input['project_loc'] == 'BGBU':
#     rckb_unit_scost = [1120775.21, 1875294.22, 1058281.27, 1058281.27, 0, 1987152.27, 528683.95, 0, 661020.76, 0, 671510.73, 2029318.35, 423365.88, 0, 502514.32, 567685.23, 1372382.14, 318297.98, 0, 1068633.72, 278670.71, 288234.05, 330605.94, 0, 216414.14, 0, 211888.74, 246265.65]
#     rckb_unit_hcost = [1120775.21, 1911879.73, 2112234.91, 1334750.81, 1034690.92, 1987152.27, 414438.21, 0.00, 764997.09, 1433412.29, 1901141.67, 1863890.11, 0.00, 1424401.99, 1413994.59, 1301189.19, 1834568.31, 0.00, 763760.06, 0.00, 252716.80, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
# elif basic_input['project_loc'] == 'NIGBU':
#     rckb_unit_scost = [1120775.21, 1892317.88, 1078414.46, 1078414.46, 0, 1984033.59, 532151.31, 0, 660856.15, 0, 664642.25, 1955126.10, 423365.88, 0, 505816.78, 567685.23, 1592178.06, 318297.98, 0, 1137462.36, 278670.71, 288234.05, 330605.94, 0, 221149.22, 0, 211888.74, 246265.65]
#     rckb_unit_hcost = [1120775.21, 1909133.62, 2112234.91, 1224652.41, 1029200.31, 1984033.59, 414438.21, 0.00, 764997.09, 1433412.29, 1901141.67, 1863890.11, 0.00, 1424401.99, 1413994.59, 1301189.19, 1834568.31, 0.00, 763760.06, 0.00, 252716.80, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
# elif basic_input['project_loc'] == 'MAGBU':
#     rckb_unit_scost = [1120775.21, 1827487.10, 1058281.27, 1058281.27, 0, 1021682.90, 532151.31, 0, 660856.15, 0, 668996.60, 1973405.93, 423365.88, 0, 505816.78, 567685.23, 1411371.64, 318297.98, 0, 1137462.36, 278670.71, 288234.05, 330605.94, 0, 216414.14, 0, 211888.74, 246265.65]
#     rckb_unit_hcost = [1120775.21, 1916182.32, 2112234.91, 1334750.81, 1034690.92, 1021682.90, 414438.21, 0.00, 764997.09, 1433412.29, 1920511.90, 1863890.11, 0.00, 1424401.99, 1413994.59, 1301189.19, 1590109.70, 0.00, 763760.06, 0.00, 252716.80, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

# print np.array(Unit_Rate(basic_input, inventory).Rockbits().ix[:, 'smith_unit_cost']).shape
# print len(rckb_unit_scost)
# print len(rckb_unit_scost)
# print len(rckb_unit_hcost)
# rckb_unit_scost1 = [1120775.21, 1875294.22, 1058281.27, 1058281.27, 0, 1987152.27, 528683.95, 0, 661020.76, 0, 671510.73, 2029318.35, 423365.88, 0, 502514.32, 567685.23, 1372382.14, 318297.98, 0, 1068633.72, 278670.71, 288234.05, 330605.94, 0, 216414.14, 0, 211888.74, 246265.65]
# rckb_unit_hcost1 = [1120775.21, 1911879.73, 2112234.91, 1334750.81, 1034690.92, 1987152.27, 414438.21, 0.00, 764997.09, 1433412.29, 1901141.67, 1863890.11, 0.00, 1424401.99, 1413994.59, 1301189.19, 1834568.31, 0.00, 763760.06, 0.00, 252716.80, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

# print len(rckb_unit_scost1)
# print len(rckb_unit_hcost1)

rckb_qty        = {}.fromkeys(rckb_asmpt.index, False)
for i in np.arange(16, 19):
    rckb_qty[list(rckb_qty.keys())[i]] = True

if basic_input['project_loc'] == 'LGBU':
    wlhd_asmpt              = pd.read_excel(dt_dir + '/wellhead.xlsx')
    wlhd_last_row           = 103558.77 
elif basic_input['project_loc'] == 'BGBU':
    wlhd_asmpt              = pd.read_excel(dt_dir + '/wellhead_BGBU.xlsx')
    wlhd_last_row           =  103934.64     
elif basic_input['project_loc'] == 'NIGBU':
    wlhd_asmpt              = pd.read_excel(dt_dir + '/wellhead_NIGBU.xlsx')
    wlhd_last_row           =  104122.57     
elif basic_input['project_loc'] == 'MAGBU':
    wlhd_asmpt              = pd.read_excel(dt_dir + '/wellhead_MAGBU.xlsx')
    wlhd_last_row           =  103934.64 

mdeg_asmpt              = pd.read_excel(dt_dir + '/mud_engr.xlsx').set_index('Standard Flatspots')
rig_move1_asmpt         = pd.read_excel(dt_dir + '/rig_move.xlsx')
rig_move1_asmpt.ix[0, 2 + np.where(rig_move1_asmpt.ix[:, 2:].columns.values == basic_input['rig'].upper())[0][0]]
rig_move2_asmpt         = pd.read_excel(dt_dir + '/equipment.xlsx')
rig_move2_asmpt         = rig_move2_asmpt.ix[:, 1:].set_index(rig_move2_asmpt.Equipment)
rig_move2_asmpt.ix[rig_move2_asmpt.index.values == '50T CRANE', 4]
ada_cost                = pd.read_excel(dt_dir + '/ada_cost.xlsx')
rigmove_daily           = pd.read_excel(dt_dir + '/rigmovedaily.xlsx')
mud_consumables         = pd.read_excel(dt_dir + '/mud_consumables.xlsx')

if basic_input['project_loc'] == 'LGBU':
    big_hole                = pd.read_excel(dt_dir + '/big_hole.xlsx')
    reg_hole                = pd.read_excel(dt_dir + '/regular_hole.xlsx')
elif basic_input['project_loc'] == 'BGBU':
    big_hole                = pd.read_excel(dt_dir + '/big_hole_BGBU.xlsx')
    reg_hole                = pd.read_excel(dt_dir + '/regular_hole_BGBU.xlsx')
elif basic_input['project_loc'] == 'NIGBU':
    big_hole                = pd.read_excel(dt_dir + '/big_hole_NIGBU.xlsx')
    reg_hole                = pd.read_excel(dt_dir + '/regular_hole_NIGBU.xlsx')
elif basic_input['project_loc'] == 'MAGBU':
    big_hole                = pd.read_excel(dt_dir + '/big_hole_MAGBU.xlsx')
    reg_hole                = pd.read_excel(dt_dir + '/regular_hole_MAGBU.xlsx')

big_hole.ix[ 0, 3] = roundup(Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['surface'] / 11.5) + 3
big_hole.ix[ 2, 3] = roundup(big_hole.ix[0, 3] / 4.) + 1
big_hole.ix[ 7, 3] = roundup(Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['intermediate'] / 11.5) + 3
big_hole.ix[10, 3] = roundup(big_hole.ix[0, 3] / 3.) + 2
big_hole.ix[11, 3] = roundup((big_hole.ix[7, 3] - big_hole.ix[0, 3]) / 3.) + 3.
big_hole.ix[16, 3] = roundup(Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['prodn_casing'] / 11.5) + 3
big_hole.ix[20, 3] = roundup(big_hole.ix[7, 3] / 3.) + 2
big_hole.ix[21, 3] = roundup((big_hole.ix[16, 3] - big_hole.ix[7, 3]) / 3.) + 3.
big_hole.ix[26, 3] = roundup((Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['prodn_liner_1'] - Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['prodn_casing']) / 11.5) + 3
big_hole.ix[33, 3] = roundup((Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['prodn_liner_2'] - Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['prodn_liner_1']) / 11.5) + 3
big_hole.ix[36, 3] = big_hole.ix[26, 3]
big_hole.ix[43, 3] = big_hole.ix[33, 3]

reg_hole.ix[ 0, 3] = roundup(Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['surface'] / 11.5) + 3
reg_hole.ix[ 2, 3] = roundup(reg_hole.ix[0, 3] / 4.) + 1
reg_hole.ix[ 7, 3] = roundup(Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['intermediate'] / 11.5) + 3
reg_hole.ix[10, 3] = roundup(reg_hole.ix[0, 3] / 3.) + 2
reg_hole.ix[11, 3] = roundup((reg_hole.ix[7, 3] - reg_hole.ix[0, 3]) / 3.) + 3.
reg_hole.ix[16, 3] = roundup(Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['prodn_casing'] / 11.5) + 3
reg_hole.ix[20, 3] = roundup(reg_hole.ix[7, 3] / 3.) + 2
reg_hole.ix[21, 3] = roundup((reg_hole.ix[16, 3] - reg_hole.ix[7, 3]) / 3.) + 3.
reg_hole.ix[26, 3] = roundup((Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['prodn_liner_1'] - Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)['prodn_casing']) / 11.5) + 3

transhipment            = pd.read_excel(dt_dir + '/transhipment.xlsx')
handling_hauling        = pd.read_excel(dt_dir + '/handling_hauling.xlsx')
transhipment_drillpipes = pd.read_excel(dt_dir + '/transhipment_drillpipes.xlsx')
depreciation            = pd.read_excel(dt_dir + '/depreciation.xlsx')
insurance               = pd.read_excel(dt_dir + '/insurance.xlsx')
service_fee             = pd.read_excel(dt_dir + '/service_fee.xlsx')
genex                   = pd.read_excel(dt_dir + '/genex.xlsx')
wellname                = pd.read_excel(dt_dir + '/wellname.xlsx')
inter_island            = pd.read_excel(dt_dir + '/inter_island_cost.xlsx')
rigmove_cost            = pd.read_excel(dt_dir + '/rigmove_cost.xlsx')
cement_slb_asmpt2       = pd.read_excel(dt_dir + '/equipmental_rentals.xlsx')
tpwsi_rr_rigs           = pd.read_excel(dt_dir + '/tpwsi_rr_rigs.xlsx')
average_rop_day_rate    = pd.read_excel(dt_dir + '/average_rop_day_rate.xlsx')
rig1_peripherals        = pd.read_excel(dt_dir + '/rig1peripherals.xlsx')
meals_accommodations    = pd.read_excel(dt_dir + '/meals_accommodations.xlsx')
rigmove                 = pd.read_excel(dt_dir + '/rigmove.xlsx')
equipment               = pd.read_excel(dt_dir + '/equipment_rates.xlsx')
chf                     = pd.read_excel(dt_dir + '/chf.xlsx').set_index('Index')
"""
T A B L E S
"""
# COMPUTE THE HEADER
head = header(basic_input, assumptions, drlg_input, flat_input)
# print head
# MATERIALS AND SUPPLIES
fuel                 = Cost_Center(basic_input, assumptions, head).fuel(fuel_asmpt, drlg_input, flat_input, unit_cost = list(np.repeat(30, 7))).sum().sum()
print fuel
lubricants           = Cost_Center(basic_input, assumptions, head).lubricants(fuel_asmpt, drlg_input, flat_input, unit_cost = list(np.repeat(30, 7))).ix[:, 1:].sum().sum()
# print lubricants
hole_depth           = Hole_Casing(basic_input, category = 'hole_depth').compute(assumptions)
mud_chemicals        = Cost_Center(basic_input, assumptions, head).mud_chemicals(mud_consumables, hole_depth, casing_depth_input, unit_cost = [42.25, 187.86, 16.94, 64.91, 1024.80, 397.39, 1295.94, 84.71, 60.76, 754.38, 781.35, 73.68, 85.00, 41.96, 73.68, 66.22, 66.58, 148.75, 38.34, 63.99, 397.39, 85.08, 15.55, 15.11, 110.33, 161.50, 224.68, 13.09, 94.73]).ix[:, 1:].sum().sum()
# mud_chemicals        = Cost_Center(basic_input, assumptions, head).mud_chemicals(mud_consumables, hole_depth, casing_depth_input).ix[:, 1:].to_json(orient="records")
# print mud_chemicals
# print mud_chemicals
# print "Fuel %d" % fuel
# print fuel
# print lubricants
print "Mud Chemicals %f" % mud_chemicals
drlg_input['prodn_liner_2']
if basic_input['rh_or_bh'] == 'Big Hole':
    idx = list(cemt.index)[:len(list(cemt.index)) - 1] + [cement_slb_asmpt2.ix[5, 'Equipment']]
else:
    idx = list(cemt.index)[:len(list(cemt.index)) - 1] + [cement_slb_asmpt2.ix[7, 'Equipment']]

cement_cost = list(cemt.Price)[0:len(list(cemt.Price)) - 1] + list(cement_slb_asmpt2.ix[cement_slb_asmpt2.Equipment == idx[-1], 'Unit Price, USD'])
cement_and_additives = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2, unit_cost = cement_cost).sum().sum()
# cement_and_additives = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2)

# print cement_and_additives
# print cemt
print "Cement and Additives %f" % cement_and_additives

smith                = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rckb_unit_scost).sum().sum()
hughes               = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rckb_unit_hcost, category = 'HUGHES').sum().sum()
rockbits             = smith + hughes

# print rockbits
print smith
# print "RockBits Smith %d" % smith
print "RockBits Hughes %f" % hughes
print "RockBits %f" % rockbits

if basic_input['rig'] == 'Rig 1' or basic_input['rig'] == 'Rig 2':
    cost_ds = np.array([0, 0], dtype = "int")
else:
    cost_ds = np.array([2000 * basic_input['forex_ph_us'], 6000 * basic_input['forex_ph_us']], dtype = "int")

drilling_supplies    = Cost_Center(basic_input, assumptions, head).drilling_supplies(unit_cost = cost_ds).ix[:, 1:].sum().sum()
casings              = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole, unit_cost = True).ix[:, 1:].sum().sum()
# casings              = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole).ix[:, 1:]
# casings              = Cost_Center(basic_input, assumptions, head).casings(big_hole, reg_hole, unit_cost = None).ix[:, 1:]
print "CASINGS %f" % casings
# print "Casings %f" % casings

if basic_input['rh_or_bh'] == 'Big Hole':
    cost = wlhd_asmpt.ix[:, 'Big Hole Unit cost'].values
else:
    cost = wlhd_asmpt.ix[:, 'Regular Hole Unit cost'].values

well_head            = Cost_Center(basic_input, assumptions, head).wellhead(wlhd_asmpt, unit_cost = np.append(cost, wlhd_last_row)).ix[:, 1:].sum().sum()
print "Well Head %f" % well_head
# print well_head

# PURCHASED SERVICES
cementing            = Cost_Center(basic_input, assumptions, head).cementing(unit_cost = [961.17*0.975, 27.55*0.975, 21.35*0.975, 76.21*0.975, 280*0.975, 280*0.975, 316.25*0.975, 77*0.975, 316.25*0.975, 552*0.975, 207*0.975, 207*0.975, 862.5*0.975]).ix[:, 1:].sum().sum()
# cementing            = Cost_Center(basic_input, assumptions, head).cementing().ix[:, 1:]

# cementing            = Cost_Center(basic_input, assumptions, head).cementing().ix[:, 1:]
# print "Cementing %d" % 
print "CEMENTING %f" % cementing
if basic_input['pwd_fliner1']:
    dd_qty = [2, 2, 4, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1]
else:
    dd_qty = [2, 2, 4, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1]

directional_drilling = Cost_Center(basic_input, assumptions, head).directional_drilling(transhipment, unit_cost = [552.50, 552.50, 455.00, 3.25, 130.00, 3.25, 97.50, 3.25, 3.25, 2038.40, 162.50, 0, 0, 219.96, 219.96, 219.96, 232.18, 247.00, 200.20, 130.00, 130.00, 130.00, 260.00, 219.96, 219.96, 24957.00, 24957.00, 60, 60, 850.00, 850.00, 9375.00], qty = dd_qty).sum().sum()
# directional_drilling = Cost_Center(basic_input, assumptions, head).directional_drilling(transhipment, qty = dd_qty)

# directional_drilling = Cost_Center(basic_input, assumptions, head).directional_drilling(transhipment, qty = dd_qty)
print directional_drilling
# directional_drilling = Cost_Center(basic_input, assumptions, head).directional_drilling(transhipment)
# print "directional drilling %f" % directional_drilling
# print "DIRECTIONAL DRILLING %f" %directional_drilling
# directional_drilling = Cost_Center(basic_input, assumptions, head).directional_drilling(transhipment)

# print np.arange(directional_drilling.shape)
# print directional_drilling
mud_engineering      = Cost_Center(basic_input, assumptions, head).mud_engineering(unit_cost =  472.50).ix[:, 1:].sum().sum()
print "MUD ENGINEERING %f" % mud_engineering
aerated_drilling     = Cost_Center(basic_input, assumptions, head).aerated_drilling(ada_cost, drlg_input, flat_input, unit_cost = [ 3203.50, 2214.50, 67000.00, 67000.00, 1097.50, 351.25, 2900.00, np.nan, 879.78, 1173.04, 244.24, 391.30, 236.50, 258.00, np.nan, 1450.00, 1050.00, 950.00, 950.00, 7500.00, 800.00]).ix[:, 1:].sum().sum()
print aerated_drilling
# print "a %f" % aerated_drilling

# aerated_drilling     = Cost_Center(basic_input, assumptions, head).aerated_drilling(ada_cost, drlg_input, flat_input).ix[:, 1:]

print "AERATED DRILLING %f " % aerated_drilling
jars_shock_tools     = Cost_Center(basic_input, assumptions, head).jars_shock(transhipment, drlg_input, unit_cost = [145.00, 135.00, 135.00, 135.00, 65.00, 3100.00]).ix[:, 1:].sum().sum()
jars_shock_tools1     = Cost_Center(basic_input, assumptions, head).jars_shock(transhipment, drlg_input, unit_cost = [145.00, 135.00, 135.00, 135.00, 65.00, 3100.00]).ix[:, 1:]
jars_shock_tools2    = Cost_Center(basic_input, assumptions, head).jars_shock(transhipment, drlg_input).ix[:, 1:]
# jars_shock_tools     = Cost_Center(basic_input, assumptions, head).jars_shock(transhipment, drlg_input).ix[:, 1:]

# jars_shock_tools     = Cost_Center(basic_input, assumptions, head).jars_shock(transhipment, drlg_input).ix[:, 1:]

# print "jar %f" % jars_shock_tools
print jars_shock_tools1
print jars_shock_tools2


idx = basic_input['project_loc'] == transhipment.ix[:, 'LOCATION']
# transhipment.ix[idx, 'FROM'] 
a_chf = chf.columns[2:] == basic_input['project_loc'] 
b_chf = chf.columns[2:] == basic_input['project_loc'] + '.1'
col_chf1 = a_chf + b_chf
col_chf2 = np.array(chf.ix['CHF', 2:] == basic_input['chf'])

if basic_input['rh_or_bh'] == 'Regular Hole':
    cost1_chf = np.array(chf.ix['13-5/8" CHF X 13-3/8" Casing', 2:])[col_chf1 * col_chf2][0]
else:
    cost1_chf = np.array(chf.ix['20-3/4" CHF X 18-5/8" Casing', 2:])[col_chf1 * col_chf2][0]

cost2_chf = np.array(chf.ix['Mob/Demob of Equipment', 2:])[col_chf1 * col_chf2][0]
cost3_chf = np.array(chf.ix['Mob/Demob of Personnel', 2:])[col_chf1 * col_chf2][0]
cost4_chf = np.array(chf.ix['Service Vehicle (Day Rate)', 2:])[col_chf1 * col_chf2][0]
cost5_chf = np.array(chf.ix['Standby Equipment', 2:])[col_chf1 * col_chf2][0]
cost6_chf = np.array(chf.ix['Standby Personnel', 2:])[col_chf1 * col_chf2][0]
cost7_chf = np.array(chf.ix['Standby Boom Truck', 2:])[col_chf1 * col_chf2][0]
cost8_chf = np.array(chf.ix['Standby Personnel and Equipment', 2:])[col_chf1 * col_chf2][0]

chf_cost = [cost1_chf, cost2_chf, cost3_chf, cost4_chf, cost5_chf, cost6_chf, cost7_chf, cost8_chf,  50000.00]
chf_welding          = Cost_Center(basic_input, assumptions, head).chf_installation(unit_cost = chf_cost).ix[:, 1:].sum().sum()
# print chf_welding
mud_logging          = Cost_Center(basic_input, assumptions, head).mud_logging(drlg_input, flat_input, unit_cost = [931.20, 820.80]).ix[:, 1:].sum().sum()
# print mud_logging
casing_running       = Cost_Center(basic_input, assumptions, head).casing_running(unit_cost =  69300 / 31.).sum().sum()
# casing_running       = Cost_Center(basic_input, assumptions, head).casing_running(mdeg_asmpt, drlg_input, flat_input).sum()

print "CASING RUNNING %f" % casing_running
# cost of drilling rig
idx_cd = basic_input['rig'] == tpwsi_rr_rigs.ix[:, 'Rig']
col_cd = basic_input['project_loc'] == tpwsi_rr_rigs.columns
cost1 = np.array(tpwsi_rr_rigs.ix[idx_cd, col_cd]).flatten()[0]

idx_ma_m = 'Meals' == meals_accommodations.ix[:, 'Type']
idx_ma_a = 'Accommodation' == meals_accommodations.ix[:, 'Type']
col_ma = basic_input['project_loc'] == meals_accommodations.columns

if np.sum(idx_ma_m) > 0 and np.sum(idx_ma_a) > 0 and np.sum(col_ma):
    meal_daily_rate = meals_accommodations.ix[idx_ma_m, col_ma]
    accm_daily_rate = meals_accommodations.ix[idx_ma_a, col_ma]
else:
    meal_daily_rate = 0
    accm_daily_rate = 0

rig1pe_summary = pd.DataFrame(index = ['3RD PARTY', 'CHF', 'CEMENT CUTTERS', 'OTHERS (BOOMTRUCK DRIVER & SV DRIVER)'], columns = ['DURATION', 'MEALS', 'ACCOM', 'TOTAL COST'])
rig1pe_summary.ix[0, 'DURATION'] = basic_input['total_days']
rig1pe_summary.ix[1, 'DURATION'] = 10.
if basic_input['double_liner']:
    rig1pe_summary.ix[2, 'DURATION'] = 5 * 4
else:
    rig1pe_summary.ix[2, 'DURATION'] = 4 * 4

rig1pe_summary.ix[3, 'DURATION'] = basic_input['total_days']

rig1pe_summary.ix[0, 'MEALS'] = rig1_peripherals.ix[0:5, 'MEAL'].sum()
rig1pe_summary.ix[1, 'MEALS'] = rig1_peripherals.ix[6:7, 'MEAL'].sum()
rig1pe_summary.ix[2, 'MEALS'] = rig1_peripherals.ix[8, 'MEAL']
rig1pe_summary.ix[3, 'MEALS'] = rig1_peripherals.ix[10, 'MEAL']

rig1pe_summary.ix[0, 'ACCOM'] = rig1_peripherals.ix[0:5, 'ACCOMMODATION'].sum()
rig1pe_summary.ix[1, 'ACCOM'] = rig1_peripherals.ix[6:7, 'ACCOMMODATION'].sum()
rig1pe_summary.ix[2, 'ACCOM'] = rig1_peripherals.ix[8, 'ACCOMMODATION']
rig1pe_summary.ix[3, 'ACCOM'] = rig1_peripherals.ix[10, 'ACCOMMODATION']

for i in np.arange(4):
    rig1pe_summary.ix[i, 'TOTAL COST'] = rig1pe_summary.ix[i, 'DURATION'] * (rig1pe_summary.ix[i, 'MEALS'] * np.array(meal_daily_rate).flatten()[0] + rig1pe_summary.ix[i, 'ACCOM'] * np.array(accm_daily_rate).flatten()[0])

if basic_input['rig'] == 'Rig 1' or basic_input['rig'] == 'Rig 2':
    cost2 = assumptions[5]['Base Day Rate']
    cost3 = cost4 = average_rop_day_rate.ix[45 - 30, '0 LTI']
    cost5 = assumptions[5]['Additional Payment'] / 365.
    cost6 = assumptions[5]['Well Bonus']
    cost7 = average_rop_day_rate.ix[basic_input['target_rop'] - 30, 1]
    cost9 = rig1pe_summary.ix[:, 'TOTAL COST'].sum() / basic_input['total_days']
    cost10 =  3403000.00 
else:
    cost2 = cost3 = cost4 = cost5 = cost6 = cost7 = cost9 = cost10 = 0
cost8 = 0

drilling_rig_cost = [cost1, cost2, cost3, cost4, cost5, cost6, cost7, cost8, cost9, cost10]
drilling_rig         = Cost_Center(basic_input, assumptions, head).drilling_rig_services(drlg_input, flat_input, unit_cost = drilling_rig_cost).ix[:, 2:].sum().sum()
# np.nansum(basic_input['drilling_row_total'].values() + [-3])
# drilling_rig.ix[:, 'RATE']

print drilling_rig
# print Cost_Center(basic_input, assumptions, head).head
qty = np.zeros(4)
if basic_input['rent_drill_pipes']:
    qty[0:2] = basic_input['no_of_Joints']
    qty[2:] = 50
print "QTY######"
print qty
drill_pipes          = Cost_Center(basic_input, assumptions, head).drill_pipes(drlg_input, flat_input, qty = qty, unit_cost = [1.50, 47.02, 3250*0.05, 3250*0.02]).ix[:, 1:]
drill_pipes          = Cost_Center(basic_input, assumptions, head).drill_pipes(drlg_input, flat_input, qty = qty).ix[:, 1:]
print drill_pipes
completion_test      = Cost_Center(basic_input, assumptions, head).completion_test(unit_cost = [2500000, 1100000]).ix[:, 1:].sum().sum()
# print completion_test
cement_out           = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2)

if basic_input['project_loc'] == 'LGBU':
    other_cementing_cost = 13
elif basic_input['project_loc'] == 'BGBU':
    other_cementing_cost = 16
elif basic_input['project_loc'] == 'NIGBU':
    other_cementing_cost = 15
elif basic_input['project_loc'] == 'MAGBU':
    other_cementing_cost = 10

other_cementing      = Cost_Center(basic_input, assumptions, head).other_cementing_services(cement_out, unit_cost = other_cementing_cost).ix[:1, 1:].sum().sum()
print "other cementing %f" % other_cementing
# print other_cementing
trans_table          = Cost_Center(basic_input, assumptions, head).transhipment_cost(handling_hauling, transhipment_drillpipes)
# print trans_table
handling_towing      = Cost_Center(basic_input, assumptions, head).handling(drlg_input, flat_input, asmpt1 = trans_table.ix[:, 'TOTAL'].sum()).sum().sum()
print handling_towing

drilling_rig_table   = Cost_Center(basic_input, assumptions, head).drilling_rig_services(drlg_input, flat_input, unit_cost = drilling_rig_cost).ix[:, 1:].sum()

rig_mobilization_index = ['40 FT HI-BED TRAILER', '40 FT SEMI-LOW BED TRAILER (35T)', '35 FT LOW BED TRAILER (60T)', '50T CRANE', '70T CRANE', '180T CRANE', 'PAYLOADER', 'FORKLOADER', 'TOWING EQUIPMENT', 'BOOM TRUCK', '5TUT PUMP', 'INTERISLAND RIGMOVE (ALLOCATED)']
idx1_rm = basic_input['project_loc'] == handling_hauling.index
idx2_rm = rig_mobilization_index[1] == rigmove.ix[:, 'ITEM']
idx3_rm = rig_mobilization_index[2] == rigmove.ix[:, 'ITEM']
idx4_rm = rig_mobilization_index[3] == equipment.ix[:, 'Equipment Rental']
idx5_rm = rig_mobilization_index[4] == equipment.ix[:, 'Equipment Rental']
idx6_rm = rig_mobilization_index[5] == equipment.ix[:, 'Equipment Rental']
idx7_rm = rig_mobilization_index[6] == rigmove.ix[:, 'ITEM']
idx8_rm = rig_mobilization_index[7] == rigmove.ix[:, 'ITEM']
idx9_rm = rig_mobilization_index[8] == rigmove.ix[:, 'ITEM']
idx10_rm = rig_mobilization_index[9] == rigmove.ix[:, 'ITEM']
idx11_rm = rig_mobilization_index[10] == equipment.ix[:, 'Equipment Rental']

cost1_rm = np.array(handling_hauling.ix[idx1_rm, '40ft HBT']).flatten()[0]
cost2_rm = np.array(rigmove.ix[idx2_rm, 'UNIT COST']).flatten()[0]
cost3_rm = np.array(rigmove.ix[idx3_rm, 'UNIT COST']).flatten()[0]
cost4_rm = np.array(equipment.ix[idx4_rm, 'UNIT RATES']).flatten()[0]
cost5_rm = np.array(equipment.ix[idx5_rm, 'UNIT RATES']).flatten()[0]
cost6_rm = np.array(equipment.ix[idx6_rm, 'UNIT RATES']).flatten()[0]
cost7_rm = np.array(rigmove.ix[idx7_rm, 'UNIT COST']).flatten()[0]
cost8_rm = np.array(rigmove.ix[idx8_rm, 'UNIT COST']).flatten()[0]
cost9_rm = np.array(rigmove.ix[idx9_rm, 'UNIT COST']).flatten()[0]
cost10_rm = np.array(rigmove.ix[idx10_rm, 'UNIT COST']).flatten()[0]
cost11_rm = np.array(equipment.ix[idx11_rm, 'UNIT RATES']).flatten()[0]

rm_cost = [cost1_rm, cost2_rm, cost3_rm, cost4_rm, cost5_rm, cost6_rm, cost7_rm, cost8_rm, cost9_rm, cost10_rm, cost11_rm, 0]
# rig_mobilization     = np.array(Cost_Center(basic_input, assumptions, head).rig_mobilization(asmpt1 = rig_move1_asmpt, asmpt2 = rig_move2_asmpt, asmpt3 = rigmove_cost, asmpt4 = drilling_rig_table.rigmove, unit_cost = rm_cost, total = True))[0]
rig_mobilization     = Cost_Center(basic_input, assumptions, head).rig_mobilization(asmpt1 = rig_move1_asmpt, asmpt2 = rig_move2_asmpt, asmpt3 = rigmove_cost, asmpt4 = drilling_rig_table.rigmove, unit_cost = rm_cost, total = True)


# print rig_mobilization

# # for i in 
# idx_er = equipment_rental.index[6] == equipment.ix[:, 'Equipment Rental']
# col_er = "HR " + basic_input['project_loc'] == equipment.columns
# noh1 = np.array(equipment.ix[idx_er, col_er]).flatten()[0]

# if basic_input['rig'] == 'Rig 1' or basic_input['rig'] == 'Rig 2':
#     weight_er = 0
# else:
#     weight_er = 1

# noh1 * weight_er

# rig_move1_asmpt.ITEM.values
# equipment_rental.index.values[1]
if basic_input['project_loc'] == 'LGBU':
    er_qty = [1, 1, 0, 0, 2, 2, 1]
elif basic_input['project_loc'] == 'BGBU':
    er_qty = [0, 0, 0, 0, 0, 1, 1]
elif basic_input['project_loc'] == 'NIGBU':
    er_qty = [1, 1, 0, 0, 2, 2, 1]
elif basic_input['project_loc'] == 'MAGBU':
    er_qty = [1, 1, 0, 0, 2, 2, 1]

equipment_rental     = Cost_Center(basic_input, assumptions, head).equipment_rental(rig_move2_asmpt, equipment, drlg_input, flat_input, unit_cost =  [cost4_rm, cost5_rm, cost6_rm, 0, cost11_rm, cost8_rm, 0], qty = er_qty).ix[:, 1:].sum().sum()
# equipment_rental     = Cost_Center(basic_input, assumptions, head).equipment_rental(rig_move2_asmpt, equipment, drlg_input, flat_input).ix[:, 0:]

print equipment_rental
# print [cost4_rm, cost5_rm, cost6_rm, 0, cost11_rm, cost8_rm, 0]
rig_allocated        = Cost_Center(basic_input, assumptions, head).rig_allocated(rigmove_daily, depreciation, insurance, genex, service_fee, wellname, inter_island, drlg_input, flat_input).ix[:, 1:].sum().sum()
# print rig_allocated
cover_sheet_index = [
        '5202000 - Fuels',                            
        '5203000 - Lubricants (Oil, Grease, etc.)',
        '5213000 - Mud and Chemicals',  
        '5214000 - Cement and Additives',             
        '5215000 - Rockbits',            
        '5216000 - Drilling Supplies',                
        '5221000 - Casings',               
        '5253000 - Wellhead',                         
        '5467000 - Cementing Services',               
        '5466000 - Directional Drilling Services',
        '5468000 - Mud Engineering Services',   
        '5470000 - Aerated Drilling Services',        
        '5469000 - Jars and Shock Tools',       
        '5425000 - CHF Welding Services',            
        '5472000 - Mud Logging Services',            
        '5471000 - Casing Running Services',          
        '5463000 - Drilling Rig Services',         
        '5503000 - Drill Pipes',           
        '5465000 - Completion Test -Wireline',
        '5465000 - Other Cementing Services',       
        '5411000 - Handling, Hauling, Towing & Del.',
        '5431000 - Rig Mobilization Charges',
        '5503000 - Equipment Rental',        
        'Rig Allocated Charges',
        'Total'  
]

values = [
    fuel, lubricants, mud_chemicals, cement_and_additives, rockbits, drilling_supplies, casings, 
    well_head, cementing, directional_drilling, mud_engineering, aerated_drilling, jars_shock_tools, chf_welding, mud_logging, casing_running, drilling_rig, drill_pipes, completion_test, 
    other_cementing, handling_towing, rig_mobilization, equipment_rental, rig_allocated
    ]

values = values + [np.sum(values)]
cover_df = pd.DataFrame(values, index = cover_sheet_index)

pd.DataFrame(values, index = cover_sheet_index).to_csv('/Users/al-ahmadgaidasaad/Documents/WORK/NEURAL-MECHANICS/EDC/cover_sheet.csv')

###############
# asmpt1 = rig_move2_asmpt
# asmpt2 = equipment
# unit_cost =  [cost4_rm, cost5_rm, cost6_rm, 0, cost11_rm, cost8_rm, 0]

# cement_and_additives = Cost_Center(basic_input, assumptions, head).cement_additives(cemt, cement_slb_asmpt2, unit_cost = cement_cost).sum().sum()
# asmpt = assumptions
# asmpt1 = cemt
# asmpt2 = cement_slb_asmpt2
# keys = [
#     'surface',
#     'intermediate',
#     'prodn_casing',
#     'prodn_liner_1',
#     'prodn_liner_2',
#     'prodn_liner_3'
#     ]

# if basic_input['double_liner']:
#     head_columns = ['rigmove'] + [i + '_' + j for j in keys[:5] for i in ['d', 'f']]
# else:
#     head_columns = ['rigmove'] + [i + '_' + j for j in keys[:4] for i in ['d', 'f']]

# smith                = Cost_Center(basic_input, assumptions, head).rockbits(rckb_asmpt, rckb_qty, rckb_unit_scost).sum().sum()
# category = 'SMITH'
# asmpt = rckb_asmpt
# qty = rckb_qty#, rckb_unit_scost
# idx = asmpt.index
# rockbits_columns = head_columns + ['d_prodn_liner_2']

# table = pd.DataFrame(0, index = idx, columns = rockbits_columns)

# for i in rockbits_columns:
#     i = rockbits_columns[5]
#     if i[0] == 'd':
#         if i == 'd_surface':
#             if basic_input['rh_or_bh'] == 'Big Hole':
#                 table.loc['32"  TCI Cutters (3 pcs)', i] = asmpt.loc['32"  TCI Cutters (3 pcs)', 'PROG' + ' ' + category]

#             table.loc['26" x Tricone IADC Code 515', i] = asmpt.loc['26" x Tricone IADC Code 515', 'PROG' + ' ' + category]

#         elif i == 'd_intermediate':
#             if basic_input['rh_or_bh'] == 'Big Hole':
#                 table.loc['23" x Tricone IADC Code 515', i] = asmpt.loc['23" x Tricone IADC Code 515', 'PROG' + ' ' + category]
#             else:
#                 table.loc['17 " x Tricone IADC Code 525', i] = asmpt.loc['17 " x Tricone IADC Code 525', 'PROG' + ' ' + category]
#                 table.loc['17 " x Tricone IADC Code 615', i] = asmpt.loc['17 " x Tricone IADC Code 615', 'PROG' + ' ' + category]

#                 if category == 'HUGHES':
#                     table.loc['23" x Tricone IADC Code 515', i] = asmpt.loc['23" x Tricone IADC Code 515', 'PROG' + ' ' + category]

#         elif i == 'd_prodn_casing':
#             if basic_input['rh_or_bh'] == 'Big Hole':
#                 table.loc['17 " x Tricone IADC Code 525', i] = asmpt.loc['17 " x Tricone IADC Code 525', 'PROG' + ' ' + category]
#                 table.loc['17 " x Tricone IADC Code 615', i] = asmpt.loc['17 " x Tricone IADC Code 615', 'PROG' + ' ' + category]
#             else:
#                 table.loc['12.25 " x PDC PDC BIT', i] = asmpt.loc['12.25 " x PDC PDC BIT', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 217', i] = asmpt.loc['12.25 " x Tricone IADC 217', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 517', i] = asmpt.loc['12.25 " x Tricone IADC 517', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 537', i] = asmpt.loc['12.25 " x Tricone IADC 537', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 547', i] = asmpt.loc['12.25 " x Tricone IADC 547', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 637', i] = asmpt.loc['12.25 " x Tricone IADC 637', 'PROG' + ' ' + category]   
            
#             if category == 'HUGHES':
#                     table.loc['17 " x Tricone IADC Code 525', i] = asmpt.loc['17 " x Tricone IADC Code 525', 'PROG' + ' ' + category]

#         elif i == 'd_prodn_liner_1':
#             if basic_input['rh_or_bh'] == 'Big Hole':
#                 table.loc['12.25 " x PDC PDC BIT', i] = asmpt.loc['12.25 " x PDC PDC BIT', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 217', i] = asmpt.loc['12.25 " x Tricone IADC 217', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 517', i] = asmpt.loc['12.25 " x Tricone IADC 517', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 537', i] = asmpt.loc['12.25 " x Tricone IADC 537', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 547', i] = asmpt.loc['12.25 " x Tricone IADC 547', 'PROG' + ' ' + category]
#                 table.loc['12.25 " x Tricone IADC 637', i] = asmpt.loc['12.25 " x Tricone IADC 637', 'PROG' + ' ' + category]
#             else:
#                 table.loc['8.5 " x PDC PDC BIT', i] = asmpt.loc['8.5 " x PDC PDC BIT', 'PROG' + ' ' + category]
#                 table.loc['8.5 " x Tricone IADC 117 / 217', i] = asmpt.loc['8.5 " x Tricone IADC 117 / 217', 'PROG' + ' ' + category]
#                 table.loc['8.5 " x Tricone IADC 637', i] = asmpt.loc['8.5 " x Tricone IADC 637', 'PROG' + ' ' + category]

#         elif i == 'd_prodn_liner_2':
#             if basic_input['rh_or_bh'] == 'Big Hole':
#                 table.loc['9-7/8 " x PDC PDC Bit', i] = asmpt.loc['9-7/8 " x PDC PDC Bit', 'PROG' + ' ' + category]
#                 table.loc['9-7/8 " x Tricone IADC 117/217', i] = asmpt.loc['9-7/8 " x Tricone IADC 117/217', 'PROG' + ' ' + category]
#                 table.loc['9-7/8 " x Tricone IADC 517', i] = asmpt.loc['9-7/8 " x Tricone IADC 517', 'PROG' + ' ' + category]
#                 table.loc['9-7/8 " x Tricone IADC 537', i] = asmpt.loc['9-7/8 " x Tricone IADC 537', 'PROG' + ' ' + category]
#                 table.loc['9-7/8 " x Tricone IADC 637', i] = asmpt.loc['9-7/8 " x Tricone IADC 637', 'PROG' + ' ' + category]

#             if qty['8.5 " x PDC PDC BIT']:
#                 table.loc['8.5 " x PDC PDC BIT', i] = asmpt.loc['8.5 " x PDC PDC BIT', 'PROG' + ' ' + category]
#             if qty['8.5 " x Tricone IADC 117 / 217']:
#                 table.loc['8.5 " x Tricone IADC 117 / 217', i] = asmpt.loc['8.5 " x Tricone IADC 117 / 217', 'PROG' + ' ' + category]
#             if qty['8.5 " x Tricone IADC 637']:
#                 table.loc['8.5 " x Tricone IADC 637', i] = asmpt.loc['8.5 " x Tricone IADC 637', 'PROG' + ' ' + category]

#     if unit_cost is not None:
#         table.ix[:, i] *= unit_cost

# return table