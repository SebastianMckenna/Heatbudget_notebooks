import xarray as xr
import dask
import numpy as np
#function to get T at 50m
def get_bot_layer(T):
    """
    Parameters
    --------------
    T : DataArray
        DataArray of chosen variable
    

    Returns
    --------------
    Array
        Array of the bottom of each layer (the k-1 coordinate from temperature)
    """
    T_lay = T.lev
    lay_bot=np.array([0.])
    for i in range(len(T_lay.values)):
        thickness = 2*T_lay.values[i]-lay_bot[i]
        lay_bot = np.insert(lay_bot,i+1,thickness)
    return lay_bot[1:]

def int_TUV_50(T):
    """
    Parameters
    --------------
    T : DataArray
        DataArray of chosen variable
    

    Returns
    --------------
    DataArray
        DataArray of the chosen variable for the k coordinate interpolated so \
        that bottom (vertical velocity) layer is at 50m
    """
    #get the bottom layer array
    bottom = get_bot_layer(T)
    #get the value of the layer under 50
    lev_n1 = max(val for val in bottom if val < 50)
    #now get the value of the layer to interpolate to
    lev_nt = lev_n1 + ((50-lev_n1)/2)
    return lev_nt

def insert_level(T):
    """
    Parameters
    --------------
    T : DataArray
        DataArray of chosen variable
    

    Returns
    --------------
    DataArray
        DataArray of the chosen variable with new interpolated value for T coordinate 
        corresopsonding to 50m (bottom (vertical velocity) layer is at 50m). 
        If this layer exists already, then nothing is inserted
    """
    #calc new level
    new_layer_val = int_TUV_50(T)
    #check if this level exists
    if new_layer_val not in T.lev.values:
        #interpolate values into new layer layer
        new_layer = T.interp(lev = new_layer_val)
        #now concat adding the last level, after removing any data deeper than desired layer
        T = T.sel(lev=slice(0,new_layer_val))
        Tnew = xr.concat([T, new_layer], dim = 'lev')
    else:
        #remove anyting below 50m
        Tnew = T.sel(lev=slice(0,50))
    return Tnew

def insert_level_w(T):
    """
    Parameters
    --------------
    T : DataArray
        DataArray of chosen variable
    

    Returns
    --------------
    DataArray
        DataArray of the chosen variable with new interpolated value for Z coordinate for W 
        corresopsonding to 50m (bottom (vertical velocity) layer is at 50m). 
        If this layer exists already, then nothing is inserted
    """
    #new level
    new_layer_val = 50
    #check if layer exists
    if new_layer_val not in T.lev.values:
        #interpolate values into new layer layer
        new_layer = T.interp(lev = new_layer_val)
        #now concat adding the last level, after removing any data that comes before hand
        T = T.sel(lev=slice(0,new_layer_val))
        Tnew = xr.concat([T, new_layer], dim = 'lev')
    else:
        #remove all bellow 50m
        Tnew = T.sel(lev=slice(0,51))
    return Tnew
def diff_T(T):
    try:
        dTdt = T.differentiate(coord = 'time', edge_order=1,  datetime_unit= 's')
    except:
        dTdt = T.chunk('auto').differentiate(coord = 'time', edge_order=1,  datetime_unit= 's')
    return dTdt
def get_weights(INP):
    weights = INP.lev
    #add a 0m surface layer
    wt=np.array([0.])
    for i in range(len(weights.values)):
        NW = 2*weights.values[i]-wt[i]
        wt = np.insert(wt,i+1,NW)
    thickness = wt[1:]-wt[:-1]
    thickness_DA = xr.DataArray(thickness, coords={'lev': INP.lev},
                 dims=['lev'])
    return thickness_DA

def weighted_avg(inp):
    weights = get_weights(inp)
    avg=inp.weighted(weights).mean('lev')
    return avg


def get_clim(INP):
    INP = INP.groupby('time.month').mean('time')
    return INP
