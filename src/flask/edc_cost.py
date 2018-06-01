# from edc_assumptions import Assumptions
# import numpy as np
# import pandas as pd

class Unit_Rate(object):

    def __init__(self, basic_input, asmpt, inventory):
        """
        Class for Computing Unit Rate of Materials

        # Arguments:
            basic_input: dict, items of basic inputs
            asmpt: list, list of basic assumptions
            inventory: excel file, spreadsheet containing the inventory of materials
        """

        self.basic_input = basic_input
        self.asmpt = asmpt
        self.inventory = inventory

        self.rockbits_index = ['32" 	TCI Cutters (3 pcs)', '26" x Tricone	IADC Code 515', '23" x Tricone	IADC Code 515', '17 " x Tricone	IADC Code 525', '17 " x Tricone	IADC Code 615', '12.25 " x PDC	PDC BIT', '12.25 " x Tricone	IADC 217', 
            '12.25 " x Tricone	IADC 517', '12.25 " x Tricone	IADC 537', '12.25 " x Tricone	IADC 547', '12.25 " x Tricone	IADC 637', '9-7/8 " x PDC	PDC Bit', '9-7/8 " x Tricone	IADC 117/217', '9-7/8 " x Tricone	IADC 517', '9-7/8 " x Tricone	IADC 537', 
            '9-7/8 " x Tricone	IADC 637', '8.5 " x PDC	PDC BIT', '8.5 " x Tricone	IADC 117 / 217', '8.5 " x Tricone	IADC 637', '7-7/8 " x PDC	PDC Bit', '7-7/8 " x Tricone	IADC 217', '7-7/8 " x Tricone	IADC 517', '7-7/8 " x Tricone	IADC 537',
            '7-7/8 " x Tricone	IADC 637', '6-1/8" x Tricone	IADC Code 200/300', '6-1/8" x Tricone	IADC Code 500/600', '6" x Tricone	IADC Code 200/300', '6" x Tricone	IADC Code 500/600']
        self.rockbits_reg_hole = ['', 'SURFACE', '', 'INTERMEDIATE', 'INTERMEDIATE', 'PRODUCTION', 'PRODUCTION', 'PRODUCTION', 'PRODUCTION', 'PRODUCTION', 'PRODUCTION', '', '', '', '', '', 'LINER1', 'LINER1', 'LINER1', '', '', '', '', '', '', '', '', '']
        self.rockbits_big_hole = ['SURFACE', 'SURFACE', 'INTERMEDIATE', 'PRODUCTION', 'PRODUCTION', 'LINER1', 'LINER1', 'LINER1', 'LINER1', 'LINER1', 'LINER1', 'LINER2', 'LINER2', 'LINER2', 'LINER2', 'LINER2', '', '', '', 'LINER3', 'LINER3', 'LINER3', 'LINER3', 'LINER3', '', '', '', '']
        self.rockbits_smith_code = ['10723', '40327', '13945', '13945', '115424', '13944', '8887', '13950', '13951', '', '13952', '52582', '108569', '', '40328', '8909', '13957', '8913', '13960', '52541', '85217', '8915', '109766', '8910', '8911', '112532', '14052', '13942']
        self.rockbits_hughes_code = ['10723', '115060', '14049', '8889', '85216', '13944', '108568', '13970', '13940', '115423', '13949', '52543', '115429', '109768', '52542', '13967', '13973', '8912', '13956', '115427', '115426', '109257', '13968', '13969', '', '', '', '']
        self.rockbits_columns = ['reg_hole', 'big_hole', 'smith_material_code', 'hughes_material_code', 'smith_SAMDI', 'smith_BGBU', 'smith_LGBU', 'smith_NIGBU', 'smith_MAGBU', 'hughes_SAMDI', 'hughes_BGBU', 'hughes_LGBU', 'hughes_NIGBU', 'hughes_MAGBU', 'smith_average', 'smith_qty', 'smith_unit_cost', 'hughes_average', 'hughes_qty', 'hughes_unit_cost']

        self.wellhead_big_index = ['20-3/4" x 3M (900S) CASING HEAD FLANGE', '20-3/4" x 3M x 13-5/8" x 3M EXPANSION SPOOL', '12" x 900S MASTER VALVE', '3-1/8" x 3m WING VALVES']
        self.wellhead_big_code = ['11482', '14640', '15704', '116389']
        self.wellhead_reg_index = ['13-5/8" x 3M (900S) CASING HEAD FLANGE)', '13-5/8" x 3M x 11" x 3M EXPANSION SPOOL', '10" x 900S MASTER VALVE', '3-1/8" x 3M WING VALVES']
        self.wellhead_reg_code = ['11644', '14639', '15733', '116389']

    def fuel(self):
        """
        Interface for Fuel Cost
        """

        return list(np.repeat(30, 7))

    def lubricants(self):
        """
        Interface for Lubricants Cost
        """

        return list(np.repeat(30, 7))

    def mud_chemicals(self):
        """
        Interface for Mud and Chemicals Cost
        """

        return [42.25, 187.86, 16.94, 64.91, 1024.80, 397.39, 1295.94, 84.71, 60.76, 754.38, 781.35, 73.68, 85.00, 41.96, 73.68, 66.22, 66.58, 148.75, 38.34, 63.99, 397.39, 85.08, 15.55, 15.11, 110.33, 161.50, 224.68, 13.09, 94.73]

    def cement_additives(self, path):
        """
        Interface for Cement and Additives Cost

        # Arguments:
            path: string, path of the equipmental_rentals.xlsx
        """
        cement = Assumptions(self.basic_input, self.asmpt).cement_additives()
        cement_2 = pd.read_excel(path)

        if self.basic_input['rh_or_bh'] == 'Big Hole':
            idx = list(cement.index)[:len(list(cement.index)) - 1] + [cement_2.ix[5, 'Equipment']]
        else:
            idx = list(cement.index)[:len(list(cement.index)) - 1] + [cement_2.ix[7, 'Equipment']]

        cost = list(cement.Price)[0:len(list(cement.Price)) - 1] + list(cement_2.ix[cement_2.Equipment == idx[-1], 'Unit Price, USD'])

        return cost

    def rockbits(self):
        """
        Interface for Rockbits Cost
        """
        table = pd.DataFrame(0, index = self.rockbits_index, columns =  self.rockbits_columns)
        
        for i in self.rockbits_columns:
            if i == 'reg_hole':
                table.ix[:, i] = self.rockbits_reg_hole
            elif i == 'big_hole':
                table.ix[:, i] = self.rockbits_big_hole
            elif i == 'smith_material_code':
                table.ix[:, i] = self.rockbits_smith_code
            elif i == 'hughes_material_code':
                table.ix[:, i] = self.rockbits_hughes_code
            else:  
                for j in np.arange(table.shape[0]):
                    if i[:5] == 'smith':
                        idx = str(table.ix[j, 'smith_material_code']) == np.array(self.inventory.ix[:, 'Material No.']).astype(str)
                        if i[6].isupper():
                            col = i[6:] + '_' + 'UNIT PRICE' == np.array(self.inventory.columns).astype(str)
                            table.ix[j, i] = 0 if np.sum(idx) == 0 or np.sum(col) == 0 else np.array(self.inventory.ix[idx, col])[0]
                        elif i[6].islower():
                            if i == 'smith_average':
                                dat = np.array([table.ix[j, col] for col in self.rockbits_columns[4:9]])
                                table.ix[j, i] = np.sum(dat) / float(dat[dat != 0].shape[0])
                            elif i == 'smith_qty':
                                table.ix[j, i] = 0 if np.sum(idx) == 0 else np.array(self.inventory.ix[idx, 'QTY'])[0]
                            elif i == 'smith_unit_cost':
                                col = self.basic_input['project_loc'] + '_' + 'UNIT PRICE' == np.array(self.inventory.columns).astype(str)
                                table.ix[j, i] = 0 if np.sum(idx) == 0 or np.sum(col) == 0 else table.ix[j, 'smith_average'] if np.array(self.inventory.ix[idx, col])[0] == 0 else np.array(self.inventory.ix[idx, col])[0]
                                # print np.sum(idx) == 0
                    elif i[:6] == 'hughes':
                        idx = str(table.ix[j, 'hughes_material_code']) == np.array(self.inventory.ix[:, 'Material No.']).astype(str)                        
                        if i[7].isupper():
                            col = i[7:] + '_' + 'UNIT PRICE' == np.array(self.inventory.columns).astype(str)
                            table.ix[j, i] = 0 if np.sum(idx) == 0 or np.sum(col) == 0 else np.array(self.inventory.ix[idx, col])[0]
                        elif i[7].islower():
                            if i == 'hughes_average':
                                dat = np.array([table.ix[j, col] for col in self.rockbits_columns[9:14]])
                                table.ix[j, i] = np.sum(dat) / float(dat[dat != 0].shape[0])
                            elif i == 'hughes_qty':
                                table.ix[j, i] = 0 if np.sum(idx) == 0 else np.array(self.inventory.ix[idx, 'QTY'])[0]
                            elif i == 'hughes_unit_cost':
                                col = self.basic_input['project_loc'] + '_' + 'UNIT PRICE' == np.array(self.inventory.columns).astype(str)
                                table.ix[j, i] = 0 if np.sum(idx) == 0 or np.sum(col) == 0 else table.ix[j, 'hughes_average'] if np.array(self.inventory.ix[idx, col])[0] == 0 else np.array(self.inventory.ix[idx, col])[0]
                                # print self.basic_input['project_loc'] + '_' + 'UNIT PRICE'
                                # print np.array(self.inventory.columns).astype(str)
        return table
    
    def drilling_supplies(self):
        """
        Interface of Drilling Supplies Cost
        """
        if self.basic_input['rig'] == 'Rig 1' or self.basic_input['rig'] == 'Rig 2':
            cost = np.array([0, 0], dtype = "int")
        else:
            cost = np.array([2000 * self.basic_input['forex_ph_us'], 6000 * self.basic_input['forex_ph_us']], dtype = "int")

        return cost

    def casings(self):
        """
        Interface for Casings Cost
        """        
        if basic_input['rh_or_bh'] == 'Big Hole':
            cost = wlhd_asmpt.ix[:, 'Big Hole Unit cost'].values
        else:
            cost = wlhd_asmpt.ix[:, 'Regular Hole Unit cost'].values

        if basic_input['project_loc'] == 'LGBU':
            wlhd_last_row           = 103558.77 
        elif basic_input['project_loc'] == 'BGBU':
            wlhd_last_row           =  103934.64     
        elif basic_input['project_loc'] == 'NIGBU':
            wlhd_last_row           =  104122.57     
        elif basic_input['project_loc'] == 'MAGBU':
            wlhd_last_row           =  103934.64 

        return np.append(cost, wlhd_last_row)
    
    def cementing(self):
        """
        Interface for Cementing Cost
        """

        return [961.17*0.975, 27.55*0.975, 21.35*0.975, 76.21*0.975, 280*0.975, 280*0.975, 316.25*0.975, 77*0.975, 316.25*0.975, 552*0.975, 207*0.975, 207*0.975, 862.5*0.975]

    def directional_drilling(self):
        """
        Interface for Directional Drilling Cost
        """

        return [552.50, 552.50, 455.00, 3.25, 130.00, 3.25, 97.50, 3.25, 3.25, 2038.40, 162.50, 0, 0, 219.96, 219.96, 219.96, 232.18, 247.00, 200.20, 130.00, 130.00, 130.00, 260.00, 219.96, 219.96, 24957.00, 24957.00, 60, 60, 850.00, 850.00, 9375.00]

    def mud_engineering(self):
        """
        Interface for Mud Engineering Cost
        """

        return 472.50

    def aerated_drilling(self):
        """
        Interface for Aerated Drilling Cost
        """

        return [ 3203.50, 2214.50, 67000.00, 67000.00, 1097.50, 351.25, 2900.00, np.nan, 879.78, 1173.04, 244.24, 391.30, 236.50, 258.00, np.nan, 1450.00, 1050.00, 950.00, 950.00, 7500.00, 800.00]

    def jars_shock(self):
        """
        Interface for Jars and Shock Cost
        """

        return [145.00, 135.00, 135.00, 135.00, 65.00, 3100.00]

    def chf(self, path):
        """
        Interface for CHF Cost

        # Arguments:
            path: string, path of the chf.xlsx
        """
        chf = pd.read_excel(path)

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

    def mud_logging(self):
        """
        Interface for Mud Logging
        """
        
        return [931.20, 820.80]

    def casing_running(self):
        """
        Interface for Casing Running
        """

        return 69300 / 31.        

    def drilling_rig_services(self, path):
        """
        Interface for Drilling Rig Services

        # Arguments:
            path: list, list of path of the tpwsi_rr_rigs.xlsx, meals_accommodations.xlsx, rig1peripherals.xlsx
        """
        tpwsi_rr_rigs = pd.read_excel(path[0])
        meals_accommodations = pd.read_excel(path[1])
        rig1_peripherals = pd.read_excel(path[2])

        idx_cd = self.basic_input['rig'] == tpwsi_rr_rigs.ix[:, 'Rig']
        col_cd = self.basic_input['project_loc'] == tpwsi_rr_rigs.columns
        cost1 = np.array(tpwsi_rr_rigs.ix[idx_cd, col_cd]).flatten()[0]

        idx_ma_m = 'Meals' == meals_accommodations.ix[:, 'Type']
        idx_ma_a = 'Accommodation' == meals_accommodations.ix[:, 'Type']
        col_ma = self.basic_input['project_loc'] == meals_accommodations.columns

        if np.sum(idx_ma_m) > 0 and np.sum(idx_ma_a) > 0 and np.sum(col_ma):
            meal_daily_rate = meals_accommodations.ix[idx_ma_m, col_ma]
            accm_daily_rate = meals_accommodations.ix[idx_ma_a, col_ma]
        else:
            meal_daily_rate = 0
            accm_daily_rate = 0
        
        rig1pe_summary = pd.DataFrame(index = ['3RD PARTY', 'CHF', 'CEMENT CUTTERS', 'OTHERS (BOOMTRUCK DRIVER & SV DRIVER)'], columns = ['DURATION', 'MEALS', 'ACCOM', 'TOTAL COST'])
        rig1pe_summary.ix[0, 'DURATION'] = self.basic_input['total_days']
        rig1pe_summary.ix[1, 'DURATION'] = 10.
        if self.basic_input['double_liner']:
            rig1pe_summary.ix[2, 'DURATION'] = 5 * 4
        else:
            rig1pe_summary.ix[2, 'DURATION'] = 4 * 4

        rig1pe_summary.ix[3, 'DURATION'] = self.basic_input['total_days']

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

        if self.basic_input['rig'] == 'Rig 1' or self.basic_input['rig'] == 'Rig 2':
            cost2 = self.asmpt[5]['Base Day Rate']
            cost3 = cost4 = average_rop_day_rate.ix[45 - 30, '0 LTI']
            cost5 = self.asmpt[5]['Additional Payment'] / 365.
            cost6 = self.asmpt[5]['Well Bonus']
            cost7 = average_rop_day_rate.ix[self.basic_input['target_rop'] - 30, 1]
            cost9 = rig1pe_summary.ix[:, 'TOTAL COST'].sum() / self.basic_input['total_days']
            cost10 =  3403000.00 
        else:
            cost2 = cost3 = cost4 = cost5 = cost6 = cost7 = cost9 = cost10 = 0
        cost8 = 0

        drilling_rig_cost = [cost1, cost2, cost3, cost4, cost5, cost6, cost7, cost8, cost9, cost10]

        return drilling_rig_cost

    def drill_pipes(self):
        """
        Interface for Drill Pipes Cost
        """
        
        return [1.50, 47.02, 3250*0.05, 3250*0.02]

    def completion_test(self):
        """
        Interface for Completion Test
        """

        return [2500000, 1100000]

    def other_cementing_services(self):
        """
        Interface for Other Cementing Services
        """    
        if self.basic_input['project_loc'] == 'LGBU':
            other_cementing_cost = 13
        elif self.basic_input['project_loc'] == 'BGBU':
            other_cementing_cost = 16
        elif self.basic_input['project_loc'] == 'NIGBU':
            other_cementing_cost = 15
        elif self.basic_input['project_loc'] == 'MAGBU':
            other_cementing_cost = 10

        return other_cementing_cost

    def rig_mobilization(self, path):
        """
        Interface for Rig Mobilization Cost

        # Arguments:
            path: list, list of path of the handling_hauling.xlsx, rigmove.xlsx, equipment_rates.xlsx
        """
        handling_hauling = pd.read_excel(path[0])
        rigmove = pd.read_excel(path[1])
        equipment = pd.read_excel(path[2])

        rig_mobilization_index = ['40 FT HI-BED TRAILER', '40 FT SEMI-LOW BED TRAILER (35T)', '35 FT LOW BED TRAILER (60T)', '50T CRANE', '70T CRANE', '180T CRANE', 'PAYLOADER', 'FORKLOADER', 'TOWING EQUIPMENT', 'BOOM TRUCK', '5TUT PUMP', 'INTERISLAND RIGMOVE (ALLOCATED)']
        idx1_rm = self.basic_input['project_loc'] == handling_hauling.index
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
        
        self.rm_cost = rm_cost
        
        return rm_cost

    def equipmental_rental(self):
        """
        Interface for Equipmental Rental Cost
        """
        # [cost4_rm, cost5_rm, cost6_rm, 0, cost11_rm, cost8_rm, 0]
        cost = [self.rm_cost[i] for i in [3, 4, 5]]
        cost += [0]
        cost += [self.rm_cost[i] for i in [10, 7]]
        cost += [0]

        return cost