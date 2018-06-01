import numpy as np
import pandas as pd

class Analysis(object):

    def __init__(self, basic_input, asmpt, drlg = None, rop_sec = None):
        """
        Analysis of Permutation

        # Arguments:
            basic_input: dictionary, containing all the basic inputs.
            asmpt      : list, containing the depth of the casing and other assumptions           
            total_rop  : int, baseline total rop
            rop_sec    : dict, rop per section i.e. {surface : x1, intermediate : x2, prodn_casing : x3, prodn_liner_1 : x4, prodn_liner_2 : x5}            
        """
        # self.total_rop = total_rop
        self.basic_input = basic_input
        self.asmpt = asmpt

        if drlg is None and rop_sec is not None:
            self.rop_sec = rop_sec
        elif drlg is None and rop_sec is None:
            raise ValueError("Specify drlg if rop_sec is None.")
        elif drlg is not None and rop_sec is not None:
            raise Warning("drlg is not needed since rop_sec is specified.")
            self.rop_sec = rop_sec
        elif drlg is not None and rop_sec is None:
            self.rop_sec = {}
            self.rop_sec["surface"]  = asmpt[2]["surface"] / drlg["surface"]
            self.rop_sec["intermediate"]  = (asmpt[2]["intermediate"] - asmpt[2]["surface"]) / drlg["intermediate"]
            self.rop_sec["prodn_casing"]  = (asmpt[2]["prodn_casing"] - asmpt[2]["intermediate"]) / drlg["prodn_casing"]
            self.rop_sec["prodn_liner_1"] = (asmpt[2]["prodn_liner_1"] - asmpt[2]["prodn_casing"]) / drlg["prodn_liner_1"]
            self.rop_sec["prodn_liner_2"] = (asmpt[2]["prodn_liner_2"] - asmpt[2]["prodn_liner_1"]) / drlg["prodn_liner_2"]
            
    def drlg_days(self):
        """
        Compute the Drilling Days

        # Value:
            dictionary, drilling days
        """
        
        surface       = self.asmpt[2]["surface"] / self.rop_sec["surface"]
        intermediate  = (self.asmpt[2]["intermediate"] - self.asmpt[2]["surface"]) / self.rop_sec["intermediate"]
        prodn_casing  = (self.asmpt[2]["prodn_casing"] - self.asmpt[2]["intermediate"]) / self.rop_sec["prodn_casing"]
        prodn_liner_1 = (self.asmpt[2]["prodn_liner_1"] - self.asmpt[2]["prodn_casing"]) / self.rop_sec["prodn_liner_1"]
        prodn_liner_2 = (self.asmpt[2]["prodn_liner_2"] - self.asmpt[2]["prodn_liner_1"]) / self.rop_sec["prodn_liner_2"]

        drlg_days = {
            "surface" : surface,
            "intermediate" : intermediate,
            "prodn_casing" : prodn_casing,
            "prodn_liner_1": prodn_liner_1,
            "prodn_liner_2": prodn_liner_2
        }
        
        return drlg_days
    
    # def afe_cost(self):

    # def automate(self, drlg_days, flat_days, liner = "single"):
    #     """
    #     Automating the Computation

    #     This function will compute the total rop and the cost.

    #     # Arguments:
    #         total_rop: int, baseline total rop
    #         asmpt    : list, containing the depth of the casing
    #         rop_sec  : dict, rop per section i.e. {surface : x1, intermediate : x2, prodn_casing : x3, prodn_liner_1 : x4, prodn_liner_2 : x5}
    #     """
    #     d_days = self.drlg_days()
    #     d_obj = Drilling_Days(d_days, flat_days)
    #     target_rop = d_obj.rop(self.basic_input, liner = liner)
    #     afe_obj = Cost_Center(self.basic_input, self.asmpt)
        
class Drilling_Days(object):

    def __init__(self, drlg, flat):
        """
        Drilling Days

        # Arguments:
            drlg: dictionary, drilling days
            flat: dictionary, flat days
        """
        self.drlg = drlg
        self.flat = flat

    def total(self):
        """
        Computes the total days
        """
        x = np.array(self.drlg.values())
        y = np.array(self.flat.values())
        return np.nansum(np.hstack((x, y)))

    def row_total(self):
        total_drlg_flat = {}.fromkeys(self.drlg.keys())

        for keys in self.drlg.keys():
            total_drlg_flat[keys] = self.drlg[keys] + self.flat[keys]

        return total_drlg_flat

    def cell(self, basic_input):
        """
        Computes the drilling days

        # Arguments:
            basic_input: dictionary, containing all the basic inputs 
        """
        if basic_input["prodn_liner_3"]:
            return np.nansum(np.hstack((self.total(), - self.flat["prodn_liner_3"])))
        else:
            return np.nansum(np.hstack((self.total(), - self.flat["prodn_liner_2"])))

    def spud_td(self, liner = "single"):
        """
        Computes the Spud to TD

        # Arguments:
            liner: string, 'single' (default) or double
            sum_type: type of sum, 'all' or 'partial'
        """
        keys = ["surface", "intermediate", "prodn_casing", "prodn_liner_1", "prodn_liner_2", "prodn_liner_3"]
        if liner == "single":
            drlg = [self.drlg[key] for key in keys[:4]]
            flat = [self.flat[key] for key in keys[:3]]
            return np.nansum(np.hstack((drlg, flat)))
        elif liner == "double":
            drlg = [self.drlg[key] for key in keys[:5]]
            flat = [self.flat[key] for key in keys[:4]]
            return np.nansum(np.hstack((drlg, flat)))
        else:
            raise ValueError("liner argument takes only 'single' or 'double', got %s." % liner)

    def rop(self, basic_input, liner = 'single'):
        """
        Computes the ROP

        # Arguments:
            basic_input: dictionary, containing all the basic inputs.
            liner: string, 'single' (default) or double
        """
        return basic_input['target_depth'] / float(self.spud_td(liner))

    def target_rop(self, basic_input, liner = 'single'):
        if basic_input['double_liner']:
            return np.ceil(self.rop(basic_input, 'double'))
        else:
            if self.rop(basic_input) > 75:
                return 75
            else:
                return np.round(self.rop(basic_input))


class Hole_Casing(object):

    def __init__(self, basic_input, data, category = 'size'):
        """
        Hole, Casing Summary

        # Arguments:
            basic_input: dictionary, containing all the basic inputs.
            category   : string, choices are 'size', 'hole_depth', 'case_id' and 'hole_length'.
        """
        if category != 'size' and category != 'hole_depth' and category != 'case_id' and category != 'hole_length':
            raise ValueError("argument category takes only 'size', 'hole_depth', 'case_id', 'hole_length', got %s instead" % category)

        self.basic_input = basic_input
        self.category = category
        self.keys = [
            'surface',
            'intermediate',
            'prodn_casing',
            'prodn_liner_1',
            'prodn_liner_2',
            'prodn_liner_3',
            'reline'
            ]
        self.casing_size_reline = float(data['reline-case-size']) #9.625 # 7 or 5
        self.hole_depth_reline = float(data['reline-hole-depth']) #12.415 # choices are 10.05, 8.755, 6.276

    def compute(self, asmpt):
        """
        Computes the Hole Summary

        # Arguments:
            asmpt : list, containing the hole and casing assumptions
        """
        hole_dict     = {}.fromkeys(self.keys)
        case_dict     = {}.fromkeys(self.keys)
        hole_len_dict = {}.fromkeys(self.keys)
        case_id_dict  = {}.fromkeys(self.keys)
        keys = ['surface', 'intermediate', 'prodn_casing', 'prodn_liner_1', 'prodn_liner_2', 'prodn_liner_3', 'no_label_1', 'no_label_2', 'no_label_3']
        
        for i in self.keys:
            if self.category == 'size' or self.category == 'case_id':
                if i == 'intermediate' or i == 'prodn_casing':
                    if self.basic_input['rh_or_bh'] == 'Regular Hole':
                        hole_dict[i] = asmpt[0]['hole']['rh'][i]
                        case_dict[i] = asmpt[0]['case']['rh'][i]
                    else:
                        hole_dict[i] = asmpt[0]['hole']['bh'][i]
                        case_dict[i] = asmpt[0]['case']['bh'][i]
                else:
                    if i == 'surface':
                        if self.basic_input['b23']:
                            hole_dict[i], case_dict[i] = 23, 18.625
                        else:
                            if self.basic_input['rh_or_bh'] == 'Regular Hole':
                                hole_dict[i] = asmpt[0]['hole']['rh'][i]
                                case_dict[i] = asmpt[0]['case']['rh'][i]
                            else:
                                hole_dict[i] = asmpt[0]['hole']['bh'][i]
                                case_dict[i] = asmpt[0]['case']['bh'][i]

                    elif i == 'prodn_liner_1':
                        if self.basic_input['regular_bottom_section_for_bh']:
                            case_dict[i] = asmpt[0]['case']['rh']['prodn_casing']
                        else:
                            if self.basic_input['rh_or_bh'] == 'Regular Hole':
                                case_dict[i] = asmpt[0]['case']['rh'][i]
                            else:
                                case_dict[i] = asmpt[0]['case']['bh'][i]

                        if self.basic_input['rh_or_bh'] == 'Regular Hole':
                            hole_dict[i] = asmpt[0]['hole']['rh'][i]
                        else:
                            hole_dict[i] = asmpt[0]['hole']['bh'][i]

                    elif i == 'prodn_liner_2':
                        if self.basic_input['aerated_prodn_liner_2']:
                            weight = 1
                        else:
                            weight = 0

                        if case_dict['prodn_liner_1'] > asmpt[0]['case']['rh']['prodn_casing']:
                            hole_dict[i] = asmpt[0]['hole']['bh'][i] * weight
                        else:
                            hole_dict[i] = asmpt[0]['hole']['rh']['prodn_liner_1'] * weight

                        match = hole_dict[i] == np.array([asmpt[1]['hole'][key] for key in keys[3:]]) #np.array(list(asmpt[1]['hole'].values()))[3:]
                        case_dict[i] = 0 if np.sum(match) == 0 else np.array([asmpt[1]['case'][key] for key in keys[3:]])[match][0] #np.array(list(asmpt[1]['case'].values()))[3:][match]
                    
                    elif i == 'prodn_liner_3':
                        if self.basic_input[i]:
                            hole_dict[i] = asmpt[0]['hole']['bh'][i]
                            case_dict[i] = asmpt[0]['case']['bh'][i]
                        else:
                            hole_dict[i] = 0; case_dict[i] = 0
                    elif i == 'reline':
                        if self.category == 'size':
                            case_dict[i] = self.casing_size_reline
                            hole_dict[i] = 0

                if self.category == 'case_id':
                    if case_dict[i] == None:
                        case_id_dict[i] = np.nan
                    else:
                        if i == 'surface' or i == 'intermediate' or i == 'prodn_casing':
                            if self.basic_input['rh_or_bh'] == 'Big Hole':
                                case_id_dict[i] = asmpt[3]['bh'][i]
                            elif self.basic_input['rh_or_bh'] == 'Regular Hole':
                                case_id_dict[i] = asmpt[3]['rh'][i]
                            else:
                                raise ValueError("Choices for Basic Input for 'RH or BH?' are 'Big Hole' and 'Regular Hole', got %s instead" % self.basic_input['rh_or_bh'])
                        elif i == 'prodn_liner_1' or i == 'prodn_liner_2': 
                            match = case_dict[i] == np.array([asmpt[1]['case'][key] for key in keys][3:])
                            case_id_dict[i] = 0 if np.sum(match) == 0 else np.array([asmpt[1]['id'][key] for key in keys][3:])[match].astype(float)[0]
                        elif i == 'prodn_liner_3':
                            if self.basic_input['prodn_liner_3']:
                                case_id_dict[i] = asmpt[3]['bh'][i]
                            else:
                                case_id_dict[i] = np.nan
                        elif i == 'reline':
                            if self.basic_input['reline']:
                                match = self.casing_size_reline == np.array([asmpt[0]['case']['rh'][key] for key in keys[:5]])
                                case_id_dict[i] = 0 if np.sum(match) == 0 else np.array([asmpt[3]['rh'][key] for key in keys[:5]])[match][0]
                            else:
                                case_id_dict[i] = np.nan
            elif self.category == 'hole_depth' or self.category == 'hole_length':
                if i == 'prodn_liner_1' or i == 'prodn_liner_2':
                    hole_dict[i] = asmpt[2][i]
                elif i == 'prodn_liner_3':
                    if self.basic_input[i]:
                        hole_dict[i] = asmpt[2][i]
                    else:
                        hole_dict[i] = 0
                elif i == 'reline':
                    hole_dict[i] = self.hole_depth_reline
                else:
                    hole_dict[i] = asmpt[2][i] + 3

                if self.category == 'hole_length':
                    if i == 'surface':
                        hole_len_dict[i] = hole_dict[i]
                    elif i == 'prodn_liner_2':
                        if hole_dict[i] == 0 or hole_dict[i] == None:
                            hole_len_dict[i] = 0
                        else:
                            if self.basic_input['rh_or_bh'] == 'Big Hole':
                                hole_len_dict[i] = hole_dict[i] - hole_dict[g]
                            else:
                                hole_len_dict[i] = 0
                    elif i == 'prodn_liner_3':
                        if self.basic_input[i]:
                            hole_len_dict[i] = hole_dict[i] - hole_dict[g]
                        else:
                            hole_len_dict[i] = 0
                    elif i == 'reline':
                        if self.basic_input['reline'] is False:
                            hole_len_dict[i] = 0
                        else:
                            hole_len_dict[i] = asmpt[2]['reline']
                    else:
                        hole_len_dict[i] = hole_dict[i] - hole_dict[g]

                g = i

        if self.category == 'size':
            hole_case = [hole_dict, case_dict]
        elif self.category == 'hole_depth':
            hole_case = hole_dict
        elif self.category == 'case_id':
            hole_case = case_id_dict
        elif self.category == 'hole_length':
            hole_case = hole_len_dict

        return hole_case