def get_temp_tendency(model):
    #load in T
    T = xr.open_mfdataset(model, parallel=True).votemper.rename({'time_counter':'time', 'deptht':'lev'})
    #convert level to m if not already
    if T.lev.attrs['units'] =='m':
        pass
    elif T.lev.attrs['units'] =='cm':
        T['lev'] = T['lev']/100
        T.lev.attrs['units'] = 'm'
    elif T.lev.attrs['units'] =='centimeters':
        T['lev'] = T['lev']/100
        T.lev.attrs['units'] = 'm'
    #subset spatially
    T = T.sel(lat=slice(-40,30),lon=slice(30,125))
    #subset time
    T = T.sel(time= slice('1950', '2015'))
    #interpolate to 50m
    T = insert_level(T)
    #get time deriviative
    dTdt = diff_T(T)
    #weighted average
    dTdt_w = weighted_avg(dTdt)
    #get climatology
    dTdt_clim = get_clim(dTdt_w)
    return dTdt_clim
#fucntions to get dtdx and dtdy
def T_xgrad(T):
    dTdx = T.differentiate('lon', edge_order = 1) / (110e3 * np.cos(T.lat * np.pi / 180))
    return dTdx
def T_ygrad(T):
    dTdy = T.differentiate('lat', edge_order = 1) / (110e3 )
    return dTdy
def load_U(model):
    #load in U
    U = xr.open_mfdataset(model, parallel=True).vozocrte.rename({'time_counter':'time', 'deptht':'lev'})
    #convert level to m if not already
    if U.lev.attrs['units'] =='m':
        pass
    elif U.lev.attrs['units'] =='cm':
        U['lev'] = U['lev']/100
        U.lev.attrs['units'] = 'm'
    elif U.lev.attrs['units'] =='centimeters':
        U['lev'] = U['lev']/100
        U.lev.attrs['units'] = 'm'
    #subset spatially
    U = U.sel(lat=slice(-40,30),lon=slice(30,125))
    #subset time
    U = U.sel(time= slice('1950', '2015'))
    #interpolate to 50m
    U = insert_level(U)
    #set land values to 0
    U = U.fillna(0)
    return U
def load_V(model):
    #load in U
    U = xr.open_mfdataset(model, parallel=True).vomecrtn.rename({'time_counter':'time', 'deptht':'lev'})
    if U.lev.attrs['units'] =='m':
        pass
    elif U.lev.attrs['units'] =='cm':
        U['lev'] = U['lev']/100
        U.lev.attrs['units'] = 'm'
    elif U.lev.attrs['units'] =='centimeters':
        U['lev'] = U['lev']/100
        U.lev.attrs['units'] = 'm'
    #subset spatially
    U = U.sel(lat=slice(-40,30),lon=slice(30,125))
    #subset time
    U = U.sel(time= slice('1950', '2015'))
    #interpolate to 50m
    U = insert_level(U)
    #set land values to 0
    U = U.fillna(0)
    return U
def load_T(model):
    #load in U
    T = xr.open_mfdataset(model, parallel=True).votemper.rename({'time_counter':'time', 'deptht':'lev'})
    if T.lev.attrs['units'] =='m':
        pass
    elif T.lev.attrs['units'] =='cm':
        T['lev'] = T['lev']/100
        T.lev.attrs['units'] = 'm'
    elif T.lev.attrs['units'] =='centimeters':
        T['lev'] = T['lev']/100
        T.lev.attrs['units'] = 'm'
    #subset spatially
    T = T.sel(lat=slice(-40,30),lon=slice(30,125))
    #subset time
    T = T.sel(time= slice('1950', '2015'))
    #interpolate to 50m
    T = insert_level(T)
    return T

def get_uadv(modelu, modelt):
    #load u
    U = load_U(modelu)
    T = load_T(modelt)
    #get xgrad
    dtdx = T_xgrad(T)
    #calc advection
    uadv = U*dtdx
    #weighted average
    uadv_w = weighted_avg(uadv)
    #get climatology
    uadv_clim = get_clim(uadv_w)
    return uadv_clim

