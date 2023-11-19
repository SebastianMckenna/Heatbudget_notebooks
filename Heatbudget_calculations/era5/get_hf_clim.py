import xarray as xr
import pandas as pd
import numpy as np
import scipy
import os
import sys

era_dir="/g/data/e14/sm2435/ERA5/"
out_dir="/g/data/e14/sm2435/ERA5/clim/"

def load_lhf(files):
    var = xr.open_mfdataset(files, parallel=True).mslhf
    var = var.groupby('time.month').mean('time')
    return var

def load_shf(files):
    var = xr.open_mfdataset(files, parallel=True).msshf
    var = var.groupby('time.month').mean('time')
    return var

def load_swrf(files):
    var = xr.open_mfdataset(files, parallel=True).msnswrf
    var = var.groupby('time.month').mean('time')
    return var

def load_lwrf(files):
    var = xr.open_mfdataset(files, parallel=True).msnlwrf
    var = var.groupby('time.month').mean('time')
    return var



lhf = 'mslhf/*.nc'
shf = 'msshf/*.nc'
swrf = 'msnswrf/*.nc'
lwrf = 'msnlwrf/*.nc'


lhf_files = (os.path.join(era_dir,  lhf))
shf_files = (os.path.join(era_dir,  shf))
swrf_files = (os.path.join(era_dir,  swrf))
lwrf_files = (os.path.join(era_dir,  lwrf))

try:
    lhf_c =load_lhf(lhf_files)
    lhf_c.to_netcdf(os.path.join(out_dir, 'ERA5_lhf.nc'))
except Exception as e:
    print(e)
    traceback.print_exc()
    pass

try:
    shf_c =load_shf(shf_files)
    shf_c.to_netcdf(os.path.join(out_dir, 'ERA5_shf.nc'))
except Exception as e:
    print(e)
    traceback.print_exc()
    pass

try:
    swrf_c =load_swrf(swrf_files)
    swrf_c.to_netcdf(os.path.join(out_dir, 'ERA5_swrf.nc'))
except Exception as e:
    print(e)
    traceback.print_exc()
    pass

try:
    lwrf_c =load_lwrf(lwrf_files)
    lwrf_c.to_netcdf(os.path.join(out_dir, 'ERA5_lwrf.nc'))
except Exception as e:
    print(e)
    traceback.print_exc()
    pass












sys.exit()

