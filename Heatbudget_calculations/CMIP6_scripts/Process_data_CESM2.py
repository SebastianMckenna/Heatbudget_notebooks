import xarray as xr
import dask
import numpy as np
import scipy
import os
from HeatBudget_CESM2 import *
from pathlib import Path
import traceback

#loop to go through data folders. Do this in try except so that we know if/when somehting has failed, but the script will keep on running
CMIP_dir = '/scratch/e14/sm2435/CMIP6/'
outdir = '/scratch/e14/sm2435/CMIP6_HB/'
list_models = ['CESM2', 'CESM2-WACCM', 'CESM2-FV2', 'CESM2-WACCM-FV2']
"""
#get all data for temp tendency
var = 'thetao/*.nc'
for model in list_models:
    #input file
    thetao_files = (os.path.join(CMIP_dir, model, var))
    #create file output location if it doesn't exist 
    out_loc = outdir+model
    Path(outdir+model).mkdir(parents=True, exist_ok=True)
    try:
        #calculate temperature tendency
        dTdt = get_temp_tendency(thetao_files)
        #save output as netcdf file
        dTdt.to_netcdf(os.path.join(out_loc, str(model+'_temp_tendency.nc')))
        print (dTdt)
    except Exception as e:
        print(e)
        pass

#get Qnet term
hfds = 'hfds/*.nc'
rsntds = 'rsntds/*.nc'

#Q advection
for model in list_models:
    print('start', model)
    #input file
    rsntds_files = (os.path.join(CMIP_dir, model, rsntds))
    hfds_files = (os.path.join(CMIP_dir, model, hfds))
    #create file output location if it doesn't exist
    out_loc = outdir+model
    Path(outdir+model).mkdir(parents=True, exist_ok=True)
    try:
        #calculate temperature tendency
        print('calc Qnet')
        qnet = get_qnet(hfds_files, rsntds_files)
        print('finish qnet, save output')
        #save output as netcdf file
        qnet.to_netcdf(os.path.join(out_loc, str(model+'_qnet.nc')))
        print('qnet advection saved to ', os.path.join(out_loc, str(model+'_qnet.nc')))
    except Exception as e:
        print(e)
        traceback.print_exc()
        pass
"""


#now calcaulte advection
thetao = 'thetao/*.nc'
uo = 'uo/*.nc'
vo = 'vo/*.nc'
"""
#u advection
for model in list_models:
    print('start', model)
    #input file
    thetao_files = (os.path.join(CMIP_dir, model, thetao))
    uo_files = (os.path.join(CMIP_dir, model, uo))
    #create file output location if it doesn't exist
    out_loc = outdir+model
    Path(outdir+model).mkdir(parents=True, exist_ok=True)
    try:
        #calculate temperature tendency
        print('calc u advection')
        uadv = get_uadv(uo_files, thetao_files)
        print('finish u advection, save output')
        #save output as netcdf file
        uadv.to_netcdf(os.path.join(out_loc, str(model+'_u_advection.nc')))
        print('u advection saved to ', os.path.join(out_loc, str(model+'_u_advection.nc')))
    except Exception as e:
        print(e)
        pass
"""
#v advection
for model in list_models:
    print('start', model)
    #input file
    thetao_files = (os.path.join(CMIP_dir, model, thetao))
    vo_files = (os.path.join(CMIP_dir, model, vo))
    #create file output location if it doesn't exist
    out_loc = outdir+model
    Path(outdir+model).mkdir(parents=True, exist_ok=True)
    try:
        #calculate temperature tendency
        print('calc v advection')
        vadv = get_vadv(vo_files, thetao_files)
        print('finish v advection, save output')
        #save output as netcdf file
        vadv.to_netcdf(os.path.join(out_loc, str(model+'_v_advection.nc')))
        print('v advection saved to ', os.path.join(out_loc, str(model+'_v_advection.nc')))
    except Exception as e:
        print(e)
        pass
"""
#w advection
for model in list_models:
    print('start', model)
    #input file
    thetao_files = (os.path.join(CMIP_dir, model, thetao))
    uo_files = (os.path.join(CMIP_dir, model, uo))
    vo_files = (os.path.join(CMIP_dir, model, vo))
    #create file output location if it doesn't exist
    out_loc = outdir+model
    Path(outdir+model).mkdir(parents=True, exist_ok=True)
    try:
        #calculate temperature tendency
        print('calc w advection')
        wadv = get_wadv(uo_files, vo_files, thetao_files)
        print('finish w advection, save output')
        #save output as netcdf file
        wadv.to_netcdf(os.path.join(out_loc, str(model+'_w_advection.nc')))
        print('w advection saved to ', os.path.join(out_loc, str(model+'_w_advection.nc')))
    except Exception as e:
        print(e)
        pass

"""