def get_vadv(modelv, modelt):
    #load u
    V = load_V(modelv)
    T = load_T(modelt)
    #get xgrad
    dtdy = T_ygrad(T)
    #calc advection
    vadv = V*dtdy
    #weighted average
    vadv_w = weighted_avg(vadv)
    #get climatology
    vadv_clim = get_clim(vadv_w)
    return vadv_clim
#make functions for getting w advection
def load_U_w(model):
    #load in U
    U = xr.open_mfdataset(model, parallel=True).vozocrte.rename({'time_counter':'time', 'deptht':'lev'})
    if U.lev.attrs['units'] =='m':
        pass
    elif U.lev.attrs['units'] =='cm':
        U['lev'] = U['lev']/100
        U.lev.attrs['units'] = 'm'
    elif U.lev.attrs['units'] =='centimeters':
        U['lev'] = U['lev']/100
        U.lev.attrs['units'] = 'm'
    #subset spatially
    U = U.sel(lat=slice(-40,30),lon=slice(30,125))
    #subset time
    U = U.sel(time= slice('1950', '2015'))
    #set land values to 0
    U = U.fillna(0)
    return U
def load_V_w(model):
    #load in U
    U = xr.open_mfdataset(model, parallel=True).vomecrtn.rename({'time_counter':'time', 'deptht':'lev'})
    if U.lev.attrs['units'] =='m':
        pass
    elif U.lev.attrs['units'] =='cm':
        U['lev'] = U['lev']/100
        U.lev.attrs['units'] = 'm'
    elif U.lev.attrs['units'] =='centimeters':
        U['lev'] = U['lev']/100
        U.lev.attrs['units'] = 'm'
    #subset spatially
    U = U.sel(lat=slice(-40,30),lon=slice(30,125))
    #subset time
    U = U.sel(time= slice('1950', '2015'))
    #set land values to 0
    U = U.fillna(0)
    return U
def calc_w_no_w(model_u, model_v):
    U = load_U_w(model_u)
    V = load_V_w(model_v)
    dudx = U.differentiate(coord = 'lon') / (110e3 * np.cos(U.lat * np.pi / 180))
    dvdy = V.differentiate(coord='lat') / (110e3)
    lay_bot = get_bot_layer(U)
    w_list = []
    for i, j in enumerate(lay_bot):
        if i == 0:
            dz = 0 - j
            w = (dudx[:,i] + dvdy[:,i])*-dz
            #add to new DataArray with vertical coords put in
            w = w.assign_coords({'lev': lay_bot[i]})
            w_list.append(w)
        else:
            dz = lay_bot[i-1] - j
            l = (dudx[:,i] + dvdy[:,i])*-dz + w_list[i-1]
            w = l.assign_coords({'lev': lay_bot[i]})
            w_list.append(w)
    #now put all layers into one array
    w = xr.concat(w_list, dim = 'lev')
    return w


def T_zgrad(T):
    #get z at 50m layer (but at t coordinate part of it)
    dTdz = (T[:,0] - T[:,-1])/float(T.lev[-1])
    return dTdz

def get_wadv_cont(modelu, modelv, modelt):
    #load
    W = calc_w_no_w(modelu, modelv)
    #get W at 50 m
    W = W.interp(lev=50)
    T = load_T(modelt)
    #get zgrad
    dtdz = T_zgrad(T)
    #calc advection
    wadv = W*dtdz
    wadv_clim = get_clim(wadv)
    return wadv_clim



def load_hfds(model):
    q = xr.open_mfdataset(model, parallel=True).sohefldo.rename({'time_counter':'time'})
    #subset spatially
    q = q.sel(lat=slice(-40,30),lon=slice(30,125))
    #subset time
    q = q.sel(time= slice('1950', '2015'))
    return q


def get_qnet(q_data):
    Q = load_hfds(q_data)
    qnet = Q/(3986*1026*50)
    #now get climatology
    qnet = get_clim(qnet)
    return qnet
