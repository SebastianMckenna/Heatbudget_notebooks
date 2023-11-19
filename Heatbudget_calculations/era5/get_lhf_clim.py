import xarray as xr
import pandas as pd
import numpy as np
import scipy
import os
import sys

era_dir="/g/data/e14/sm2435/ERA5/"
out_dir="/g/data/e14/sm2435/ERA5/clim/"

def load_lhf(lhf_files):
    lhf = xr.open_mfdataset(lhf_files, parallel=True).mslhf
    return lhf
def get_lhf_clim(lhf_files):
    lhf = load_lhf(lhf_files)
    lhf = lhf.groupby('time.month').mean('time')
    return lhf

#tauu and tauv files
lhf = 'lhf/*.nc'

#Wstress compoenents
lhf_files = (os.path.join(era_dir,  lhf))
try:
    #calculate wspd
    lhf_c =get_lhf_clim(lhf_files)
    #save output as netcdf file
    lhf_c.to_netcdf(os.path.join(out_dir, 'ERA5_lhf.nc'))
except Exception as e:
    print(e)
    traceback.print_exc()
    pass
sys.exit()

