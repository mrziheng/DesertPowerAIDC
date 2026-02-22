import pandas as pd
import pickle
from PowerModel import opt_power
import math
import sys
import numpy as np

from utils import get_work_dir


workdir = get_work_dir()

pv = pd.read_csv(workdir+'/data/vre/desert_solar.csv')
we = pd.read_csv(workdir+'/data/vre/desert_we.csv')

pv_cf = pd.read_pickle('./data/vre/desert_solar_cfprof.pkl') #this file is too large, please contact the lead contact
we_cf = pd.read_pickle('./data/vre/desert_wind_cfprof.pkl') #this file is too large, please contact the lead contact

res = pv[['lon','lat']].copy(deep=True)
res['pv_poten'] = pv['cap_mid']
res['we_poten'] = we['cap_mid']


res['we_cap'] = -1.0
res['pv_cap'] = -1.0
res['st_cap'] = -1.0
res = res.set_index(['lon','lat'])

res_ts = {}

process_count = 10

forward = math.ceil(res.shape[0] / process_count)


def opt_wss_config_sub_process(p_count,tot_p,forward):
    if p_count == tot_p - 1:
        index_df = res.iloc[p_count*forward:,:].copy(deep=True)
    else:
        index_df = res.iloc[p_count*forward:(p_count+1)*forward,:].copy(deep=True)
    
    index_ts = {}
    
    invalid_count = 0
    
    for i,r in index_df.iterrows(): 
        opt_config = opt_power(pv_cap=1000*res.at[i,'pv_poten'],
                               pv_cf=pv_cf[i][:8760],
                               we_cap=1000*res.at[i,'we_poten'],
                               we_cf=we_cf[i][:8760])
        
        if not opt_config is None:
            index_df.at[i,'pv_cap'] = opt_config['cap']['pv']
            index_df.at[i,'we_cap'] = opt_config['cap']['we']
            index_df.at[i,'st_cap'] = opt_config['cap']['sto']
        
            index_ts[i] = opt_config['ts']
        else:
            invalid_count += 1
    
    return index_df, index_ts


if __name__ == '__main__':
    if len(sys.argv) > 1:
        idx = int(sys.argv[1])
    else:
        idx = 0
    
    df,ts = opt_wss_config_sub_process(idx,tot_p=process_count,forward=forward)
    
    df.to_csv(workdir+'data/res/WSSConfig/scen/sub/df_'+str(idx)+'.csv')
    
    with open(workdir+'data/res/WSSConfig/scen/sub/ts'+str(idx)+'.pkl','wb+') as fout:
        pickle.dump(ts,fout)
    fout.close()
    