def header(basic_input, asmpt, data, drlg_input, flat_input):
    """
    Computed the Header Table of the Cost Center.

    # Arguments
        asmpt      : list, containing the hole and casing assumptions
    """
    keys = [
            'surface',
            'intermediate',
            'prodn_casing',
            'prodn_liner_1',
            'prodn_liner_2',
            'prodn_liner_3'
            ]

    head_index = [
        'Hole Size Diameter Inches',
        'Hole Depths Meters',
        'Casing Size Diameter Inches',
        'Casing Depths Meters',
        'Drilling Duration per Hole Size (days)',
        'Flat Spot Duration per Hole Size (days)'
    ]

    if basic_input['double_liner']:
        head_columns = ['rigmove'] + [i + '_' + j for j in keys[:5] for i in ['d', 'f']]
    else:
        head_columns = ['rigmove'] + [i + '_' + j for j in keys[:4] for i in ['d', 'f']]
        
    table = pd.DataFrame(0, index = head_index, columns = head_columns)
    table.ix[5, 'rigmove'] = 13.0

    in_s = Hole_Casing(basic_input, data, category = 'size').compute(asmpt)
    in_d = Hole_Casing(basic_input, data, category = 'hole_depth').compute(asmpt)

    for i in head_columns[1:]:
        if i[0] == 'd':
            if i == 'd_prodn_casing':
                inp = drlg_input['prodn_casing']
            else:
                inp = drlg_input[i[2:]]

            table.ix[[0, 1, 4], i] = [
                in_s[0][i[2:]],
                in_d[i[2:]],
                inp
            ]
        elif i[0] == 'f':
            if i == 'f_prodn_casing':
                inp = flat_input['prodn_casing']
            else:
                inp = flat_input[i[2:]]

            table.ix[[2, 3, 5], i] = [
                in_s[1][i[2:]],
                asmpt[2][i[2:]],
                inp
            ]

    return table

class Unit_Rate(object):

    def __init__(self, basic_input, inventory):
        self.basic_input = basic_input
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
        
    def rockbits(self):
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
    
    # def well_head(self):
    #     table = pd.DataFrame(0, index = )

