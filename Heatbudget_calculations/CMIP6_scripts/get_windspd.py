import xarray as xr
import dask
import numpy as np
import scipy
import os
#from HeatBudget import *
from pathlib import Path
import traceback
import xarray.ufuncs as xu


#loop to go through data folders. Do this in try except so that we know if/when somehting has failed, but the script will keep on running
CMIP_dir = '/scratch/e14/sm2435/CMIP6/'
outdir = '/scratch/e14/sm2435/CMIP6_HB/'

def load_tau(tx_files, ty_files):
    tx = xr.open_mfdataset(tx_files, parallel=True).tauuo
    ty = xr.open_mfdataset(ty_files, parallel=True).tauvo
    return tx, ty


def coriolis_param(lat):
    day = (24*60*60)-(4*60)# this is 23hrs 56mins
    om = (2*np.pi)/day
    f = 2*om*np.sin(lat * np.pi / 180)
    return f

def WSC(tx_files, ty_files):
    tx,ty = load_tau(tx_files, ty_files)
    dtydx = ty.differentiate('lon') / (110e3 * np.cos(ty.lat * np.pi / 180))
    dtxdy = tx.differentiate('lat') / (110e3 )
    wsc = dtydx-dtxdy
    wsc = wsc.groupby('time.month').mean('time')
    return wsc

def wspd(tx_files, ty_files):
    tx,ty = load_tau(tx_files, ty_files)
    ws = xu.sqrt(tx**2+ty**2)
    ws = ws.groupby('time.month').mean('time')
    return ws


#tauu and tauv files
tauu = 'tauuo/*.nc'
tauv = 'tauvo/*.nc'

#Wspd
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
        print('calc wspd')
        wspd_var = wspd(tauu_files, tauv_files)
        print('finish wspd, save output')
        #save output as netcdf file
        wspd_var.to_netcdf(os.path.join(out_loc, str(model+'_wspd.nc')))
        print('wspd saved to ', os.path.join(out_loc, str(model+'_wspd.nc')))
    except Exception as e:
        print(e)
        traceback.print_exc()
        pass

#Wind stress curl
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
        print('calc wsc')
        wsc_var = WSC(tauu_files, tauv_files)
        print('finish wsc, save output')
        #save output as netcdf file
        wsc_var.to_netcdf(os.path.join(out_loc, str(model+'_wsc.nc')))
        print('wsc saved to ', os.path.join(out_loc, str(model+'_wsc.nc')))
    except Exception as e:
        print(e)
        traceback.print_exc()
        pass



