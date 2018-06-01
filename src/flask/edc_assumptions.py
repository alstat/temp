from edc_source import Hole_Casing
import numpy as np
import pandas as pd
import re

class Assumptions(object):

    def __init__(self, basic_input, asmpt):
        self.basic_input = basic_input
        self.asmpt = asmpt

        self.cement_slb_index    = ['Cement', 'Antifoam', 'Extender', 'Dispersant', 'Retarder', 'Silica', 'Micro Silica', 'Fluid loss', 'Retarder, L', 'Fluid loss', 'Yield']
        self.cement_slb_column   = ['Unit1', 'Unit2', 'Price', 'surface_basic', 'surface_acid', 'intermediate_basic', 'intermediate_acid', 'prodn_casing_basic', 'prodn_casing_acid', 'prodn_liner_1_basic', 'cp_basic', 'tie_back_basic', 'reline_basic']
        self.cement_slb_yield    = [np.nan, np.nan, 0, 1.797, 1.803,	1.797, 1.806, 1.8, 1.8, 1.8, 1.8, 1.645, 1.64]
        self.cement_slb_price    = [30.42, 56.77, 0.46, 1.64, 8.31, 24.03, 50.45, 4.07, 38.38, 46.233, 0]
        self.cement_slb_sbasic   = [0.05, 0.35, 0.09, 0.18, 40, 0, 0, 0, 0]
        self.cement_slb_sacid    = [0.05, 0, 0.45, 0.14, 35, 1, 0, 0, 0]
        self.cement_slb_ibasic   = [0.05, 0.25, 0.2, 0.04, 40, 0, 0.65, 0, 0]
        self.cement_slb_iacid    = [0.05, 0, 0.5, 0.088, 35, 1, 0.6, 0, 0]
        self.cement_slb_pbasic   = [0.05, 0, 0.4, 0, 40, 0, 0.85, 0.03, 0]
        self.cement_slb_pacid    = [0.05, 0, 0.5, 0.1, 35, 1, 0.65, 0, 0]
        self.cement_slb_pl1basic = [0.05, 0, 0.5, 0.1, 35, 1, 0.65, 0, 0]
        self.cement_slb_cpbasic  = [0.05, 0, 0.5, 0.1, 35, 1, 0.65, 0, 0]
        self.cement_slb_tbbasic  = [0.05, 0.13, 0.1, 0.155, 40, 0, 0, 0, 0.1]
        self.cement_slb_rbasic   = [0.05, 0.13, 0.1, 0.22, 40, 0, 0, 0, 0.1]

        self.cement_slb_total_const1  = 0.1781
        self.cement_slb_total_const2  = 3.281
        self.cement_slb_total_const3  = 1029.24
        self.cement_slb_total_const4  = 5.6145
        self.cement_slb_total_const5  = 3 * 3.281
        self.cement_slb_total_const6  = 1. # oh excess volume in percentage
        self.cement_slb_total_const7  = 0.1781
        self.cement_slb_total_const8  = 5.6146
        self.cement_slb_total_const9  = 1029.4
        self.cement_slb_total_const10 = 5.614
        self.cement_slb_total_const11 = 40 # IC shoe joint length
        self.cement_slb_total_const12 = 0  # top of cement depth 
        self.cement_slb_total_const13 = 33 # liner plug
        self.cement_slb_total_const14 = .5

        self.cement_slb_total_const15 = 94
        self.cement_slb_total_const16 = 110.
        self.cement_slb_total_const17 = 2.2
        self.cement_slb_total_const18 = 50.

    def roundup(self, x, y):
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

    def cement_slb(self, data):
        """
        Computes the Cement Assumption
        asmpt1 - dictionary, Hole_Casing class using compute method with argument category = size.
        """
        
        table = pd.DataFrame(0, index = self.cement_slb_index, columns = self.cement_slb_column)
        table.ix[:, 'Unit1'] = ['D907 (110lb)', 'D047 (gps)', 'D020 (lbs)', 'D065 (lbs)', 'D800 (lbs)', 'D066 (lbs)', 'D155 (gps)', 'D112 (lbs)', 'D197 (gps)', 'D255 (lbs)', '']
        table.ix[:, 'Unit2'] = ['110lb', 'gal', 'lb', 'lb', 'lb', 'lb', 'gal', 'lb', 'gal', 'lb', '']
        table.ix[:, 'Price'] = self.cement_slb_price
        table.ix['Yield', :] = self.cement_slb_yield

        table_final = pd.DataFrame(0, index = self.cement_slb_index, columns = self.cement_slb_column)
        table_final.ix[:, 'Unit1'] = ['D907 (110lb)', 'D047 (gps)', 'D020 (lbs)', 'D065 (lbs)', 'D800 (lbs)', 'D066 (lbs)', 'D155 (gps)', 'D112 (lbs)', 'D197 (gps)', 'D255 (lbs)', '']
        table_final.ix[:, 'Unit2'] = ['110lb', 'gal', 'lb', 'lb', 'lb', 'lb', 'gal', 'lb', 'gal', 'lb', '']
        table_final.ix[:, 'Price'] = self.cement_slb_price
        table_final.ix['Yield', :] = self.cement_slb_yield

        hc_hole = Hole_Casing(self.basic_input, data, category = 'size').compute(self.asmpt)[0]
        hc_case = Hole_Casing(self.basic_input, data, category = 'size').compute(self.asmpt)[1] 
        
        for i in self.cement_slb_column[3:]:  
            if i[:12] == 'prodn_casing':
                match = i[:12]
                case_depth = self.asmpt[2][match] * self.cement_slb_total_const2
            elif i[:13] == 'prodn_liner_1':
                match = i[:13]
                case_depth = self.asmpt[2][match] * self.cement_slb_total_const2
            elif i == 'tie_back_basic':
                match = 'prodn_casing'
                case_depth = self.asmpt[2][match] * self.cement_slb_total_const2
            elif i == 'cp_basic':
                pass
            else:
                match = re.search(r'^[a-z]+', i).group()
                case_depth = self.asmpt[2][match] * self.cement_slb_total_const2
            # print match
            case_id = Hole_Casing(self.basic_input, data, category = 'case_id').compute(self.asmpt)[match] * 1.
            # print case_id
            # print "Casing ID %f" % case_id
            # if self.basic_input['rh_or_bh'] == 'Big Hole':
            #     # case_id = self.asmpt[3]['bh'][match]
            #     case_id = Hole_Casing(self.basic_input, data, category = 'case_id').compute(self.asmpt)[match]
            # else:
            #     case_id = self.asmpt[3]['rh'][match]
            print("This is the hc_hole")
            print(hc_hole)
            print(match)
            if i == 'reline_basic':
                if self.basic_input['rh_or_bh'] == 'Big Hole':
                    anulus_capacity_open = ((self.asmpt[3]['bh']['prodn_casing']**2 - hc_hole[match]**2) / self.cement_slb_total_const3) * self.cement_slb_total_const4            
                else:
                    anulus_capacity_open = ((self.asmpt[3]['rh']['prodn_casing']**2 - hc_hole[match]**2) / self.cement_slb_total_const3) * self.cement_slb_total_const4            
            else:
                anulus_capacity_open = ((hc_hole[match]**2 - hc_case[match]**2) / self.cement_slb_total_const3) * self.cement_slb_total_const4            

            if i != 'reline_basic':
                anulus_capacity_case = ((case_id**2 - hc_case[match]**2) / self.cement_slb_total_const9) * self.cement_slb_total_const10
            
            casing_capacity = case_id**2 / self.cement_slb_total_const3 * self.cement_slb_total_const4
            # if i == 'prodn_liner_1_basic':
            #     print self.asmpt[3]['bh'][match]
            #     print case_id
            #     print self.cement_slb_total_const3 
            #     print self.cement_slb_total_const4
            if i == 'surface_basic' or i == 'surface_acid':
                if case_depth != 0:
                    total_length_oh = case_depth + self.cement_slb_total_const5
                else:
                    total_length_oh = 0

                open_hole_vol = total_length_oh * anulus_capacity_open
                oh_percentage = open_hole_vol * self.cement_slb_total_const6

                tot_slurry_cft = open_hole_vol + oh_percentage
                tot_slurry_bbl = tot_slurry_cft * self.cement_slb_total_const7
                
                if i == 'surface_basic':
                    table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_sbasic
                    
                    table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                    table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                    table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i], 1)
                    table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)

                else:
                    table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_sacid

                    table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                    table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                    table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                    table_final.ix[6, i] = self.roundup(table.ix[0, i] * table.ix[6, i], 1)
                
            elif i == 'intermediate_basic' or i == 'intermediate_acid':
                case_id = Hole_Casing(self.basic_input, data, category = 'case_id').compute(self.asmpt)[p_match]
                
                # if self.basic_input['rh_or_bh'] == 'Big Hole':
                #     case_id = self.asmpt[3]['bh'][p_match]
                # else:
                #     case_id = self.asmpt[3]['rh'][p_match]

                anulus_capacity_case = ((case_id**2 - hc_case[match]**2) / self.cement_slb_total_const9) * self.cement_slb_total_const10
                
                case_depth_m = self.asmpt[2][match] * self.cement_slb_total_const2
                case_depth_p = self.asmpt[2][p_match] * self.cement_slb_total_const2
                total_length_oh = (case_depth_m - case_depth_p) + (self.cement_slb_total_const5)

                open_hole_vol = total_length_oh * anulus_capacity_open
                oh_percentage = open_hole_vol * self.cement_slb_total_const6

                case_hole_vol = anulus_capacity_case * case_depth_p
                shoe_joint_vol = casing_capacity * self.cement_slb_total_const11

                tot_slurry_cft = open_hole_vol + oh_percentage + case_hole_vol + shoe_joint_vol
                tot_slurry_bbl = tot_slurry_cft * self.cement_slb_total_const7
                
                if i == 'intermediate_basic':
                    table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_ibasic

                    table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                    table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                    table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i], 1)
                    table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                    table_final.ix[6, i] = self.roundup(table.ix[0, i] * table.ix[6, i], 1)
                    table_final.ix[7, i] = self.roundup(table.ix[0, i] * table.ix[7, i] * self.cement_slb_total_const15 / 100., 1)

                else:
                    table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_iacid

                    table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                    table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                    table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                    table_final.ix[6, i] = self.roundup(table.ix[0, i] * table.ix[6, i], 1)
                    table_final.ix[7, i] = self.roundup(table.ix[0, i] * table.ix[7, i] * self.cement_slb_total_const15 / 100., 1)
                
            elif i == 'prodn_casing_basic' or i == 'prodn_casing_acid':
                case_id = Hole_Casing(self.basic_input, data, category = 'case_id').compute(self.asmpt)[p_match]

                # if self.basic_input['rh_or_bh'] == 'Big Hole':
                #     case_id = self.asmpt[3]['bh'][p_match]
                # else:
                #     case_id = self.asmpt[3]['rh'][p_match]

                anulus_capacity_case = ((case_id**2 - hc_case[match]**2) / self.cement_slb_total_const9) * self.cement_slb_total_const10
                case_depth_m = self.asmpt[2][match] * self.cement_slb_total_const2
                case_depth_p = self.asmpt[2][p_match] * self.cement_slb_total_const2
                total_length_oh = (case_depth_m - case_depth_p) + (self.cement_slb_total_const5)

                open_hole_vol = total_length_oh * anulus_capacity_open
                oh_percentage = open_hole_vol * self.cement_slb_total_const6

                case_hole_vol = anulus_capacity_case * (case_depth_p - (case_depth_p - self.cement_slb_total_const5 * 10))
                shoe_joint_vol = casing_capacity * self.cement_slb_total_const11

                tot_slurry_cft = case_hole_vol + oh_percentage + open_hole_vol + shoe_joint_vol
                tot_slurry_bbl = tot_slurry_cft * self.cement_slb_total_const7
                
                if i == 'prodn_casing_basic':
                    table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_pbasic

                    table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                    table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                    table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i], 1)
                    table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                    table_final.ix[6, i] = self.roundup(table.ix[0, i] * table.ix[6, i], 1)
                    table_final.ix[7, i] = self.roundup(table.ix[0, i] * table.ix[7, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[8, i] = self.roundup(table.ix[0, i] * table.ix[8, i], 1)

                else:
                    table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_pacid

                    table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                    table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                    table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i] * self.cement_slb_total_const15 / 100., 1)
                    table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                    table_final.ix[6, i] = self.roundup(table.ix[0, i] * table.ix[6, i], 1)
                    table_final.ix[7, i] = self.roundup(table.ix[0, i] * table.ix[7, i] * self.cement_slb_total_const15 / 100., 1)
            
            elif i == 'prodn_liner_1_basic':
                total_length_oh = (self.cement_slb_total_const5 * 10 - self.cement_slb_total_const12) + (self.cement_slb_total_const5)
                
                anulus_capacity_open = ((hc_hole[match]**2) / self.cement_slb_total_const3) * self.cement_slb_total_const4            

                open_hole_vol = total_length_oh * anulus_capacity_open
                oh_percentage = open_hole_vol * self.cement_slb_total_const6
                
                shoe_joint_vol = casing_capacity * self.cement_slb_total_const11 
                tot_slurry_cft = oh_percentage + open_hole_vol + shoe_joint_vol   
                tot_slurry_bbl = tot_slurry_cft * self.cement_slb_total_const7
            
                table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_pl1basic
                table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                table_final.ix[6, i] = self.roundup(table.ix[0, i] * table.ix[6, i], 1)
                table_final.ix[7, i] = self.roundup(table.ix[0, i] * table.ix[7, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[8, i] = self.roundup(table.ix[0, i] * table.ix[8, i], 1)

            elif i == 'cp_basic':
                table.ix[:table.shape[0] - 1, i] = [self.roundup((self.cement_slb_total_const13 * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_cpbasic

                table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                table_final.ix[6, i] = self.roundup(table.ix[0, i] * table.ix[6, i], 1)
                table_final.ix[7, i] = self.roundup(table.ix[0, i] * table.ix[7, i] * self.cement_slb_total_const15 / 100., 1)

            elif i == 'tie_back_basic':
                case_depth_p = self.asmpt[2][p_match] * self.cement_slb_total_const2
                
                total_length_oh = ((case_depth_p - self.cement_slb_total_const5 * 10) - self.cement_slb_total_const12) + (self.cement_slb_total_const5)
                
                open_hole_vol = total_length_oh * anulus_capacity_open
                oh_percentage = open_hole_vol * self.cement_slb_total_const14
                
                shoe_joint_vol = casing_capacity * self.cement_slb_total_const11

                tot_slurry_cft = oh_percentage + open_hole_vol + shoe_joint_vol
                tot_slurry_bbl = tot_slurry_cft * self.cement_slb_total_const7
                
                table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_tbbasic

                table_final.ix[0, i] = table.ix[0, i] * self.cement_slb_total_const15 / self.cement_slb_total_const16
                table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i], 1)
                table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                table_final.ix[9, i] = self.roundup(table.ix[0, i] * table.ix[9, i] * self.cement_slb_total_const15 / 100., 1)

            elif i == 'reline_basic':
                case_depth_p = self.asmpt[2][p_match] * self.cement_slb_total_const2
                
                total_length_oh = ((case_depth_p - self.cement_slb_total_const5 * 10) - self.cement_slb_total_const12) + (self.cement_slb_total_const5)
                
                open_hole_vol = total_length_oh * anulus_capacity_open
                oh_percentage = open_hole_vol * self.cement_slb_total_const14
                
                shoe_joint_vol = casing_capacity * self.cement_slb_total_const1

                tot_slurry_cft = oh_percentage + open_hole_vol + shoe_joint_vol
                tot_slurry_bbl = tot_slurry_cft * self.cement_slb_total_const7
                
                table.ix[:table.shape[0] - 1, i] = [self.roundup((tot_slurry_bbl * self.cement_slb_total_const8) / table.ix['Yield', i], 1)] + self.cement_slb_rbasic
                table_final.ix[1, i] = self.roundup(table.ix[0, i] * table.ix[1, i], 1)
                table_final.ix[2, i] = self.roundup(table.ix[0, i] * table.ix[2, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[3, i] = self.roundup(table.ix[0, i] * table.ix[3, i] * self.cement_slb_total_const15 / 100., 1)
                table_final.ix[4, i] = self.roundup(table.ix[0, i] * table.ix[4, i], 1)
                table_final.ix[5, i] = self.roundup(table.ix[0, i] * table.ix[5, i] * self.cement_slb_total_const15 / 100. / self.cement_slb_total_const17 / self.cement_slb_total_const18, 1)
                
            if i == 'surface_acid' or i == 'intermediate_acid':
                p_match = match

        return table_final
        # return table