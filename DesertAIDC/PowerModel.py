import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import math

global sto_dur, time_len, char_effi, dischar_effi,wacc

#default
sto_dur = 4
char_effi = 0.95
dischar_effi = 0.95


time_len = 8760
wacc = 0.075

cap_equal = 1
cap_rsv = cap_equal * 0.05

capex_pv = 3450
capex_we = 4200
capex_st = 2000


life_pv = 25
life_we = 25
life_st = 15


def get_crf(wacc, years):
    crf = (wacc * math.pow(1+wacc, years)) / (math.pow(1+wacc, years)-1)
    return round(crf,6)



#this optimization is to determine the ratio of wind, solar, and storage for a target generation profile, investment cost here does not change the results
def opt_power(pv_cap,pv_cf,we_cap,we_cf):
    model = gp.Model()
    
    sto_cap = model.addVar(lb=0,vtype=GRB.CONTINUOUS)
    
    pv_cap_opt = model.addVar(lb=0,vtype=GRB.CONTINUOUS)
    we_cap_opt = model.addVar(lb=0,vtype=GRB.CONTINUOUS)
    
    pv_output = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    we_output = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    
    pv_rsv = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    we_rsv = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    
    sto_char = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    sto_dischar = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    
    sto_char_rsv = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    sto_dischar_rsv = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    
    sto_eng = model.addVars(time_len,lb=0,vtype=GRB.CONTINUOUS)
    
    model.setObjective(get_crf(wacc=wacc,years=life_pv) * pv_cap_opt + 
                       get_crf(wacc=wacc,years=life_we) * we_cap_opt + 
                       get_crf(wacc=wacc,years=life_st) * sto_cap +
                       0.000001 * gp.quicksum([sto_dischar[t]+sto_char[t] 
                                             for t in range(time_len)]))
    
    #model.addConstr(pv_cap_opt <= pv_cap)
    #model.addConstr(we_cap_opt <= we_cap)
    #model.addConstr(sto_eng[0] == sto_eng[time_len-1])
    
    model.addConstrs(pv_output[t] + pv_rsv[t] <= pv_cap_opt * pv_cf[t] for t in range(time_len))
    model.addConstrs(we_output[t] + we_rsv[t] <= we_cap_opt * we_cf[t] for t in range(time_len))
    
    model.addConstrs(sto_char_rsv[t] <= sto_dischar[t] for t in range(time_len))
    model.addConstrs(sto_dischar_rsv[t] + sto_dischar[t] 
                     <= dischar_effi * sto_cap for t in range(time_len))
    
    model.addConstrs(sto_dischar_rsv[t] + sto_char_rsv[t] 
                     <= dischar_effi * sto_cap for t in range(time_len))
    
    model.addConstrs(pv_output[t] + 
                     we_output[t] +
                     sto_dischar[t] 
                     == cap_equal + sto_char[t]
                     for t in range(time_len))
    
    model.addConstrs(pv_rsv[t] + 
                     we_rsv[t] +
                     sto_dischar_rsv[t] + 
                     sto_char_rsv[t] 
                     >= cap_rsv
                     for t in range(time_len))
    
    model.addConstrs(sto_eng[t] <= sto_dur * sto_cap for t in range(time_len))
    
    model.addConstrs(sto_eng[t] == sto_eng[(time_len+t-1) % time_len] + 
                                   char_effi * sto_char[t] -
                                   round(1/dischar_effi,8) * sto_dischar[t]
                                   for t in range(time_len))
    
    
    model.addConstrs(sto_char[t] <= sto_cap for t in range(time_len))
    
    model.addConstrs(round(1/dischar_effi,8) * sto_dischar[t] <= sto_cap for t in range(time_len))
    
    model.setParam('Method',2)
    model.setParam('Crossover',0)
    model.setParam('OutputFlag', 0)
            
    model.optimize()
    
    if model.Status == 2:
        res = {
            'cap':{'sto':sto_cap.x,
                   'pv':pv_cap_opt.x,
                   'we':we_cap_opt.x},
            
            'ts': {
                'sto_char':np.array([sto_char[t].x for t in range(time_len)]),
                'sto_dischar':np.array([sto_dischar[t].x for t in range(time_len)]),
                'sto_eng':np.array([sto_eng[t].x for t in range(time_len)]),
                'pv_output':np.array([pv_output[t].x for t in range(time_len)]),
                'we_output':np.array([we_output[t].x for t in range(time_len)])
            }
        }
    else:
        res = None
    
    return res