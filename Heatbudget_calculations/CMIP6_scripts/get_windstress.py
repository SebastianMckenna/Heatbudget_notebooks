import xarray as xr
import dask
import numpy as np
import scipy
import os
#from HeatBudget import *
from pathlib import Path
import traceback
import xarray.ufuncs as xu
import sys

#loop to go through data folders. Do this in try except so that we know if/when somehting has failed, but the script will keep on running
CMIP_dir = '/g/data/e14/sm2435/CMIP6/CMIP6/'
outdir = '/g/data/e14/sm2435/CMIP6_HB/'

def load_tau(tx_files, ty_files):
    tx = xr.open_mfdataset(tx_files, parallel=True).tauuo
    ty = xr.open_mfdataset(ty_files, parallel=True).tauvo
    return tx, ty

def get_wst_comp(tx_files, ty_files):
    tx,ty = load_tau(tx_files, ty_files)
    tx = tx.groupby('time.month').mean('time')
    ty = ty.groupby('time.month').mean('time')
    return tx, ty

#tauu and tauv files
tauu = 'tauuo/*.nc'
tauv = 'tauvo/*.nc'

#Wstress compoenents
for model in os.listdir(CMIP_dir):
    print('start', model)
    #input file
    tauu_files = (os.path.join(CMIP_dir, model, tauu))
    tauv_files = (os.path.join(CMIP_dir, model, tauv))
    #create file output location if it doesn't exist
    out_loc = outdir+model
    Path(outdir+model).mkdir(parents=True, exist_ok=True)
    try:
        #calculate wspd
        print('load Wstress componenets')
        tu, tv =get_wst_comp(tauu_files, tauv_files)
        print('finish wstress, save output')
        #save output as netcdf file
        tu.to_netcdf(os.path.join(out_loc, str(model+'_tauu.nc')))
        tv.to_netcdf(os.path.join(out_loc, str(model+'_tauv.nc')))
        print('wstress saved to ', os.path.join(out_loc, str(model+'_tauu.nc')))
        print('wstress saved to ', os.path.join(out_loc, str(model+'_tauv.nc')))
    except Exception as e:
        print(e)
        traceback.print_exc()
        pass
sys.exit()
