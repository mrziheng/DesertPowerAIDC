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
    

def calcu_lcoe(capex,opex,cf,years,disc_r):
    ele_yr = cf * 8760
    
    denominator = sum([ele_yr/(1+disc_r)**yr for yr in range(1,years+1)])
    
    numerator = capex/(1+disc_r) + sum([opex/(1+disc_r)**yr for yr in range(1,years+1)])
    
    res = round(numerator/denominator,8)
    
    return res


def get_work_dir():
    work_dir = os.path.abspath('./') + get_dirflag()

    return work_dir
