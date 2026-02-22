import math
import multiprocessing
import os
import platform
import re
import sys
import datetime
import cv2

sys.path.append(os.path.dirname(__file__)) #this path

from multiprocessing import cpu_count

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Polygon,LineString

global cpu_worker_num
global now

cpu_worker_num = max(cpu_count(),60)
now = datetime.datetime.now()


def get_dirflag():
    flag = platform.system()
    if 'Darwin' in flag or 'Linux' in flag:
        return '/'
    else:
        return '\\'


def makedir(path):
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)

    return path+get_dirflag()


def get_crf(wacc, years):
    wacc = wacc
    crf = (wacc * math.pow(1+wacc, years)) / (math.pow(1+wacc, years)-1)

    return round(crf,6)
    

def calcu_lcoe(total_capex, storage_capex, opex, cf, years, disc_r, 
               storage_life=15, cost_decline_rate=0.03):
    # 1. Denominator: Discounted Annual Energy Production (AEP)
    # E_t = Capacity * 8760 * CF
    # Note: Assuming constant generation (degradation not included in this simplified block)
    ele_yr = cf * 8760
    denominator = sum([ele_yr / (1 + disc_r)**yr for yr in range(1, years + 1)])
    
    # 2. Numerator Part A: Initial CAPEX & OPEX
    # Initial Investment (discounted from Year 1 to allow consistency with user logic, 
    # typically Year 0 is undiscounted in standard cash flow models)
    initial_cost = total_capex / (1 + disc_r)
    opex_cost = sum([opex / (1 + disc_r)**yr for yr in range(1, years + 1)])
    
    numerator = initial_cost + opex_cost
    
    # 3. Numerator Part B: Storage Replacement Cost (C_rep)
    replacement_cost_total = 0
    last_rep_cost_future = 0 
    last_rep_year = 0        
    
    # Identify replacement years: e.g., for 25yr project, 15yr storage -> Year 15
    for r_year in range(storage_life, years, storage_life):
        # Apply cost decline curve: Cost_t = Cost_0 * (1 - decline_rate)^t
        future_capex = storage_capex * ((1 - cost_decline_rate) ** r_year)
        
        # Discount future replacement cost to Present Value (PV)
        discounted_rep_cost = future_capex / (1 + disc_r)**r_year
        replacement_cost_total += discounted_rep_cost
        
        # Track for salvage value calculation
        last_rep_cost_future = future_capex
        last_rep_year = r_year

    numerator += replacement_cost_total

    # 4. Numerator Part C: Salvage Value Recovery (V_salvage)
    salvage_value_discounted = 0
    battery_end_year = last_rep_year + storage_life
    
    # Check if storage has remaining life at project end
    if last_rep_year > 0 and battery_end_year > years:
        remaining_years = battery_end_year - years
        
        # Linear Depreciation: Value = Purchase_Price * (Remaining / Total_Life)
        salvage_value_nominal = last_rep_cost_future * (remaining_years / storage_life)
        
        # Discount salvage value from Year N to Year 0
        salvage_value_discounted = salvage_value_nominal / (1 + disc_r)**years
        
        # Subtract from total cost (Revenue/Credit)
        numerator -= salvage_value_discounted

    # 5. Final Calculation
    lcoe = numerator / denominator
    return round(lcoe, 8)


def get_work_dir():
    work_dir = os.path.abspath('./') + get_dirflag()

    return work_dir
