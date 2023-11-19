import xarray as xr
import pandas as pd
import numpy as np
import scipy
import os
import sys

era_dir="/g/data/e14/sm2435/ERA5/"
out_dir="/g/data/e14/sm2435/ERA5/clim/"

def load_tau(tx_files, ty_files):
    tx = xr.open_mfdataset(tx_files, parallel=True).iews
    ty = xr.open_mfdataset(ty_files, parallel=True).inss
    return tx, ty

def get_wst_comp(tx_files, ty_files):
    tx,ty = load_tau(tx_files, ty_files)
    w = np.sqrt(tx**2+ty**2)
    w = w.groupby("time.month").mean("time")
    return w

#tauu and tauv files
tauu = 'uss/*.nc'
tauv = 'vss/*.nc'

#Wstress compoenents
tauu_files = (os.path.join(era_dir,  tauu))
tauv_files = (os.path.join(era_dir,  tauv))
try:
    #calculate wspd
    w=get_wst_comp(tauu_files, tauv_files)
    #save output as netcdf file
    w.to_netcdf(os.path.join(out_dir, 'ERA5_wspd.nc'))
except Exception as e:
    print(e)
    traceback.print_exc()
    pass
sys.exit()