class Cost_Center(object):

    def __init__(self, basic_input, asmpt, header):
        """
        Class for Cost of the Materials and Supplies

        # Arguments
            basic_input: dictionary, containing all the basic inputs.
        """
        self.asmpt = asmpt
        self.basic_input = basic_input
    
        self.keys = [
            'surface',
            'intermediate',
            'prodn_casing',
            'prodn_liner_1',
            'prodn_liner_2',
            'prodn_liner_3'
            ]

        self.head_index = [
            'Hole Size Diameter Inches',
            'Hole Depths Meters',
            'Casing Size Diameter Inches',
            'Casing Depths Meters',
            'Drilling Duration per Hole Size (days)',
            'Flat Spot Duration per Hole Size (days)'
        ]

        if self.basic_input['double_liner']:
            self.head_columns = ['rigmove'] + [i + '_' + j for j in self.keys[:5] for i in ['d', 'f']]
        else:
            self.head_columns = ['rigmove'] + [i + '_' + j for j in self.keys[:4] for i in ['d', 'f']]
            
        self.head = header

        self.fuel_index = [
            'Rig',
            'Air Drilling Equipment',
            'Crane',
            'Cementing Unit',
            'Water Pump',
            'Rig Trucks (Forkloader, Man lift, Back Hoe, Payloader, Boom Truck)',
            'Tower Lights (Genset)'
        ]
        self.fuel_columns = ['Liters per Day'] + self.head_columns

        self.lubricants_index = ['Lubricants (Oil, grease, etc.)']
        self.lubricants_columns = ['Percent of Fuel Cost'] + self.head_columns
        self.mud_chemicals_index = ['ALUMINUM STEARATE', 'BENTONITE API', 'Caustic Soda', 'CMC TECH LV', 'CONQOR 202-B', 'CONQOR 303 A', 'CONQOR 404', 'DEFOAM-A', 'DUOVIS', 'KLA-GARD', 'Lube 167', 'M-I PAC R', 'OS-1', 'OS-1L', 'POLYPAC R', 'POLYPAC UL', 'POLY-PLUS', 'POLY-PLUS DRY', 'POLYSAL T', 'RESINEX II', 'Safe Cor', 'SAFE-CIDE', 'Soda Ash', 'Sodium Bicarbonate', 'SP-101', 'TACKLE (liquid)', 'TACKLE (dry)', 'TANNATHIN', 'Zinc Carbonate']

        self.cement_columns = self.head_columns
        self.rockbits_columns = ['rigmove'] + [i + '_' + j for j in self.keys[:5] for i in ['d', 'f']] #self.head_columns #+ ['d_prodn_liner_2']

        self.drilling_supplies_index = [
            'Shale Shaker Screens',
            '32" TCI Cutters'
        ]
        self.drilling_supplies_columns = ['unit'] + self.head_columns

        self.wellhead_columns = ['unit'] + self.head_columns

        self.cementing_index = ['Cementing Primary Equipment', '26" Circulating Swedge', '18 5/8" Circulating Swedge', '20 - 18 5/8" CMT Head', '13 3/8" MST', '9 5/8" MST', 'Cement Plug', 'Top Job', 'Cementing Casing', 'Cementing Engineer/Supervisor', 'Equipment Operator/Helper', 'Batch Mixer Operator', 'Toolman(call out)']
        self.directional_drilling_index = ['Directional Engineer', 'MWD Engineer', '9-5/8" Mud Motor, rental', '9-5/8" Mud Motor, run charge', '8" Mud Motor, rental', '8" Mud Motor, run charge', '6-3/4" Mud Motor, rental', '6-3/4" Mud Motor, run charge', 'MWD, operating', 'MWD, rental', 'EMS, rental', 'EMS, operating', 'EMS Redress', '8" NMDC', '6-1/2" Pony NMDC', '6-1/2" NMDC', '26" Stabilizer', '23" Stabilizer', '16"/ 16-1/2" Stabilizer', '12-1/4" Stabilizer', '9-7/8" Stabilizer', '8-1/2" Stabilizer', '6-1/2" Stabilizer', '9" NMDC', '8" Pony NMDC', '8" PWD Tool', '6-3/4" PWD Tool', 'Circulating Hours 8 PWD', 'Circulating Hours 6 PWD', 'PWD Engineer 8in', 'PWD Engineer 6in', 'Tool Mob/Demob']
        self.aerated_drilling_index = ['Equipment Operating Rate', 'Equipment Standby Rate', 'Equipment Mobilization', 'Equipment Demobilization', 'Air Drilling Supervisor', 'Air Drilling Operator', 'Supervisor Mobilization', 'ANCILLARIES', 'Backup Booster Standby', 'Backup Booster Operating', 'Mist Pump Standby', 'Mist Pump Operating', '20-3/4" / 21-1/4" Rotating Head', '21-1/4" Banjo Box (Optional)', 'CONSUMABLES', 'Rotating Rubber Head', 'Corrosion Inhibitor', 'Defoamer', 'Surfactant', 'Rotating Head Refurbishment', 'FV and Sub Inspection and Refurbishment']
        self.drill_pipes_index = ['Rental of S-135 Pipes', 'Post rental inspection', 'Transhipment Cost (Fixed Rate - Import)', 'Transhipment Cost (Truck Rate - Import)']
        self.drilling_rig_services_index = ['FIXED FEE - Rigmove', 'DRILLING RIG SERVICES - Rigmob', 'DRILLING RIG SERVICES - Base Rate @ 50 ROP', 'DRILLING RIG SERVICES - Well Completion', 'Additional Payment', 'No LIH/LTI/Environmental Incident Bonus', 'ROP Bonus', 'Peripherals', 'Meals & Accom', 'Others: Drilling Peripherals']
    
        self.chf_installation_index = ['CHF Casing', 'Mob/Demob of Equipment', 'Mob/Demob of Personnel', 'Service Vehicle; Daily', 'Standby Rate; Daily, Equipment', 'Standby Rate; Daily, Personnel', 'Standby Rate; Daily, Boom Truck', 'Standby Rate; Daily', 'WTL']
        self.jars_shock_index = ['SHOCKTOOL', '8" MDJ JAR', '62" MDJ JAR', '4 and 3/4\" DNT JAR', 'BACKUP JAR', 'REDRESS']

        self.mud_logging_index = ['Mud Logging Service - Operating', 'Mud Logging Service - Standby']
        self.rig_mobilization_index = ['40 FT HI-BED TRAILER', '40 FT SEMI-LOW BED TRAILER (35T)', '35 FT LOW BED TRAILER (60T)', '50T CRANE', '70T CRANE', '180T CRANE', 'PAYLOADER', 'FORKLOADER', 'TOWING EQUIPMENT', 'BOOM TRUCK', '5TUT PUMP', 'INTERISLAND RIGMOVE (ALLOCATED)']
        self.equipment_rental_index = ['50T CRANE', '70T CRANE', '180T CRANE', 'Manlift', '5TUT PUMP', 'FORKLOADER', 'BOOM TRUCK']
        self.rig_allocated_index = ['RIG OML DAILY RATE', 'DEPRECIATION', 'INSURANCE', 'GENEX DAILY RATE', 'THERMAPRIME', 'DG', 'INTER-ISLAND COST']

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

    def fuel(self, asmpt, drlg_input, flat_input, unit_cost = None):
        """
        Computes the fuel table

        # Arguments
            asmpt: pandas.DataFrame, data frame containing the assumption for fuel.
            unit_cost: list, containing the unit cost for each equipment.
        """
        table         = asmpt.copy()
        table.index   = self.fuel_index
        table.columns = self.fuel_columns[1:]

        for i in self.fuel_columns[1:]:
            if i == 'rigmove':
                table.ix[:, i] *= self.head.ix[5, i]
            elif i[0] == 'd':
                if i == 'd_surface':
                    table.ix[:, i] *= self.head.ix[4, i]
                elif i == 'd_intermediate':
                    table.ix[:, i] *= self.head.ix[4, i]
                elif i == 'd_prodn_casing':
                    table.ix[0, i] *= self.head.ix[4, i]
                    table.ix[[2, 3, 4, 5, 6], i] *= self.head.ix[4, i]

                    if self.basic_input['aerated_prodn_casing']:
                        table.ix[1, i] *= self.head.ix[4, i]
                    else:
                        table.ix[1, i] *= 0

                elif i == 'd_prodn_liner_1':
                    table.ix[0, i] *= self.head.ix[4, i]
                    table.ix[[2, 3, 4, 5, 6], i] *= self.head.ix[4, i]

                    if self.basic_input['aerated_prodn_liner_1']:
                        table.ix[1, i] *= self.head.ix[4, i]
                    else:
                        table.ix[1, i] *= 0
                elif i == 'd_prodn_liner_2':
                    table.ix[[0, 2, 3, 4, 5, 6], i] *= drlg_input[i[2:]]
                    if self.basic_input['aerated_prodn_liner_2']:
                        table.ix[1, i] *= drlg_input[i[2:]]
                    else:
                        table.ix[1, i] *= 0
            else:
                if i == 'f_surface':
                    table.ix[0, i] *= self.head.ix[5, i]
                    table.ix[[2, 3, 4, 5, 6], i] *= self.head.ix[5, i]

                    if self.basic_input['aerated_intermediate']:
                        table.ix[1, i] *= self.head.ix[5, i]
                    else:
                        table.ix[1, i] *= 0
                elif i == 'f_intermediate':
                    table.ix[:, i] *= self.head.ix[5, i]
                elif i == 'f_prodn_casing':
                    table.ix[:, i] *= self.head.ix[5, i]
                elif i == 'f_prodn_liner_1':
                    table.ix[:, i] *= self.head.ix[5, i]
                elif i == 'f_prodn_liner_2':
                    table.ix[:, i] *= self.head.ix[5, i]
            if unit_cost is not None:
                table[i] *= self.basic_input['diesel_ph_us']

        return table

    def lubricants(self, asmpt, drlg_input, flat_input, unit_cost = None):
        """
        Computes the Lubricant Table

        # Arguments
            asmpt: pandas.DataFrame, data frame containing the assumption for fuel.
            unit_cost: list, containing the unit cost for each equipment.
        """
        fuel = self.fuel(asmpt, drlg_input, flat_input, unit_cost = unit_cost)
        table = pd.DataFrame(0, index = self.lubricants_index, columns = self.lubricants_columns)
        for i in self.lubricants_columns:
            if i == 'Percent of Fuel Cost':
                if self.basic_input['rig'] == 'Rig 5':
                    table[i] = 5 / 100.
                else:
                    table[i] = 0 / 100.
            else:
                table[i] = table.loc[:, 'Percent of Fuel Cost'] * fuel.sum()[i]

        return table
    
    def mud_chemicals(self, asmpt1, asmpt2, asmpt3, unit_cost = None):
        """
        Computes the Mud Chemicals Table

        # Arguments:
            asmpt1: pd.DataFrame, mud_consumbles table
            asmpt2: Dictionary, hole_casing depth
            asmpt3: Dictionary, hole_casing depth
        """
        table = pd.DataFrame(0, index = self.mud_chemicals_index, columns = ['UNIT'] + self.head_columns)
        table['UNIT'] = ['10 kg bag', '1 MT BB', '25 kg bag', '25 kg bag', '55 gal dr', '55 gal dr', '55 gal dr', '55 gal dr', '25 kg bag', '55 gal dr', '55 gal dr', '25 kg bag', '25 kg bag', '5 gal can', '25 kg bag', '25 kg bag', '5 gal can', '25 kg bag', '25 kg bag', '50 lb bag', '55 gal dr', '25 lt can', '25 kg bag', '25 kg bag', '25 kg bag', '5 gal can', '50 lb bag', '50 lb bag', '25 kg bag']
    
        if self.basic_input['rh_or_bh'] == 'Big Hole':
            u_col = .7
        else:
            u_col = .5

        for i in self.head_columns:
            if i == 'rigmove':
                table.ix[:, i] = 0
            else:
                if i[0] == 'd':
                    idx = i == asmpt1.ix[:, 2]
                    for j in np.arange(4, table.shape[0] + 1):
                        if np.sum(idx) > 0:
                            if i == 'd_surface':
                                if j - 4 == 9 or j - 4 == 22 :
                                    table.ix[j - 4, i] = 0
                                elif j - 4 == 29:
                                    table.ix[j - 4, i] = np.array(asmpt1.ix[idx, j]) * asmpt2[i[2:]] * u_col
                                else:
                                    table.ix[j - 4, i] = self.roundup(np.array(asmpt1.ix[idx, j]) * asmpt2[i[2:]] * u_col, 1)
                            else:
                                if j - 4 == 9 or j - 4 == 22 :
                                    table.ix[j - 4, i] = 0
                                elif j - 4 == 29:
                                    table.ix[j - 4, i] = np.array(asmpt1.ix[idx, j]) * np.nansum([asmpt2[i[2:]], - asmpt3[k[2:]]]) * u_col
                                else:
                                    table.ix[j - 4, i] = self.roundup(np.array(asmpt1.ix[idx, j]) * np.nansum([asmpt2[i[2:]], - asmpt3[k[2:]]]) * u_col, 1)
                        else:
                            table.ix[j - 4, i] = 0
                elif i[0] == 'f':
                    if i == 'f_prodn_liner':
                        table.ix[:, i] = 0
            k = i

            if unit_cost is not None:
                table.ix[:, i] *= np.array(unit_cost) * self.basic_input['forex_ph_us']
        
        return table
    
    def cement_additives(self, asmpt1, asmpt2, unit_cost = None):
        """
        Computes the Cement Additives Table

        # Arguments
            asmpt1: pandas.DataFrame, data frame containing the assumption for Cement Additives
            asmpt2: pandas.DataFrame, equipmental_rental assumption.
            unit_cost: boolean, if None quantities are returned otherwise the computed cost is returned
        """
        if self.basic_input['rh_or_bh'] == 'Big Hole':
            idx = list(asmpt1.index)[:len(list(asmpt1.index)) - 1] + [asmpt2.ix[5, 'Equipment']]
        else:
            idx = list(asmpt1.index)[:len(list(asmpt1.index)) - 1] + [asmpt2.ix[7, 'Equipment']]

        # idx = asmpt['Index']
        table = pd.DataFrame(0, index = idx, columns = self.cement_columns)

        for i in self.cement_columns[1:]:
            if i[0] == 'd':
                if i == 'd_prodn_liner_1':
                    table[i] = np.NaN * asmpt1['cp_basic'].values
                elif i == 'd_prodn_liner_2':
                    table[i] = 0
                else:
                    table[i] = np.ceil(self.asmpt[4]['cement'][i[2:]] * asmpt1['cp_basic'].values)
            else:
                if i == 'f_prodn_liner_1':
                    if self.basic_input['rh_or_bh'] == 'Regular Hole':
                        table.ix[0:2, i] = self.roundup(asmpt1[i[2:] + '_' + 'basic'].values[0:2], 10) + self.roundup(asmpt1['tie_back_basic'].values[0:2], 1)
                        table.ix[3:8, i] = self.roundup(asmpt1[i[2:] + '_' + 'basic'].values[3:8], 10) + self.roundup(asmpt1['tie_back_basic'].values[3:8], 1)                      
                    else:
                        table.ix[0:2, i] = self.roundup(asmpt1[i[2:] + '_' + 'basic'].values[0:2], 10)                        
                        table.ix[3:8, i] = self.roundup(asmpt1[i[2:] + '_' + 'basic'].values[3:8], 10) 
                    
                    table.ix[2, i] = self.roundup(asmpt1[i[2:] + '_' + 'basic'].values[2], 10)
                    table.ix[8:10, i] = self.roundup(asmpt1[i[2:] + '_' + 'basic'].values[8:10], 10)   
                    if self.basic_input['double_liner']:
                        table.ix[10, i] = 0
                    else:
                        table.ix[10, i] = 1
                elif i == 'f_prodn_liner_2':
                    if self.basic_input['rh_or_bh'] == 'Regular Hole':
                        weight1 = 0
                    else:
                        weight1 = 1

                    if self.basic_input['double_liner']:
                        weight2 = 1
                    else:
                        weight2 = 0
                    
                    table.ix[0:10, i] = self.roundup(asmpt1.ix[0:10, 'tie_back_basic'], 10) * weight1 * weight2
                    table.ix[10, i] = weight1 * weight2
                else:
                    if not self.asmpt[4]['acid'][i[2:]]:
                        if i == 'f_intermediate':
                            table.ix[0, i] = np.nansum(np.dstack((np.ceil(asmpt1.loc[:, i[2:] + '_' + 'basic'].values[0]), np.ceil(self.asmpt[4]['top_job'][i[2:]] * 1.2 * asmpt1['cp_basic'].values[0]))), 2).flatten()
                            table.ix[1:, i] = np.nansum(np.dstack((np.ceil(asmpt1.loc[:, i[2:] + '_' + 'basic'].values[1:]), self.asmpt[4]['top_job'][i[2:]] * 1.2 * asmpt1['cp_basic'].values[1:])), 2).flatten()
                        else:
                            table[i] = np.nansum(np.dstack((np.ceil(asmpt1.loc[:, i[2:] + '_' + 'basic'].values), self.asmpt[4]['top_job'][i[2:]] * 1.2 * asmpt1['cp_basic'].values)), 2).flatten()
                    else:
                        if i[2:] + '_' + 'acid' == 'prodn_liner_1_acid':
                            table[i] = 0 * asmpt1['cp_basic'].values
                        else:
                            if i == 'f_intermediate':
                                table.ix[0, i] = np.nansum(np.dstack((np.ceil(asmpt1.loc[:, i[2:] + '_' + 'acid'].values[0]), np.ceil(self.asmpt[4]['top_job'][i[2:]] * 1.2 * asmpt1['cp_basic'].values[0]))), 2).flatten()
                                table.ix[1:, i] = np.nansum(np.dstack((np.ceil(asmpt1.loc[:, i[2:] + '_' + 'acid'].values[1:]), self.asmpt[4]['top_job'][i[2:]] * 1.2 * asmpt1['cp_basic'].values[1:])), 2).flatten()
                            else:
                                table[i] = np.nansum(np.dstack((np.ceil(asmpt1.loc[:, i[2:] + '_' + 'acid'].values), self.asmpt[4]['top_job'][i[2:]] * 1.2 * asmpt1['cp_basic'].values)), 2).flatten()

        # output = table.ix[:len(table) - 1, :].copy()
        # if self.basic_input['rh_or_bh'] == 'Regular Hole' or self.basic_input['rh_or_bh'] == 'Big Hole':
        #     if self.basic_input['double_liner']:
        #         output.loc['CBP'] = list(np.repeat(0, len(self.cement_columns)))
        #     else:
        #         output.loc['CBP'] = (list(np.repeat(0, len(self.cement_columns) - 1)) + [1]) * 1
        table.ix[10, :8] = 0 
        if unit_cost is not None:
            weight = np.array(unit_cost) * self.basic_input['forex_ph_us']
            for i in self.cement_columns:
                table.ix[:, i] *= weight
            # unit_cost = cemt.ix[:10, 'Price']
            # weight = np.array(unit_cost) * self.basic_input['forex_ph_us']
            # for i in self.cement_columns:
            #     output[i] *= weight

        return table #output

    def rockbits(self, asmpt, qty, unit_cost = None, category = 'SMITH'):
        """
        Computes the Rockbits Table

        # Arguments
            asmpt: pandas.DataFrame, data frame containing the assumption for Rockbits.
            unit_cost: list, containing the unit cost for each equipment.
            qty: boolean dictionary, containing qty for each equipment
        """
        idx = asmpt.index

        table = pd.DataFrame(0, index = idx, columns = self.rockbits_columns)

        for i in self.rockbits_columns:
            
            if i[0] == 'd':
                if i == 'd_surface':
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.loc['32" TCI Cutters (3 pcs)', i] = asmpt.loc['32" TCI Cutters (3 pcs)', 'PROG' + ' ' + category]

                    table.loc['26" x Tricone IADC Code 515', i] = asmpt.loc['26" x Tricone IADC Code 515', 'PROG' + ' ' + category]

                elif i == 'd_intermediate':
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.loc['23" x Tricone IADC Code 515', i] = asmpt.loc['23" x Tricone IADC Code 515', 'PROG' + ' ' + category]
                    else:
                        table.loc['17 " x Tricone IADC Code 525', i] = asmpt.loc['17 " x Tricone IADC Code 525', 'PROG' + ' ' + category]
                        table.loc['17 " x Tricone IADC Code 615', i] = asmpt.loc['17 " x Tricone IADC Code 615', 'PROG' + ' ' + category]

                        if category == 'HUGHES':
                            table.loc['23" x Tricone IADC Code 515', i] = asmpt.loc['23" x Tricone IADC Code 515', 'PROG' + ' ' + category]

                elif i == 'd_prodn_casing':
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.loc['17 " x Tricone IADC Code 525', i] = asmpt.loc['17 " x Tricone IADC Code 525', 'PROG' + ' ' + category]
                        table.loc['17 " x Tricone IADC Code 615', i] = asmpt.loc['17 " x Tricone IADC Code 615', 'PROG' + ' ' + category]
                    else:
                        table.loc['12.25 " x PDC PDC BIT', i] = asmpt.loc['12.25 " x PDC PDC BIT', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 217', i] = asmpt.loc['12.25 " x Tricone IADC 217', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 517', i] = asmpt.loc['12.25 " x Tricone IADC 517', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 537', i] = asmpt.loc['12.25 " x Tricone IADC 537', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 547', i] = asmpt.loc['12.25 " x Tricone IADC 547', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 637', i] = asmpt.loc['12.25 " x Tricone IADC 637', 'PROG' + ' ' + category]   
                    
                    if category == 'HUGHES':
                            table.loc['17 " x Tricone IADC Code 525', i] = asmpt.loc['17 " x Tricone IADC Code 525', 'PROG' + ' ' + category]

                elif i == 'd_prodn_liner_1':
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.loc['12.25 " x PDC PDC BIT', i] = asmpt.loc['12.25 " x PDC PDC BIT', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 217', i] = asmpt.loc['12.25 " x Tricone IADC 217', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 517', i] = asmpt.loc['12.25 " x Tricone IADC 517', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 537', i] = asmpt.loc['12.25 " x Tricone IADC 537', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 547', i] = asmpt.loc['12.25 " x Tricone IADC 547', 'PROG' + ' ' + category]
                        table.loc['12.25 " x Tricone IADC 637', i] = asmpt.loc['12.25 " x Tricone IADC 637', 'PROG' + ' ' + category]
                    else:
                        table.loc['8.5 " x PDC PDC BIT', i] = asmpt.loc['8.5 " x PDC PDC BIT', 'PROG' + ' ' + category]
                        table.loc['8.5 " x Tricone IADC 117 / 217', i] = asmpt.loc['8.5 " x Tricone IADC 117 / 217', 'PROG' + ' ' + category]
                        table.loc['8.5 " x Tricone IADC 637', i] = asmpt.loc['8.5 " x Tricone IADC 637', 'PROG' + ' ' + category]

                elif i == 'd_prodn_liner_2':
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.loc['9-7/8 " x PDC PDC Bit', i] = asmpt.loc['9-7/8 " x PDC PDC Bit', 'PROG' + ' ' + category]
                        table.loc['9-7/8 " x Tricone IADC 117/217', i] = asmpt.loc['9-7/8 " x Tricone IADC 117/217', 'PROG' + ' ' + category]
                        table.loc['9-7/8 " x Tricone IADC 517', i] = asmpt.loc['9-7/8 " x Tricone IADC 517', 'PROG' + ' ' + category]
                        table.loc['9-7/8 " x Tricone IADC 537', i] = asmpt.loc['9-7/8 " x Tricone IADC 537', 'PROG' + ' ' + category]
                        table.loc['9-7/8 " x Tricone IADC 637', i] = asmpt.loc['9-7/8 " x Tricone IADC 637', 'PROG' + ' ' + category]

                    if qty['8.5 " x PDC PDC BIT']:
                        table.loc['8.5 " x PDC PDC BIT', i] = asmpt.loc['8.5 " x PDC PDC BIT', 'PROG' + ' ' + category]
                    if qty['8.5 " x Tricone IADC 117 / 217']:
                        table.loc['8.5 " x Tricone IADC 117 / 217', i] = asmpt.loc['8.5 " x Tricone IADC 117 / 217', 'PROG' + ' ' + category]
                    if qty['8.5 " x Tricone IADC 637']:
                        table.loc['8.5 " x Tricone IADC 637', i] = asmpt.loc['8.5 " x Tricone IADC 637', 'PROG' + ' ' + category]

            if unit_cost is not None:
                table.ix[:, i] *= unit_cost

        return table

    def drilling_supplies(self, data, unit_cost = None):
        """
        Computes the Drilling Supplies
        """
        table = pd.DataFrame(0, index = self.drilling_supplies_index, columns = self.drilling_supplies_columns)
        table['unit'] = ['piece', 'set']

        in_h = Hole_Casing(self.basic_input, data, category = 'hole_length').compute(self.asmpt)
        for i in self.drilling_supplies_columns:
            if i[0] == 'd':
                if i == 'd_surface':
                    if self.head.loc['Hole Depths Meters', i] == 0.:
                        table.loc['Shale Shaker Screens', i] = 0.
                    else:
                        table.loc['Shale Shaker Screens', i] = 5.

                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        if in_h[i[2:]] > 0.:
                            table.loc['32" TCI Cutters', i] = 1.
                        else:
                            table.loc['32" TCI Cutters', i] = 0.
                    else:
                        table.loc['32" TCI Cutters', i] = 0.

                elif i == 'd_intermediate':
                    if self.head.loc['Hole Depths Meters', i] == 0.:
                        table.loc['Shale Shaker Screens', i] = 0.
                    else:
                        table.loc['Shale Shaker Screens', i] = 4.

                elif i == 'd_prodn_casing':
                    if self.head.loc['Hole Depths Meters', i] == 0.:
                        table.loc['Shale Shaker Screens', i] = 0.
                    else:
                        table.loc['Shale Shaker Screens', i] = 8.

                elif i == 'd_prodn_liner_1':
                    if self.head.loc['Hole Depths Meters', i] == 0.:
                        table.loc['Shale Shaker Screens', i] = 0.
                    else:
                        table.loc['Shale Shaker Screens', i] = 4.

                elif i == 'd_prodn_liner_2':
                    if self.basic_input['double_liner']:
                        table.loc['Shale Shaker Screens', i] = 4.
                    else:
                        table.loc['Shale Shaker Screens', i] = 0.

            if unit_cost is not None:
                table.ix[:, i] *= np.array(unit_cost)

        return table
    
    def casings(self, asmpt1, asmpt2, unit_cost = None):
        """
        Computes the Casing Table

        # Arguments
            asmpt1: pd.DataFrame, big hole table
            asmpt2: pd.DataFrame, regular hole table
        """

        if self.basic_input['rh_or_bh'] == 'Big Hole':
            self.casings_index = list(asmpt1.CASINGS.values)[:41] +  list(asmpt1.CASINGS.values)[36:]
        else:
            self.casings_index = list(asmpt2.CASINGS.values) + list(np.repeat('NA', 12)) + list(asmpt1.CASINGS.values)[36:]
        casing_columns = ['rigmove'] + [i + '_' + j for j in self.keys[:5] for i in ['d', 'f']]
        table = pd.DataFrame(0, index = self.casings_index, columns = ['UNIT'] + casing_columns)
        
        for i in casing_columns:
            if i[0] == 'f':
                for j in np.arange(table.shape[0]):
                    if i == 'f_surface':
                        if j < 7:
                            if self.basic_input['rh_or_bh'] == 'Big Hole':
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt1.ix[j, 3] * asmpt1.ix[j, 4]
                                else:
                                    table.ix[j, i] = asmpt1.ix[j, 3]
                            elif self.basic_input['rh_or_bh'] == 'Regular Hole':
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt2.ix[j, 3] * asmpt2.ix[j, 4]
                                else:
                                    table.ix[j, i] = asmpt2.ix[j, 3]
                        else:
                            table.ix[j, i] = 0
                    elif i == 'f_intermediate':
                        if j > 6 and j < 16:
                            if self.basic_input['rh_or_bh'] == 'Big Hole':
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt1.ix[j, 3] * asmpt1.ix[j, 4]
                                else:
                                    table.ix[j, i] = asmpt1.ix[j, 3]
                            elif self.basic_input['rh_or_bh'] == 'Regular Hole':
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt2.ix[j, 3] * asmpt2.ix[j, 4]
                                else:
                                    table.ix[j, i] = asmpt2.ix[j, 3]
                        else:
                            table.ix[j, i] = 0
                    elif i == 'f_prodn_casing':
                        if j > 15 and j < 26:
                            if self.basic_input['rh_or_bh'] == 'Big Hole':
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt1.ix[j, 3] * asmpt1.ix[j, 4]
                                else:
                                    table.ix[j, i] = asmpt1.ix[j, 3]
                            elif self.basic_input['rh_or_bh'] == 'Regular Hole':
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt2.ix[j, 3] * asmpt2.ix[j, 4]
                                else:
                                    table.ix[j, i] = asmpt2.ix[j, 3]
                        else:
                            table.ix[j, i] = 0
                    elif i == 'f_prodn_liner_1':
                        if self.basic_input['regular_bottom_section_for_bh']:
                            weight = 0
                        else:
                            weight = 1
                        if j > 25 and j < 33:
                            if self.basic_input['rh_or_bh'] == 'Big Hole':
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt1.ix[j, 3] * asmpt1.ix[j, 4] * weight
                                else:
                                    table.ix[j, i] = asmpt1.ix[j, 3]
                            elif self.basic_input['rh_or_bh'] == 'Regular Hole':
                                if unit_cost is not None:
                                    if j < 29:
                                        table.ix[j, i] = asmpt2.ix[j, 3] * asmpt2.ix[j, 4] * weight
                                    else:
                                        table.ix[j, i] = 0
                                else:
                                    if j < 29:
                                        table.ix[j, i] = asmpt2.ix[j, 3]
                                    else:
                                        table.ix[j, i] = 0
                        elif j > 40 and j < 48:
                            if self.basic_input['regular_bottom_section_for_bh']:
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt1.ix[j - 5, 3] * asmpt1.ix[j - 5, 4]
                                else:
                                    table.ix[j, i] = asmpt1.ix[j - 5, 3]
                            else:
                                table.ix[j, i] = 0
                        
                        else:
                            table.ix[j, i] = 0

                    elif i == 'f_prodn_liner_2':
                        if j > 32 and j < 36:
                            if not self.basic_input['double_liner']:
                                table.ix[j, i] = 0
                            else:
                                if self.basic_input['rh_or_bh'] == 'Big Hole':
                                    if unit_cost is not None:
                                        table.ix[j, i] = asmpt1.ix[j, 3] * asmpt1.ix[j, 4]
                                    else:
                                        table.ix[j, i] = asmpt1.ix[j, 3]
                                else:
                                    if unit_cost is not None:
                                        table.ix[j, i] = 0
                                    else:
                                        table.ix[j, i] = 0
                            if self.basic_input['regular_bottom_section_for_bh']:
                                table.ix[j, i] *= 0
                            else:
                                table.ix[j, i] *= 1
                        elif j > 47 and j < 51:
                            if self.basic_input['regular_bottom_section_for_bh']:
                                if unit_cost is not None:
                                    table.ix[j, i] = asmpt1.ix[j - 5, 3] * asmpt1.ix[j - 5, 4]
                                else:
                                    table.ix[j, i] = asmpt1.ix[j - 5, 3]
                        
        # this is not included in the summary, do not remove
        # if unit_cost is not None:
        #     table.ix[41, 'd_prodn_liner_1'] = table.ix[41:48, 'f_prodn_liner_1'].sum()
            
        return table

    def wellhead(self, asmpt, unit_cost = None):
        """
        Computes the Wellhead Table

        # Arguments
            asmpt: pandas.DataFrame, containst the materials for the wellhead.
            unit_cost: list, containing the unit cost for each equipment.
        """
        if self.basic_input['rh_or_bh'] == 'Big Hole':
            idx = np.append(asmpt['Big Hole Wellhead Assembly'].values, 'Bolts and gastkets')
        else:
            idx = np.append(asmpt['Regular Hole Wellhead Assembly'].values, 'Bolts and gastkets')

        table = pd.DataFrame(0, index = idx, columns = self.wellhead_columns)

        for i in self.wellhead_columns:
            if i[0] == 'f':
                if i == 'f_intermediate':
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.ix[0, i] = asmpt.ix[0, 'Big Hole Quantity']
                    else:
                        table.ix[0, i] = asmpt.ix[0, 'Regular Hole Quantity']
                        
                if i == 'f_prodn_liner_1':
                    if not self.basic_input['double_liner']:
                        if self.basic_input['rh_or_bh'] == 'Big Hole':
                            table.ix[1:4, i] = asmpt.ix[1:4, 'Big Hole Quantity'].values
                        elif self.basic_input['rh_or_bh'] == 'Regular Hole':
                            table.ix[1:4, i] = asmpt.ix[1:4, 'Regular Hole Quantity'].values

                        table.ix[4, i] = 1
                    else:
                        table.ix[1:4, i] = 0
                        table.ix[4, i] = 0

                if i == 'f_prodn_liner_2':
                    table.ix[0, i] = 0
                    if self.basic_input['double_liner']:
                        if self.basic_input['rh_or_bh'] == 'Big Hole':
                            table.ix[1:4, i] = asmpt.ix[1:4, 'Big Hole Quantity'].values
                        else:
                            table.ix[1:4, i] = asmpt.ix[1:4, 'Regular Hole Quantity'].values
                        table.ix[4, i] = 1
                    else:
                        table.ix[:, i] = 0
            if unit_cost is not None:
                table.ix[:, i] *= unit_cost

        return table
    
    def cementing(self, unit_cost = None, last_col = ''):
        table = pd.DataFrame(0, index = self.cementing_index, columns = ['UNIT'] + self.head_columns)
        table.ix[:, 'UNIT'] = ['per day', 'per day', 'per day', 'per day', 'per day', 'per day', 'per job', 'per job', 'per job', 'per day', 'per day', 'per day', 'per day']

        for i in self.head_columns:
            if i == 'rigmove':
                table.ix[ 0, i] = self.head.ix[5, i]
                table.ix[ 9, i] = self.head.ix[5, i] - 5
                table.ix[10, i] = self.head.ix[5, i] - 4
                table.ix[11, i] = self.head.ix[5, i] - 4
            else:
                if i[0] == 'd':
                    if i == 'd_surface':
                        if self.basic_input['yes_if_without_pre-installed_csg']:
                            weight = 1
                        else:
                            weight = 0

                        if self.basic_input['yes_if_without_pre-installed_csg']:
                            table.ix[0, i] = self.head.ix[4, i]
                            if self.basic_input['rh_or_bh'] == 'Big Hole':
                                table.ix[1:4, i] = 5 * weight
                            else:
                                table.ix[1:4, i] = 0
                            table.ix[9:12, i] = self.head.ix[4, i]
                            
                        else:
                            table.ix[0, i] = 0
                            table.ix[1:4, i] = 0
                            table.ix[9:12, i] = 0

                        if self.asmpt[4]['cement']['surface'] != '':
                            table.ix[6, i] = self.asmpt[4]['cement']['surface']
                        else:
                            table.ix[6, i] = 0

                    elif i == 'd_intermediate':
                        table.ix[0, i] = self.head.ix[4, i]
                        table.ix[9:12, i] = self.head.ix[4, i]
                        if self.asmpt[4]['cement']['intermediate'] != '':
                            table.ix[6, i] = self.asmpt[4]['cement']['intermediate']
                        else:
                            table.ix[6, i] = 0
                    
                    elif i == 'd_prodn_casing':
                        table.ix[0, i] = self.head.ix[4, i]
                        if self.asmpt[4]['cement']['prodn_casing'] != '':
                            table.ix[6, i] = self.asmpt[4]['cement']['prodn_casing']
                        else:
                            table.ix[6, i] = 0

                        table.ix[9:12, i] = self.head.ix[4, i]
                    elif i == 'd_prodn_liner_1':
                        table.ix[0, i] = self.head.ix[4, i]
                        table.ix[9:12, i] = self.head.ix[4, i]
                    elif i == 'd_prodn_liner_2':
                        table.ix[0, i] = self.head.ix[4, i]
                        table.ix[9:12, i] = self.head.ix[4, i]
                elif i[0] == 'f':
                    if i == 'f_surface':
                        table.ix[0, i] = self.head.ix[5, i]
                        table.ix[9:12, i] = self.head.ix[5, i]
                        if self.asmpt[4]['top_job']['surface'] != '':
                            table.ix[7, i] = self.asmpt[4]['top_job']['surface']
                        else:
                            table.ix[7, i] = 0

                        if self.basic_input['yes_if_without_pre-installed_csg']:
                            table.ix[8, i] = 1
                        else:
                            table.ix[8, i] = 0
            
                    elif i == 'f_intermediate':
                        table.ix[0, i] = self.head.ix[5, i]
                        if self.asmpt[4]['top_job']['intermediate'] != '':
                            table.ix[7, i] = self.asmpt[4]['top_job']['intermediate']
                        else:
                            table.ix[7, i] = 0

                        if self.head.ix[5, i] != '':
                            table.ix[8, i] = 1
                        else:
                            table.ix[8, i] = 0

                        table.ix[9:12, i] = self.head.ix[5, i]

                    elif i == 'f_prodn_casing':
                        table.ix[0, i] = self.head.ix[5, i]
                        if self.asmpt[4]['top_job']['prodn_casing'] != '':
                            table.ix[7, i] = self.asmpt[4]['top_job']['prodn_casing']
                        else:
                            table.ix[7, i] = 0

                        if self.head.ix[5, i] != '':
                            table.ix[8, i] = 1
                        else:
                            table.ix[8, i] = 0

                        table.ix[9:12, i] = self.head.ix[5, i]
                    elif i == 'f_prodn_liner_1':
                        table.ix[0, i] = self.head.ix[5, i]
                        if self.basic_input['double_liner']:
                            weight1 = 0
                            table.ix[6, i] = 0
                            table.ix[8, i] = 0
                        else:
                            weight1 = 10
                            table.ix[6, i] = 1
                            table.ix[8, i] = 1
                        
                        # if last_col == '':
                        #     weight1 = 10
                        #     table.ix[6, i] = 1
                        #     table.ix[8, i] = 1
                        # else:
                        #     weight1 = 0
                        #     table.ix[6, i] = 0
                        #     table.ix[8, i] = 0

                        if self.basic_input['rh_or_bh'] == 'Big Hole':
                            weight2 = 1
                            weight3 = 0
                        else:
                            weight2 = 0
                            weight3 = 1

                        table.ix[4, i] = weight1 * weight2
                        table.ix[5, i] = weight1 * weight3
                        
                        table.ix[9:12, i] = self.head.ix[5, i]
                        table.ix[12, i] = weight1 * weight2
                    elif i == 'f_prodn_liner_2':
                        if last_col == '':
                            weight1 = 10
                            weight5 = 1
                        else:
                            weight1 = 0
                            weight5 = 0

                        if self.basic_input['rh_or_bh'] == 'Regular Hole':
                            weight2 = 0
                            weight4 = 1
                        else:
                            weight2 = 1
                            weight4 = 0

                        if self.basic_input['double_liner']:
                            weight3 = 1
                        else:
                            weight3 = 0
                        
                        table.ix[[0, 9, 10, 11], i] = self.head.ix[5, i]
                        table.ix[4, i] = weight1 * weight2 * weight3
                        table.ix[5, i] = weight1 * weight4 * weight3
                        table.ix[[6, 8], i] = weight5 * weight2 * weight3
                        table.ix[12, i] = weight1
                        
            if unit_cost is not None:
                table.ix[:, i] *= np.array(unit_cost) * self.basic_input['forex_ph_us']

        return table
    
    def directional_drilling(self, asmpt1, unit_cost = None, triple_liner = '', unknown_row = True, qty = [2, 2, 4, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1]):
        """
        Computes the Directional Drilling

        # Arguments:
            asmpt1: pandas.DataFrame, transhipment table
            qty: list, quantity
            triple_liner: activated if triple_liner is considered
            unknown_row: 10th row of cost value of cementing table
        """
        table = pd.DataFrame(0, index = self.directional_drilling_index, columns = self.head_columns)
        
        for i in self.head_columns:
            if i == 'rigmove':
                if self.head.ix[5, i] != 0:
                    table.ix[0:2, i] = 2
                    idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]
                    if np.sum(idx) > 0:
                        table.ix[[2, 9, 10, 16, 23], i] = np.array(asmpt1.ix[idx, 1])
                    else:
                        table.ix[[2, 9, 10, 16, 23], i] = 0
                else:
                    table.ix[0:2, i] = 0
                    table.ix[[2, 9, 10, 16, 23], i] = 0
            elif i[0] == 'd':
                if i == 'd_surface':
                    table.ix[0:3, i] = self.head.ix[4, i]
                    table.ix[3, i] = self.head.ix[4, i] * 24
                    table.ix[8:13, i] = self.head.ix[4, i]
                    table.ix[16, i] = self.head.ix[4, i]
                
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        weight1 = 1
                    else:
                        weight1 = 0

                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        weight2 = 1
                    else:
                        weight2 = 0
                    
                    idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]
                    if np.sum(idx) > 0:
                        table.ix[17, i] = np.array(asmpt1.ix[idx, 1]) * weight1 * weight2
                    else:
                        table.ix[17, i] = 0
                    table.ix[23, i] = self.head.ix[4, i]
                
                elif i == 'd_intermediate':
                    table.ix[0:3, i] = self.head.ix[4, i]
                    table.ix[3, i] = self.head.ix[4, i] * 24
                    table.ix[8:13, i] = self.head.ix[4, i]

                    idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]
                    if np.sum(idx) > 0:
                        table.ix[16, i] = np.array(asmpt1.ix[idx, 1])
                        if self.basic_input['rh_or_bh'] == 'Big Hole':
                            table.ix[17, i] = np.array(asmpt1.ix[idx, 1])
                        else:
                            table.ix[17, i] = 0
                    else:
                        table.ix[16, i] = 0
                    table.ix[23, i] = self.head.ix[4, i]

                elif i == 'd_prodn_casing':
                    table.ix[0:2, i] = self.head.ix[4, i]

                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.ix[2, i] = self.head.ix[4, i]
                        table.ix[3, i] = self.head.ix[4, 'd_intermediate'] * 24
                        table.ix[4, i] = 0
                        table.ix[5, i] = 0
                        table.ix[18, i] = self.head.ix[4, i]
                        table.ix[23, i] = self.head.ix[4, i]
                        idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]
                        if np.sum(idx) > 0:
                            table.ix[19, i] = np.array(asmpt1.ix[idx, 1])
                        else:
                            table.ix[19, i] = 0
                    else:
                        table.ix[2, i] = 0
                        table.ix[3, i] = 0
                        table.ix[4, i] = self.head.ix[4, i]
                        table.ix[5, i] = self.head.ix[4, i] * 24
                        table.ix[18, i] = 0
                        table.ix[19, i] = self.head.ix[4, i]
                        table.ix[23, i] = 0
                    table.ix[8:13, i] = self.head.ix[4, i]
                    
                elif i == 'd_prodn_liner_1':
                    table.ix[0:2, i] = self.head.ix[4, i]

                    idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]
                    if np.sum(idx) > 0:
                        table.ix[2, i] = np.array(asmpt1.ix[idx, 1])
                        table.ix[23, i] = np.array(asmpt1.ix[idx, 1])
                    else:
                        table.ix[2, i] = 0
                        table.ix[23, i] = 0
                    
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.ix[[4, 24], i] = self.head.ix[4, i]
                        table.ix[5, i] = self.head.ix[4, i] * 24
                        table.ix[21, i] = 0
                    else:
                        table.ix[[4, 24], i] = 0
                        table.ix[5, i] = 0
                        table.ix[21, i] = self.head.ix[4, i]

                    table.ix[8:13, i] = self.head.ix[4, i]
                    table.ix[24, i] = self.head.ix[4, i]
                    if self.basic_input['pwd_fliner1']:
                        table.ix[25, i] = 1
                        table.ix[27, i] = self.head.ix[4, i] * 24
                        table.ix[29, i] = self.head.ix[4, i]
                    else:
                        table.ix[25, i] = 0
                        table.ix[27, i] = 0
                        table.ix[29, i] = 0
                elif i == 'd_prodn_liner_2':
                    if self.basic_input['double_liner']:
                        table.ix[0:2, i] = self.head.ix[4, i]
                        table.ix[8:13, i] = self.head.ix[4, i]
                    else:
                        table.ix[0:2, i] = 0
                        table.ix[8:13, i] = 0

                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.ix[6, i] = self.head.ix[4, i]
                        table.ix[7, i] = self.head.ix[4, i] * 24
                        table.ix[20, i] = self.head.ix[4, i]
                    else:
                        table.ix[6, i] = 0
                        table.ix[7, i] = 0
                        table.ix[20, i] = 0

                    if self.basic_input['pwd_fliner2']:
                        weight1 = 1
                    else:
                        weight1 = 0
                    
                    if not self.basic_input['double_liner']:
                        weight2 = 0
                    else:
                        weight2 = 1
                    
                    table.ix[26, i] = weight1 * weight2

                    if self.basic_input['pwd_fliner1']:
                        table.ix[28, i] = self.head.ix[4, i] * 24
                    else:
                        table.ix[28, i] = 0
                    
                    if self.basic_input['pwd_fliner2']:
                        table.ix[30, i] = self.head.ix[4, i]
                    else:
                        table.ix[30, i] = 0
            elif i[0] == 'f':
                if i == 'f_surface':
                    table.ix[[0, 1, 2, 8, 9, 10, 11, 12, 16, 17, 23], i] = self.head.ix[5, i]
                elif i == 'f_intermediate':
                    table.ix[0:2, i] = self.head.ix[5, i]
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.ix[2, i] = self.head.ix[5, i]
                        weight1 = 0
                        weight2 = 1
                    else:
                        weight1 = 1
                        weight2 = 0

                    idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]
                    if np.sum(idx) > 0:
                        table.ix[4, i] = np.array(asmpt1.ix[idx, 1]) * weight1
                        table.ix[18, i] = np.array(asmpt1.ix[idx, 1]) * weight2
                        if self.basic_input['rh_or_bh'] == 'Big Hole':
                            table.ix[19, i] = 0
                        else:
                            table.ix[19, i] = np.array(asmpt1.ix[idx, 1])
                    else:
                        table.ix[4, i] = 0 
                        table.ix[18, i] = 0
                    
                    table.ix[8:13, i] = self.head.ix[5, i]
                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        table.ix[23, i] = self.head.ix[5, i]
                    else:
                        table.ix[23, i] = 0
                elif i == 'f_prodn_casing':
                    table.ix[0:2, i] = self.head.ix[5, i]

                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        weight = 1
                    else:
                        weight = 0

                    idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]
                    if np.sum(idx) > 0:
                        table.ix[18, i] = np.array(asmpt1.ix[idx, 1]) * weight
                        table.ix[24, i] = np.array(asmpt1.ix[idx, 1])
                        if self.basic_input['rh_or_bh'] == 'Big Hole':
                            table.ix[4, i] = np.array(asmpt1.ix[idx, 1])
                            table.ix[19, i] = self.head.ix[5, i]
                            table.ix[21, i] = 0
                        else:
                            table.ix[4, i] = self.head.ix[5, i]
                            table.ix[19, i] = np.array(asmpt1.ix[idx, 1])
                            table.ix[21, i] = np.array(asmpt1.ix[idx, 1])
                    else:
                        table.ix[4, i] = 0
                        table.ix[18, i] = 0
                        table.ix[24, i] = np.array(asmpt1.ix[idx, 1])
                    table.ix[8:13, i] = self.head.ix[5, i]

                    if self.basic_input['pwd_fliner1']:
                        table.ix[29, i] = 5
                        table.ix[31, i] = 1
                    else:
                        table.ix[29, i] = 0
                        table.ix[31, i] = 0
                    
                elif i == 'f_prodn_liner_1':
                    table.ix[0:2, i] = self.head.ix[5, i]
                    if self.basic_input['double_liner']:
                        table.ix[4, i] = 0
                    else:
                        table.ix[4, i] = 1
                    idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]

                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        weight = 1
                        if np.sum(idx) > 0:
                            table.ix[20, i] = np.array(asmpt1.ix[idx, 1])
                            table.ix[21, i] = self.head.ix[5, i]
                        else:
                            table.ix[20, i] = 0
                    else:
                        weight = 0
                        table.ix[20, i] = 0
                        table.ix[21, i] = np.array(asmpt1.ix[idx, 1])
                    
                    idx = self.basic_input['project_loc'] == asmpt1.ix[:, 0]
                    if np.sum(idx) > 0:
                        table.ix[6, i] = np.array(asmpt1.ix[idx, 1]) * weight
                        table.ix[24, i] = np.array(asmpt1.ix[idx, 1])
                    else:
                        table.ix[6, i] = 0 * weight
                        table.ix[24, i] = 0
                    
                    table.ix[8:13, i] = self.head.ix[5, i]
                    
                    if self.basic_input['pwd_fliner1']:
                        table.ix[30, i] = self.head.ix[5, i]
                    else:
                        table.ix[30, i] = 0
                elif i == 'f_prodn_liner_2':
                    if triple_liner == '':
                        weight1 = 2
                        weight3 = 0
                    else:
                        weight1 = 7
                        weight3 = 7
                    
                    if not self.basic_input['double_liner']:
                        weight2 = 0
                    else:
                        weight2 = 1
                    
                    table.ix[0:2, i] = weight1 * weight2
                    table.ix[8:13, i] = weight3
                    
                    if self.basic_input['pwd_fliner1']:
                        weight4 = 5
                    else:
                        weight4 = 0
                    
                    if self.basic_input['double_liner']:
                        weight5 = 1
                    else:
                        weight5 = 0
                    table.ix[30, i] = weight4 * weight5

                    if self.basic_input['rh_or_bh'] == 'Big Hole':
                        idx = self.basic_input['project_loc'] == asmpt1.ix[:, 'LOCATION']
                        if np.sum(idx) > 0:
                            table.ix[6, i] = np.array(asmpt1.ix[idx, 'TO']) * weight5
                            table.ix[20, i] = np.array(asmpt1.ix[idx, 'TO']) * weight5
                        else:
                            table.ix[6, i] = 0
                            table.ix[20, i] = 0
                    else:
                        table.ix[6, i] = self.head.ix[5, 'f_prodn_liner_2'] 
                        table.ix[20, i] = 0

                    if unknown_row is not True:
                        table.ix[15, i] = 0
                    else:
                        idx = self.basic_input['project_loc'] == asmpt1.ix[:, 'LOCATION']
                        if np.sum(idx) > 0:
                            table.ix[15, i] = np.array(asmpt1.ix[idx, 'TO']) * weight5
                        else:
                            table.ix[15, i] = 0
                    
                    if triple_liner == '':
                        table.ix[22, i] = 0
                    else:
                        idx = self.basic_input['project_loc'] == asmpt1.ix[:, 'LOCATION']
                        if np.sum(idx) > 0:
                            table.ix[22, i] = np.array(asmpt1.ix[idx, 'TO'])
                        else:
                            table.ix[22, i] = 0
                
            if unit_cost is not None:
                if self.basic_input['rh_or_bh'] == 'Regular Hole':
                    weight = 0
                else:
                    weight = 1
                
                if i == 'f_prodn_liner_2':
                    mask = np.ones(table.shape[0], dtype = bool)
                    mask[[0, 1, 15]] = False
                    table.ix[mask, i] *= np.array(qty)[mask] * np.array(unit_cost)[mask] * self.basic_input['forex_ph_us']
                    table.ix[0, i] *= np.array(qty)[0] * np.array(unit_cost)[0] * self.basic_input['forex_ph_us'] * weight                    
                    table.ix[1, i] *= np.array(qty)[1] * np.array(unit_cost)[1] * self.basic_input['forex_ph_us'] * weight                    
                    table.ix[15, i] *= np.array(qty)[15] * np.array(unit_cost)[15] * self.basic_input['forex_ph_us'] * weight

                    # table.ix[[0,1,15], i] *= np.array(qty)[0,1,15] * np.array(unit_cost)[0,1,15] * self.basic_input['forex_ph_us'] * weight
                else:
                    table.ix[:, i] *= qty * np.array(unit_cost) * self.basic_input['forex_ph_us']
        
        return table

    def aerated_drilling(self, asmpt, drlg_input, flat_input, unit_cost = None):
        """
        Computes the Aerated Drilling Table

        # Arguments:
            asmpt: pd.DataFrame, ADA COST Assumption Table
        """
        table = pd.DataFrame(0, index = self.aerated_drilling_index, columns = ['UNIT'] + self.head_columns)
        table.ix[:, 'UNIT'] = ['per day', 'per day', 'per move', 'per move', '/ day for 2 pax', '/ day for 4 pax', '/ day for 2 pax', '', 'per day', 'per day', 'per day', 'per day', 'per day', 'per day', '', 'per piece', 'per drum', 'per drum', 'per drum', 'each', 'each']

        for i in self.head_columns:
            if i == 'rigmove':
                table.ix[[1, 5, 8, 10, 12, 13], i] = self.head.ix[5, i]
                table.ix[4, i] = self.head.ix[5, i] - 10
            if i[0] == 'd':
                if i == 'd_surface':
                    if self.basic_input['aerated_surface']:
                        table.ix[[0, 4, 5], i] = self.head.ix[4, i]
                        table.ix[1, i] = 0

                        table.ix[15, i] = 1
                        table.ix[16, i] = asmpt.ix[1, 'd_intermediate']
                        table.ix[17, i] = asmpt.ix[2, 'd_intermediate']
                    else:
                        table.ix[1, i] = self.head.ix[4, i]
                        table.ix[[0, 4, 5], i] = 0
                        table.ix[15:17, i] = 0

                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[[8, 10, 12, 13], i] = self.head.ix[4, i]
                    else:
                        table.ix[[8, 10, 12, 13], i] = 0
                elif i == 'd_intermediate':
                    table.ix[[0, 8, 10, 12, 13], i] = self.head.ix[4, i]
                    if self.basic_input['aerated_intermediate']:
                        table.ix[[4, 5], i] = self.head.ix[4, i]
                        table.ix[15, i] = 1
                        table.ix[16, i] = asmpt.ix[1, i]
                        table.ix[17, i] = asmpt.ix[2, i]
                    else:
                        table.ix[[4, 5], i] = 0
                        table.ix[15, i] = 0
                        table.ix[16, i] = 0
                        table.ix[17, i] = 0
                elif i == 'd_prodn_casing':
                    table.ix[0, i] = self.head.ix[4, i]
                    if self.basic_input['aerated_prodn_casing']:
                        table.ix[4:6, i] = self.head.ix[4, i]
                    else:
                        table.ix[4:6, i] = 0
                    table.ix[6, i] = 1
                    table.ix[8, i] = self.head.ix[4, i]
                    table.ix[10:12, i] = self.head.ix[4, i] / 2.
                    table.ix[12:14, i] = self.head.ix[4, i]

                    if self.basic_input['aerated_prodn_casing']:
                        table.ix[15, i] = 1
                        table.ix[16, i] = asmpt.ix[1, i]
                        table.ix[17, i] = asmpt.ix[2, i]
                        table.ix[18, i] = asmpt.ix[3, i]
                    else:
                        table.ix[15:18, i] = 0

                elif i == 'd_prodn_liner_1':
                    table.ix[[0, 8, 12, 13], i] = self.head.ix[4, i]
                    table.ix[[10, 11], i] = self.head.ix[4, i] / 2.
                    if self.basic_input['aerated_prodn_liner_1']:
                        table.ix[4:6, i] = self.head.ix[4, i]
                        table.ix[15, i] = 1
                        table.ix[16, i] = asmpt.ix[1, i]
                        table.ix[18, i] = asmpt.ix[3, i]
                    else:
                        table.ix[4:6, i] = 0
                        table.ix[[15, 16, 18], i] = 0
                elif i == 'd_prodn_liner_2':
                    if not self.basic_input['double_liner']:
                        table.ix[[0, 4, 5, 8, 10, 12, 13, 16], i] = 0
                    else:
                        table.ix[[0, 4, 5, 8, 10, 12, 13], i] = drlg_input[i[2:]]
                        if self.basic_input['aerated_prodn_liner_2']:
                            table.ix[16, i] = asmpt.ix[1, i]
                            table.ix[18, i] = asmpt.ix[3, i]
                            table.ix[19, i] = 1
                            table.ix[20, i] = 2
                        else:
                            table.ix[16, i] = 0
                            table.ix[18, i] = 0
                            table.ix[19, i] = 0
                            table.ix[20, i] = 0
            elif i[0] == 'f':
                if i == 'f_surface':
                    if self.basic_input['aerated_surface']:
                        table.ix[0, i] = self.head.ix[5, i]
                        table.ix[1, i] = 0
                        table.ix[4:6, i] = self.head.ix[5, i]
                        
                    else:
                        table.ix[0, i] = 0
                        table.ix[1, i] = self.head.ix[4, 'd_surface']
                        table.ix[4:6, i] = 0

                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[6, i] = 1
                        table.ix[[8, 10, 12, 13], i] = 0
                    else:
                        table.ix[6, i] = 0
                        table.ix[[8, 10, 12, 13], i] = self.head.ix[5, 'f_surface']

                elif i == 'f_intermediate':
                    table.ix[0, i] = self.head.ix[5, i] - 2
                    table.ix[1, i] = 2
                    if self.basic_input['aerated_intermediate']:
                        table.ix[4:6, i] = self.head.ix[5, i]
                    else:
                        table.ix[4:6, i] = 0

                    table.ix[[8, 10, 12, 13], i] = self.head.ix[5, i]

                elif i == 'f_prodn_casing':
                    table.ix[[0, 8, 10, 12, 13], i] = self.head.ix[5, i]
                    if self.basic_input['aerated_prodn_casing']:
                        table.ix[4:6, i] = self.head.ix[5, 'f_prodn_casing']
                    else:
                        table.ix[4:6, i] = 0

                elif i == 'f_prodn_liner_1':
                    table.ix[[0, 8, 10, 12, 13], i] = self.head.ix[5, i]

                    if self.basic_input['aerated_prodn_liner_1']:
                        if self.basic_input['double_liner']:
                            table.ix[4, i] = self.head.ix[5, i]
                        else:
                            table.ix[4, i] = 3
                        table.ix[5, i] = self.head.ix[5, i]
                    else:
                        table.ix[4:5, i] = 0
                elif i == 'f_prodn_liner_2':
                    if not self.basic_input['double_liner']:
                        table.ix[[0, 4, 5, 8, 10, 12, 13], i] = 0
                    else:
                        table.ix[[0, 4, 5, 8, 10, 12, 13], i] = flat_input[i[2:]]                    

            if unit_cost is not None:
                mask = table.index.isin(table.index.values[4:7])
                table.ix[~mask, i] *= np.array(unit_cost)[~mask] * self.basic_input['forex_ph_us']
                table.ix[[4, 6], i] *= np.array(unit_cost)[[4, 6]] * (self.basic_input['forex_ph_us'] * 2.)
                table.ix[5, i] *= np.array(unit_cost)[5] * (self.basic_input['forex_ph_us'] * 4.)

        return table

    def mud_engineering(self, qty = 2, unit_cost = None):
        """
        Computes Mud Engineering Table

        # Arguments
            asmpt: pandas.DataFrame, the same asmpt with that of MUD ENGINEERING table
        """
        table = pd.DataFrame(0, index = ['MUD ENGINEER'], columns = ['QTY'] + self.head_columns)
        table.ix[:, 'QTY'] = qty
        for i in self.head_columns:
            if i == 'rigmove':
                if self.basic_input['rig_move_days'] == 0:
                    table.ix[0, i] = 0
                else:
                    table.ix[0, i] = 3
            
            elif i[0] == 'd':
                if i == 'd_surface':
                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[0, i] = self.head.ix[4, i]
                    else:
                        table.ix[0, i] = 0
                elif i == 'd_intermediate':
                    table.ix[0, i] = self.head.ix[4, i]
                elif i == 'd_prodn_casing':
                    table.ix[0, i] = self.head.ix[4, i]
                elif i == 'd_prodn_liner_1':
                    table.ix[0, i] = self.head.ix[4, i]
                elif i == 'd_prodn_liner_2':
                    if not self.basic_input['double_liner']:
                        table.ix[0, i] = 0
                    else:
                        table.ix[0, i] =self.head.ix[4, i]
                else:
                    raise ValueError('No column name %s' % i)

            elif i[0] == 'f':
                if i == 'f_surface':
                    if not self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[0, i] = 0
                    else:
                        table.ix[0, i] = self.head.ix[5, i]
                elif i == 'f_intermediate':
                    table.ix[0, i] = self.head.ix[5, i]
                elif i == 'f_prodn_casing':
                    table.ix[0, i] = self.head.ix[5, i]
                elif i == 'f_prodn_liner_1':
                    if self.basic_input['double_liner']:
                        table.ix[0, i] = self.head.ix[5, i]
                    else:
                        table.ix[0, i] = 5
                elif i == 'f_prodn_liner_2':
                    if not self.basic_input['double_liner']:
                        table.ix[0, i] = 0
                    else:
                        table.ix[0, i] = 5
                else:
                    raise ValueError('No column name %s' % i)

            if unit_cost is not None:
                    table.ix[:, i] *= (unit_cost * self.basic_input['forex_ph_us'] * table.ix[:, 'QTY'])

        return table

    def casing_running(self, unit_cost = None):
        """
        Casing Running Table

        # Arguments
            asmpt: pandas.DataFrame, the same asmpt with that of MUD ENGINEERING table
        """
        table = pd.DataFrame(0, index = ['RUNNING SERVICE'], columns = ['UNIT'] + self.head_columns)

        for i in ['UNIT'] + self.head_columns:
            if i == 'rigmove':
                table.ix[:, i] = self.basic_input['rig_move_days']

            if i[0] == 'd':
                if i == 'd_surface':
                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[:, i] = self.head.ix[4, i]
                    else:
                        table.ix[:, i] = 0
                elif i == 'd_intermediate':
                    table.ix[:, i] = self.head.ix[4, i]
                elif i == 'd_prodn_casing':
                    table.ix[:, i] = self.head.ix[4, i]
                elif i == 'd_prodn_liner_1':
                    table.ix[:, i] = self.head.ix[4, i]
                elif i == 'd_prodn_liner_2':
                    if self.basic_input['double_liner']:
                        table.ix[:, i] = self.head.ix[4, i]
                    else:
                        table.ix[:, i] = 0
                else:
                    raise ValueError('No column name %s' % i)

            elif i[0] == 'f':
                if i == 'f_surface':
                    if not self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[:, i] = 0
                    else:
                        table.ix[:, i] = self.head.ix[5, i]
                elif i == 'f_intermediate':
                    table.ix[:, i] = self.head.ix[5, i]
                elif i == 'f_prodn_casing':
                    table.ix[:, i] = self.head.ix[5, i]
                elif i == 'f_prodn_liner_1':
                    table.ix[:, i] = self.head.ix[5, i]
                elif i == 'f_prodn_liner_2':
                    if self.basic_input['double_liner']:
                        table.ix[:, i] = self.head.ix[5, i]
                    else:
                        table.ix[:, i] = 0
                else:
                    raise ValueError('No column name %s' % i)

            if unit_cost is not None:
                if i != 'UNIT':
                    table.ix[:, i] *= (unit_cost * self.basic_input['forex_ph_us'])

        return table

    def completion_test(self, unit_cost = None):
        table = pd.DataFrame(0, index = ['Wireline + Survey', 'DHV'], columns = ['UNIT'] + self.head_columns)

        for i in ['UNIT'] + self.head_columns:
            if i == 'UNIT':
                table.ix[:, i] = 'lot'
            elif i == 'f_prodn_liner_1':
                if self.basic_input['double_liner']:
                    table.ix[0, i] = 0.
                    weight1 = 0.
                else:
                    table.ix[0, i] = 1.
                    weight1 = 1.
                
                if self.basic_input['dhv_1']:
                    weight2 = self.basic_input['dhv_2']
                else:
                    weight2 = 0
                
                if self.basic_input['reline']:
                    weight3 = 0
                else:
                    weight3 = 1
                
                table.ix[1, i] = weight1 * weight2 * weight3
            elif i == 'f_prodn_liner_2':
                if self.basic_input['double_liner']:
                    table.ix[0, i] = 1
                    weight1 = 1
                else:
                    table.ix[0, i] = 0
                    weight1 = 0
                
                if self.basic_input['dhv_1']:
                    weight2 = self.basic_input['dhv_2']
                else:
                    weight2 = 0
                
                table.ix[1, i] = weight1 * weight2
            if unit_cost is not None:
                if i != 'UNIT':
                    table.ix[:, i] *= unit_cost

        return table

    def other_cementing_services(self, asmpt, unit_cost = None):
        """
        Computes the Other Cementing Services

        # Arguments
            asmpt: Cement Additives Table
        """
        table = pd.DataFrame(0, index = ['CEMENT CUTTERS'], columns = ['UNIT'] + self.head_columns)

        for i in ['UNIT'] + self.head_columns:
            if i == 'UNIT':
                table.ix[:, i] = 'sacks'
            else:
                if i[0] == 'd':
                    if i == 'd_surface':
                        if self.basic_input['yes_if_without_pre-installed_csg']:
                            table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                        else:
                            table.ix[:, i] = 0

                    elif i == 'd_intermediate':
                        table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                    elif i == 'd_prodn_casing':
                        table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                    elif i == 'd_prodn_liner_1':
                        table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                    elif i == 'd_prodn_liner_2':
                        table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                elif i[0] == 'f':
                    if i == 'f_surface':
                        if self.basic_input['yes_if_without_pre-installed_csg']:
                            table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                        else:
                            table.ix[:, i] = 0

                    elif i == 'f_intermediate':
                        table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                    elif i == 'f_prodn_casing':
                        table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                    elif i == 'f_prodn_liner_1':
                        table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
                    elif i == 'f_prodn_liner_2':
                        table.ix[:, i] = self.roundup(asmpt.ix['Cement', i] * 1.2, 1)
            if unit_cost is not None:
                if i[0] == 'd':
                    if i == 'd_surface':
                        table.ix[:, i] *= unit_cost
                    else:
                        table.ix[:, i] *= 0
                elif i[0] == 'f':
                    if i == 'f_prodn_liner_2':
                        table.ix[:, i] *= 0
                    else:
                        table.ix[:, i] *= unit_cost

        return table

    def drill_pipes(self, drlg_input, flat_input, qty, unit_cost = None):
        table = pd.DataFrame(0, index = self.drill_pipes_index, columns = ['RATE'] + self.head_columns)
        table.ix[:, 'RATE'] = ['joint / day', 'per joint', 'per import', 'per/ truck']

        for i in self.head_columns:
            if i == 'rigmove':
                table.ix[0, i] = self.head.ix[5, i]
            else:
                if i[0] == 'd':
                    if i == 'd_surface':
                        table.ix[0, i] = self.head.ix[4, i]
                    elif i == 'd_intermediate':
                        table.ix[0, i] = self.head.ix[4, i]
                    elif i == 'd_prodn_casing':
                        table.ix[0, i] = self.head.ix[4, i]
                        table.ix[2:4, i] = qty[2:4]
                    elif i == 'd_prodn_liner_1':
                        table.ix[0, i] = self.head.ix[4, i]
                    elif i == 'd_prodn_liner_2':
                        table.ix[0, i] = drlg_input[i[2:]]

                elif i[0] == 'f':
                    if i == 'f_surface':
                        table.ix[0, i] = self.head.ix[5, i]
                    elif i == 'f_intermediate':
                        table.ix[0, i] = self.head.ix[5, i]
                    elif i == 'f_prodn_casing':
                        table.ix[0, i] = self.head.ix[5, i]
                    elif i == 'f_prodn_liner_1':
                        table.ix[0, i] = self.head.ix[5, i]
                        if self.basic_input['double_liner']:
                            table.ix[1, i] = 0
                        else:
                            table.ix[1, i] = qty[1]
                    elif i == 'f_prodn_liner_2':
                        table.ix[0, i] = flat_input[i[2:]]
                        if self.basic_input['double_liner']:
                            table.ix[1, i] = qty[1]
                        else:
                            table.ix[1, i] = 0

            if unit_cost is not None:
                table.ix[0, i] *= np.array(unit_cost)[0] * qty[0] * self.basic_input['forex_ph_us']                                                        
                table.ix[1, i] *= np.array(unit_cost)[1] * self.basic_input['forex_ph_us']                                        
                table.ix[2:4, i] *= np.array(unit_cost)[2:4] * self.basic_input['forex_ph_us']                                        

                # if i == 'f_prodn_liner_2':
                #     weight1 = np.array(unit_cost)[1] * self.basic_input['forex_ph_us']                                        
                #     table.ix[1, i] *= weight
                # else:
                #     weight = np.array(unit_cost) * qty * self.basic_input['forex_ph_us']                    
                #     table.ix[:, i] *= weight

        return table

    # revisit code
    def drilling_rig_services(self, drlg_input, flat_input, unit_cost, last_col = ''):
        """
        Computes the Drilling Rig Services

        # Arguments
            unit_cost: is the rate
        """
        table = pd.DataFrame(0, index = self.drilling_rig_services_index, columns = ['RATE'] + self.head_columns)
        table.ix[:, 'RATE'] = unit_cost

        for i in self.head_columns:
            if i == 'rigmove':
                table.ix[0, i] = table.ix[0, 'RATE']
                if self.basic_input['rig'] == 'Rig 1' or self.basic_input['rig'] == 'Rig 2':
                    table.ix[1, i] = 13 * self.asmpt[5]['Base Day Rate']
                else:
                    table.ix[1, i] = 0
                table.ix[4, i] = self.head.ix[5, i] * table.ix[4, 'RATE']
                table.ix[8, i] = self.head.ix[5, i] * table.ix[8, 'RATE']
            else:
                if i[0] == 'd':
                    if i == 'd_surface':
                        if self.basic_input['yes_if_without_pre-installed_csg']:
                            weight = 1
                        else:
                            weight = 0
                        table.ix[2, i] = self.head.ix[4, i] * table.ix[2, 'RATE'] * weight
                        table.ix[4, i] = self.head.ix[4, i] * table.ix[4, 'RATE'] * weight
                        table.ix[8, i] = self.head.ix[4, i] * table.ix[8, 'RATE'] * weight
                    elif i == 'd_intermediate':
                        table.ix[2, i] = self.head.ix[4, i] * table.ix[2, 'RATE']
                        table.ix[4, i] = self.head.ix[4, i] * table.ix[4, 'RATE']
                        table.ix[8, i] = self.head.ix[4, i] * table.ix[8, 'RATE']
                    elif i == 'd_prodn_casing':
                        table.ix[2, i] = self.head.ix[4, i] * table.ix[2, 'RATE']
                        table.ix[4, i] = self.head.ix[4, i] * table.ix[4, 'RATE']
                        table.ix[8, i] = self.head.ix[4, i] * table.ix[8, 'RATE']
                    elif i == 'd_prodn_liner_1':
                        table.ix[2, i] = self.head.ix[4, i] * table.ix[2, 'RATE']
                        table.ix[4, i] = self.head.ix[4, i] * table.ix[4, 'RATE']
                        table.ix[8, i] = self.head.ix[4, i] * table.ix[8, 'RATE']
                    elif i == 'd_prodn_liner_2':
                        table.ix[2, i] = drlg_input[i[2:]] * table.ix[2, 'RATE']
                        table.ix[4, i] = drlg_input[i[2:]] * table.ix[4, 'RATE']
                        table.ix[8, i] = drlg_input[i[2:]] * table.ix[8, 'RATE']
                if i[0] == 'f':
                    if i == 'f_surface':
                        if self.basic_input['yes_if_without_pre-installed_csg']:
                            table.ix[2, i] = self.head.ix[5, i] * table.ix[2, 'RATE']
                            table.ix[4, i] = self.head.ix[5, i] * table.ix[4, 'RATE']
                            table.ix[8, i] = self.head.ix[5, i] * table.ix[8, 'RATE']
                        else:
                            table.ix[2, i] = 0
                            table.ix[4, i] = 0
                            table.ix[8, i] = 0
                    elif i == 'f_intermediate':
                        table.ix[2, i] = self.head.ix[5, i] * table.ix[2, 'RATE']
                        table.ix[4, i] = self.head.ix[5, i] * table.ix[4, 'RATE']
                        table.ix[8, i] = self.head.ix[5, i] * table.ix[8, 'RATE']
                    elif i == 'f_prodn_casing':
                        table.ix[2, i] = self.head.ix[5, i] * table.ix[2, 'RATE']
                        table.ix[4, i] = self.head.ix[5, i] * table.ix[4, 'RATE']
                        table.ix[8, i] = self.head.ix[5, i] * table.ix[8, 'RATE']
                    elif i == 'f_prodn_liner_1':
                        if last_col == '':
                            table.ix[2, i] = self.head.ix[5, i] * table.ix[2, 'RATE']
                        else:
                            if self.basic_input['double_liner']:
                                table.ix[2, i] = self.head.ix[5, i]
                            else:
                                table.ix[2, i] = (self.head.ix[5, i] - 4) * table.ix[2, 'RATE']

                        table.ix[4, i] = self.head.ix[5, i] * table.ix[4, 'RATE']
                        if self.basic_input['double_liner']:
                            table.ix[5, i] = 0
                            table.ix[6, i] = 0
                            table.ix[9, i] = 0
                        else:
                            table.ix[5, i] = table.ix[5, 'RATE']
                            first_term = self.basic_input['drilling_row_total']['surface'] + self.basic_input['drilling_row_total']['prodn_casing'] + self.basic_input['drilling_row_total']['intermediate']
                            table.ix[6, i] = (first_term + 3) * (table.ix[6, 'RATE'] - table.ix[2, 'RATE'])
                            table.ix[9, i] = table.ix[9, 'RATE']

                        table.ix[8, i] = self.head.ix[5, i] * table.ix[8, 'RATE']
                    elif i == 'f_prodn_liner_2':
                        if self.basic_input['double_liner']:
                            table.ix[2, i] = np.nansum([flat_input[i[2:]], - 3]) * table.ix[2, 'RATE'] 
                            table.ix[3, i] = 4 * table.ix[3, 'RATE']
                            table.ix[4, i] = flat_input[i[2:]] * table.ix[4, 'RATE'] 
                            table.ix[5, i] = table.ix[5, 'RATE']
                            table.ix[6, i] = np.nansum(self.basic_input['drilling_row_total'].values() + [-3]) * (table.ix[6, 'RATE'] - table.ix[2, 'RATE'])
                            # print (table.ix[6, 'RATE'] - table.ix[2, 'RATE'])
                            # print table.ix[:, 'RATE']
                            # print table.ix[6, 'RATE']
                            # print table.ix[2, 'RATE']
                            table.ix[8, i] = flat_input[i[2:]] * table.ix[8, 'RATE'] 
                            table.ix[9, i] = table.ix[9, 'RATE']
                        else:
                            table.ix[2, i] = 0
                            table.ix[3, i] = 0
                            table.ix[4, i] = 0
                            table.ix[5, i] = 0
                            table.ix[6, i] = 0
                            table.ix[8, i] = 0
                            table.ix[9, i] = 0
        return table

    def chf_installation(self, unit_cost = None):
        table = pd.DataFrame(0, index = self.chf_installation_index, columns = ['UNIT'] + self.head_columns)
        table.ix[:, 'UNIT'] =  ['lump sum', 'lump sum', 'lump sum', 'per day', 'per day', 'per day', 'per day', 'per day', 'lump sum']

        for i in self.head_columns:
            if i == 'd_intermediate':
                table.ix[[4, 5, 7], i] = 7
            elif i == 'f_intermediate':
                table.ix[[0, 1, 2, 8], i] = 1
                table.ix[3, i] = 7

            if unit_cost is not None:
                table.ix[:, i] *= unit_cost

        return table

    def jars_shock(self, asmpt, drlg_input, triple_liner = '', unit_cost = None, qty = [1, 3, 3, 0, 0, 7]):
        table = pd.DataFrame(0, index = self.jars_shock_index, columns = ['UNIT'] + self.head_columns)
        table.ix[:, 'UNIT'] = ['per day', 'per day', 'per day', 'per day', 'per day', 'per job']

        for i in self.head_columns:
            if i == 'rigmove':
                table.ix[0:4, i] = self.head.ix[5, i]
            else:
                if i[0] == 'd':
                    if i == 'd_surface':
                        table.ix[0:5, i] = self.head.ix[4, i]
                    elif i == 'd_intermediate':
                        table.ix[0:5, i] = self.head.ix[4, i]
                    elif i == 'd_prodn_casing':
                        table.ix[0:5, i] = self.head.ix[4, i]
                    elif i == 'd_prodn_liner_1':
                        table.ix[0:5, i] = self.head.ix[4, i]
                        if self.basic_input['double_liner']:
                            table.ix[5, i] = 0
                        else:
                            table.ix[5, i] = 3
                    elif i == 'd_prodn_liner_2':
                        if self.basic_input['double_liner']:
                            table.ix[0:5, i] = drlg_input[i[2:]]
                            table.ix[5, i] = 3
                        else:
                            table.ix[0:5, i] = 0
                            table.ix[5, i] = 0
                        
                elif i[0] == 'f':
                    if i == 'f_surface':
                        table.ix[0:5, i] = self.head.ix[5, i]
                    elif i == 'f_intermediate':
                        table.ix[0:5, i] = self.head.ix[5, i]
                    elif i == 'f_prodn_casing':
                        table.ix[0:5, i] = self.head.ix[5, i]
                    elif i == 'f_prodn_liner_1':
                        if self.basic_input['rh_or_bh'] == 'Regular Hole':
                            idx = self.basic_input['project_loc'] == asmpt.ix[:, 'LOCATION']
                            if np.sum(idx) > 0:
                                table.ix[0:5, i] = np.array(asmpt.ix[idx, 'FROM'])
                            else:
                                table.ix[0:5, i] = 0
                        else:
                            table.ix[0:5, i] = self.head.ix[5, i]

                    elif i == 'f_prodn_liner_2':
                        if triple_liner == '':
                            weight = 1
                        else:
                            weight = 0
                        if self.basic_input['double_liner']:
                            idx = self.basic_input['project_loc'] == asmpt.ix[:, 'LOCATION']
                            if np.sum(idx) > 0:
                                table.ix[0:5, i] = np.array(asmpt.ix[idx, 'FROM']) * weight
                            else:
                                table.ix[0:5, i] = 0
                        else:
                            table.ix[0:5, i] = 0

            if unit_cost is not None:
                g_weight = np.array(unit_cost) * qty * self.basic_input['forex_ph_us'] 
                if i == 'd_surface':    
                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        weight = np.array(unit_cost)[[0, 2, 3, 4, 5]] * np.array(qty)[[0, 2, 3, 4, 5]] * self.basic_input['forex_ph_us'] 
                    else:
                        weight = 0
                    
                    table.ix[1, i] *= g_weight[1]
                    table.ix[[0, 2, 3, 4, 5], i] *= weight
                elif i == 'f_surface':
                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        weight = np.array(unit_cost)[[0, 3, 4, 5]] * np.array(qty)[[0, 3, 4, 5]] * self.basic_input['forex_ph_us'] 
                    else:
                        weight = 0
                    
                    table.ix[[1, 2], i] *= g_weight[[1, 2]]
                    table.ix[[0, 3, 4, 5], i] *= weight                
                else:
                    table.ix[:, i] *= g_weight
            
        return table

    def mud_logging(self, drlg_input, flat_input, unit_cost = None):
        table = pd.DataFrame(0, index = self.mud_logging_index, columns = ['UNIT'] + self.head_columns)
        table.ix[:, 'UNIT'] = ['lump sum', 'lump sum']

        for i in self.head_columns:
            if i == 'rigmove':
                if self.basic_input['mud_logging']:
                    weight1 = 2
                else:
                    weight1 = 0

                if self.head.ix[5, i] != 0:
                    weight2 = 1
                else:
                    weight2 = 0

                table.ix[0, i] = weight1 * weight2

                if self.basic_input['mud_logging']:
                    table.ix[1, i] = self.head.ix[5, i] - table.ix[0, i]
                else:
                    table.ix[1, i] = 0
            else:
                if i[0] == 'd':
                    if i == 'd_surface':
                        if self.basic_input['mud_logging']:
                            if self.basic_input['yes_if_without_pre-installed_csg']:
                                table.ix[0, i] = self.head.ix[4, i]
                            else:
                                table.ix[0, i] = 0
                    else:
                        if i == 'd_prodn_liner_2':
                            if self.basic_input['mud_logging']:
                                if self.basic_input['double_liner']:
                                    table.ix[0, i] = drlg_input[i[2:]]
                                else:
                                    table.ix[0, i] = 0
                            else:
                                table.ix[0, i] = 0
                        else:
                            if self.basic_input['mud_logging']:
                                table.ix[0, i] = self.head.ix[4, i]
                            else:
                                table.ix[0, i] = 0
                    
                elif i[0] == 'f':
                    if i == 'f_surface':
                        if self.basic_input['mud_logging']:
                            if self.basic_input['yes_if_without_pre-installed_csg']:
                                table.ix[0, i] = self.head.ix[5, i]
                            else:
                                table.ix[0, i] = 0
                    else:
                        if i == 'f_prodn_liner_2':
                            if self.basic_input['mud_logging']:
                                if self.basic_input['double_liner']:
                                    table.ix[0, i] = flat_input[i[2:]]
                                else:
                                    table.ix[0, i] = 0
                            else:
                                table.ix[0, i] = 0
                        else:
                            if self.basic_input['mud_logging']:
                                table.ix[0, i] = self.head.ix[5, i]
                            else:
                                table.ix[0, i] = 0

            if unit_cost is not None:
                table.ix[:, i] *= np.array(unit_cost) * self.basic_input['forex_ph_us']

        return table
    
    def handling(self, drlg_input, flat_input, asmpt1):
        """
        Computes the Handling and Hauling table

        # Arguments:
            asmpt1: float, total from the transhipment cost table
        """
        table = pd.DataFrame(0, index = ['Handling, Hauling, Towing & Del.'], columns = self.head_columns)
        for i in self.head_columns:
            #if i == 'rigmove':
            #    table.ix[0, i] = 0
            if i[0] == 'd':
                if i == 'd_prodn_liner_2':
                    table.ix[0, i] = (asmpt1 / float(self.basic_input['total_days'])) * drlg_input[i[2:]]
                else:
                    table.ix[0, i] = (asmpt1 / float(self.basic_input['total_days'])) * self.head.ix[4, i]
            elif i[0] == 'f' or i == 'rigmove':
                if i == 'f_prodn_liner_2':
                    table.ix[0, i] = (asmpt1 / float(self.basic_input['total_days'])) * flat_input[i[2:]]
                else:
                    table.ix[0, i] = (asmpt1 / float(self.basic_input['total_days'])) * self.head.ix[5, i]
        
        return table

    def transhipment_cost(self, asmpt1, asmpt2):
        """
        Computes the Transhipment Cost Table

        # Arguments:
            asmpt1: pd.DataFrame, equipment
            asmpt2: pd.DataFrame, transhipmental drill pipe
        """
        transhipment_cost_index = ['40-FT HBT (MLA-SITE/SITE-MLA)', 'EAARN', '40-FT HBT (Within SITE)-therma', 'BOOMTRUCK (Within Site)', 'FUEL TRUCK (Within Site)', 'Transshipment of SLB Cementing Package', 'Duties', 'Transshipment Drillpipes', 'Handling/Hauling (Allocated)']
        table = pd.DataFrame(0, index = transhipment_cost_index, columns = ['TOTAL # OF TRIPS', 'Hr', 'UNIT COST', 'TOTAL'])

        table.ix[0:3, 'TOTAL # OF TRIPS'] = 11
        table.ix[3:5, 'TOTAL # OF TRIPS'] = self.basic_input['total_days']
        table.ix[5:7, 'TOTAL # OF TRIPS'] = 1

        if self.basic_input['rent_drill_pipes']:
            if self.basic_input['mob/demob_drillpipes'] == 'WITHIN SITE':
                table.ix[7, 'TOTAL # OF TRIPS'] = self.roundup(self.basic_input['no_of_Joints'] / 70., 1) * 2
            else:
                table.ix[7, 'TOTAL # OF TRIPS'] = 0
        else:
            table.ix[7, 'TOTAL # OF TRIPS'] = 0
        
        table.ix[8, 'TOTAL # OF TRIPS'] = self.basic_input['total_days']
        table.ix[3:5, 'Hr'] = 8
        table.ix[0, 'UNIT COST'] = 135000
        table.ix[1, 'UNIT COST'] = 4000

        idx = self.basic_input['project_loc'] == asmpt1.index
        if np.sum(idx) > 0:
            table.ix[2, 'UNIT COST'] = np.array(asmpt1.ix[idx, '40ft HBT'])
        else:
            table.ix[2, 'UNIT COST'] = 0
        
        table.ix[3, 'UNIT COST'] = 750
        table.ix[4, 'UNIT COST'] = 448
        table.ix[5, 'UNIT COST'] = 0
        table.ix[6, 'UNIT COST'] = 100000
        
        if self.basic_input['mob/demob_drillpipes'] == 'WITHIN SITE':
            weight1 = np.array(asmpt2.ix[0, 'TRUCK RATE'])
        else:
            weight1 = 0

        if self.basic_input['rent_drill_pipes']:
            weight2 = 1
        else:
            weight2 = 0
    
        table.ix[7, 'UNIT COST'] = weight1 * weight2
        
        table.ix[[0, 1, 2, 4, 5, 6, 7, 8], 'TOTAL'] = table.ix[[0, 1, 2, 4, 5, 6, 7, 8], 'TOTAL # OF TRIPS'] * table.ix[[0, 1, 2, 4, 5, 6, 7, 8], 'UNIT COST']
        table.ix[3, 'TOTAL'] = table.ix[3, 'TOTAL # OF TRIPS'] * table.ix[3, 'UNIT COST'] * table.ix[3, 'Hr']

        return table

    def rig_mobilization(self, asmpt1, asmpt2, asmpt3, asmpt4, asmpt5 = 0, total = False, unit_cost = None, rig_14_cost = 15355322.00, qty = np.append(np.append(np.repeat(1, 10), 2), 0)):
        """
        Computed the Rig Mobilization Charges Table 

        # Arguments
            asmpt1 - pandas.DataFrame, Rigmove Data
            asmpt2 - pandas.DataFrame, Equipment Data
            asmpt3 - pandas.DataFrame, rigmove_cost
            asmpt4 - pandas.DataFrame, drilling_rig_services rigmove total
            asmpt5 - row X781 of cost details
        """
        table = pd.DataFrame(0, index = self.rig_mobilization_index, columns = ['NO OF HRS/TRIPS'] + self.head_columns)
        
        if self.basic_input['aerated_surface']:
            weight1 = 9
            weight2 = 6
        else:
            weight1 = 0
            weight2 = 0

        if self.basic_input['pwd_fliner2']:
            weight2 = 6
            weight3 = 5
            weight4 = 1
        else:
            weight2 = 0
            weight3 = 0
            weight4 = 0

        if asmpt5 == 0:
            weight5 = 0
        else:
            weight5 = 1

        table.ix[0, 'NO OF HRS/TRIPS'] = asmpt1.ix[0, 2 + np.where(asmpt1.ix[:, 2:].columns.values == self.basic_input['rig'].upper())[0][0]] + weight1 + weight2
        table.ix[1, 'NO OF HRS/TRIPS'] = asmpt1.ix[1, 2 + np.where(asmpt1.ix[:, 2:].columns.values == self.basic_input['rig'].upper())[0][0]] + weight3
        table.ix[2, 'NO OF HRS/TRIPS'] = asmpt1.ix[2, 2 + np.where(asmpt1.ix[:, 2:].columns.values == self.basic_input['rig'].upper())[0][0]] + weight4 + 5
        
        for i in np.arange(3, 6):
            table.ix[i, 'NO OF HRS/TRIPS'] = asmpt2.ix[asmpt2.index.values == table.index.values[i], 4][0]

        for i in np.arange(6, 10):
            table.ix[i, 'NO OF HRS/TRIPS'] = asmpt1.ix[i, 2 + np.where(asmpt1.ix[:, 2:].columns.values == self.basic_input['rig'].upper())[0][0]]
        
        if self.basic_input['project_loc'] != 'BGBU':
            table.ix[10, 'NO OF HRS/TRIPS'] = 11
        else:
            table.ix[10, 'NO OF HRS/TRIPS'] = 0

        for i in self.head_columns:
            if i == 'rigmove':
                if self.head.ix[5, i] != 0:
                    weight = 1
                else:
                    weight = 0

                table.ix[1, i] = 1
                if self.basic_input['rig'] == 'Rig 1' or self.basic_input['rig'] == 'Rig 2':
                    table.ix[[0, 7, 8, 9, 10], i] = 0 * weight
                    table.ix[2, i] = 0 * weight5
                    table.ix[3:7, i] = 0
                else:
                    table.ix[[0, 7, 8, 9, 10], i] = 1 * weight
                    table.ix[2, i] = 1 * weight5
                    table.ix[3:7, i] = self.head.ix[5, i]

            if unit_cost is not None:
                table.ix[:, i] *= np.array(unit_cost) * qty * table.ix[:, 'NO OF HRS/TRIPS']
        
        if total is not True:            
            return table
        else:
            if self.basic_input['rig_move_days'] == 0:
                weight_r = 0
            else:
                weight_r = 1

            if self.basic_input['rig'] == 'Rig 1' and self.basic_input['interisland_rig_move'] is False:
                return 0 + asmpt4 * weight_r
            else:
                if self.basic_input['rig'] == 'Rig 2' and self.basic_input['interisland_rig_move'] is False:
                    return 0 + asmpt4 * weight_r
                else:
                    if self.basic_input['rig'] == 'Rig 14':
                        return np.array(asmpt3.ix[5, 'TOTAL'] + asmpt4 * weight_r).flatten()[0]
                    else:
                        if self.basic_input['interisland_rig_move'] is False:
                            return np.array(table.ix[:, 'rigmove'].sum() + asmpt4 * weight_r).flatten()[0]
                        else:
                            idx = self.basic_input['interisland_rig_move'] == asmpt3.ix[:, 0]
                            if np.sum(idx) > 0:
                                return np.array(asmpt3.ix[idx, 4] + asmpt4 * weight_r).flatten()[0]
                            else:
                                return 0 + asmpt4 * weight_r

    def equipment_rental(self, asmpt1, asmpt2, drlg_input, flat_input, unit_cost = None, freq = ['HOURLY', 'HOURLY', 'HOURLY', 'DAILY', 'DAILY', 'HOURLY', 'DAILY'], qty = [1, 1, 0, 0, 2, 2, 1]):
        """
        Computes the Equipment Rental Table

        # Argument:
            asmpt1:     pd.DataFrame, Equipment Data 1
            asmpt2:     pd.DataFrame, Equipment Data 2
            unit_cost: np.array, a list of rate or cost of the equipments
            freq:      np.array, a list of frequency.
        """
        table = pd.DataFrame(0, index = self.equipment_rental_index, columns = ['NO. OF HRS'] + self.head_columns)
        for i in self.equipment_rental_index:
            if i != 'BOOM TRUCK':
                idx = i == asmpt2.ix[:, 'Equipment Rental']
                col = 'HR ' + self.basic_input['project_loc'] == asmpt2.columns
                noh = np.array(asmpt2.ix[idx, col]).flatten()[0]

                if self.basic_input['rig'] == 'Rig 1' or self.basic_input['rig'] == 'Rig 2':
                    weight = 0
                else:
                    weight = 1
                
                table.ix[i, 'NO. OF HRS'] = noh * weight
            else:
                table.ix[i, 'NO. OF HRS'] = 0

        for i in self.head_columns:
            if i == 'rigmove':
                table.ix[:, i] = self.head.ix[5, i]
            elif i[0] == 'd':
                if i == 'd_surface':
                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[:, i] = self.head.ix[4, i]
                    else:
                        table.ix[:, i] = 0
                elif i == 'd_prodn_liner_2':
                    if self.basic_input['double_liner']:
                        table.ix[:, i] = drlg_input[i[2:]]
                    else:
                        table.ix[:, i] = 0
                else:
                    table.ix[:, i] = self.head.ix[4, i]
                
            elif i[0] == 'f':
                if i == 'f_surface':
                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[:, i] = self.head.ix[5, i]
                    else:
                        table.ix[:, i] = 0
                elif i == 'f_prodn_liner_2':
                    if self.basic_input['double_liner']:
                        table.ix[:, i] = flat_input[i[2:]]
                    else:
                        table.ix[:, i] = 0
                else:
                    table.ix[:, i] = self.head.ix[5, i] 
            if unit_cost is not None:
                if i == 'rigmove':
                    table.ix[[0, 6], i] = 0
                    if freq is not None:
                        for j in np.arange(1, 6):
                            if freq[j] == 'HOURLY':
                                if j > 2:
                                    table.ix[j, i] *= 24 * unit_cost[j] * table.ix[j, 'NO. OF HRS']
                                else:
                                    table.ix[j, i] *= np.array(asmpt1.ix[asmpt1.index == table.index.values[j], 4]).flatten()[0] * unit_cost[j] * table.ix[j, 'NO. OF HRS']
                            else:
                                if j > 2:
                                    table.ix[j, i] *= unit_cost[j] * table.ix[j, 'NO. OF HRS']
                                else:
                                    table.ix[j, i] *= unit_cost[j] * table.ix[j, 'NO. OF HRS']
                        
                    else:
                        raise ValueError('Specifying unit_cost must also specify freq.')
                else:
                    table.ix[:, i] *= np.array(unit_cost) * np.array(qty) * table.ix[:, 'NO. OF HRS']
                
        return table

    def rig_allocated(self, asmpt1, asmpt2, asmpt3, asmpt4, asmpt5, asmpt6, asmpt7, drlg_input, flat_input):
        """
        Computes Rig Allocated Table

        # Arguments:
            asmpt1: pd.DataFrame, rigmove_daily table
            asmpt2: pd.DataFrame, depreciation table
            asmpt3: pd.DataFrame, insurance table
            asmpt4: pd.DataFrame, genex table
            asmpt5: pd.DataFrame, service fee table
            asmpt6: pd.DataFrame, wellname allocated cost table
            asmpt7: pd.DataFrame, inter-island cost table
        """
        table = pd.DataFrame(0, index = self.rig_allocated_index, columns = ['RATE'] + self.head_columns)

        idx1 = self.basic_input['rig'].upper() == asmpt1.ix[:, 0]
        idx2 = self.basic_input['rig'].upper() == asmpt2.ix[:, 0]
        idx3 = self.basic_input['rig'].upper() == asmpt3.ix[:, 0]
        idx4 = self.basic_input['project_loc'].upper() == asmpt4.ix[:, 0]
        
        if np.sum(idx1) > 0:
            table.ix[0, 'RATE'] = np.array(asmpt1.ix[idx1, 1])
        else:
            table.ix[0, 'RATE'] = 0

        if np.sum(idx2) > 0:
            table.ix[1, 'RATE'] = np.array(asmpt2.ix[idx2, 1])
        else:
            table.ix[1, 'RATE'] = 0

        if np.sum(idx3) > 0:
            table.ix[2, 'RATE'] = np.array(asmpt3.ix[idx3, 1])
        else:
            table.ix[2, 'RATE'] = 0

        if np.sum(idx4) > 0:
            table.ix[3, 'RATE'] = np.array(asmpt4.ix[idx4, 1])
        else:
            table.ix[3, 'RATE'] = 0

        if self.basic_input['rig'] == 'Rig 1' or self.basic_input['rig'] == 'Rig 2':
            table.ix[4, 'RATE'] = 0
        else:
            table.ix[4, 'RATE'] = np.array(asmpt5.ix[0, 1])

        if self.basic_input['well_name'] == 'SG5D' or self.basic_input['well_name'] == 'LG7D':
            table.ix[5, 'RATE'] = np.array(asmpt6.ix[0, 1])
        else:
            table.ix[5, 'RATE'] = np.array(asmpt5.ix[1, 1])

        idx5 = self.basic_input['project_loc'] == asmpt7.ix[:, 0]
        table.ix[6, 'RATE'] = np.array(asmpt7.ix[idx5, 1])

        for i in self.head_columns:
            if i == 'rigmove':
                table.ix[:, i] = table.ix[:, 'RATE'] * self.head.ix[5, i]
            elif i[0] == 'd':
                if i == 'd_surface':
                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[:, i] = table.ix[:, 'RATE'] * self.head.ix[4, i]
                    else:
                        table.ix[:, i] = 0
                elif i == 'd_prodn_liner_2':
                    if self.basic_input['double_liner']:
                        table.ix[:, i] = table.ix[:, 'RATE'] * drlg_input[i[2:]]
                    else:
                        table.ix[:, i] = 0
                else:
                    table.ix[:, i] = table.ix[:, 'RATE'] * self.head.ix[4, i]
            elif i[0] == 'f':
                if i == 'f_surface':                    
                    if self.basic_input['yes_if_without_pre-installed_csg']:
                        table.ix[:, i] = table.ix[:, 'RATE'] * self.head.ix[5, i]
                    else:
                        table.ix[:, i] = 0
                elif i == 'f_prodn_liner_2':
                    if self.basic_input['double_liner']:
                        table.ix[:, i] = table.ix[:, 'RATE'] * flat_input[i[2:]]
                    else:
                        table.ix[:, i] = 0
                else:
                    table.ix[:, i] = table.ix[:, 'RATE'] * self.head.ix[5, i]

        return table