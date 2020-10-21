from .class_NADIR import *

class NADIR_data(NADIR):                   
    ''' NATL60_data class definition '''

    def __init__(self):
        ''' '''
        NADIR.__init__(self)
        
    def convert_on_grid(self,mask_file=None,longitude_bnds=(-65,-54.95,0.05),latitude_bnds=(30,40.05,0.05),coord_grid=False):
        ''' '''

        # create longitude and latitude of the subdomain grid
        longitude_min,longitude_max,longitude_step=longitude_bnds
        longitude = np.arange(longitude_min, longitude_max, longitude_step)
        latitude_min,latitude_max,latitude_step=latitude_bnds
        latitude = np.arange(latitude_min, latitude_max, latitude_step)
        # import maskfile
        if mask_file is not None:
            mask = np.genfromtxt(mask_file).T
        else:
            mask = np.ones((len(latitude),len(longitude)))
        mesh_latitude, mesh_longitude = np.meshgrid(latitude, longitude)
        # time as string ('%Y-%m-%d')
        # time = [datetime.strftime(datetime.utcfromtimestamp(x.astype('O')/1e9),'%Y-%m-%d') for x in self.data.time.values]
        # time as number of days since 2012-10-01
        time    = np.round(self.data.time.values/86400)
        time_u  = np.sort(np.unique(time))
        lag     = np.empty((len(longitude),len(latitude),len(time_u))) ; lag.fill(np.nan)
        flag     = np.empty((len(longitude),len(latitude),len(time_u))) ; flag.fill(np.nan)
        ssh = np.empty((len(longitude),len(latitude),len(time_u))) ; ssh.fill(np.nan)
        sat = np.empty((len(longitude),len(latitude),len(time_u)),dtype=object) ; sat.fill(np.nan)
        time2 = np.empty((len(longitude),len(latitude),len(time_u))) ; time2.fill(np.nan)
        # find nearest grid point from each datapoint 
        xi = np.searchsorted(longitude,convert_lon_360_180(self.data.longitude.values)) 
        yi = np.searchsorted(latitude,self.data.latitude.values)
        # convert for each time step
        days=np.asarray([ np.where( time_u == time[i] )[0][0] for i in range(0,len(self.data.longitude)) ])
        idx= np.where( (xi<len(longitude)) & (yi<len(latitude)) )
        lag[xi[idx], yi[idx], days[idx]]=self.data.lag.values[idx]
        flag[xi[idx], yi[idx], days[idx]]=self.data.flag.values[idx]
        ssh[xi[idx], yi[idx], days[idx]]=self.data.ssh.values[idx]
        sat[xi[idx], yi[idx], days[idx]]=self.data.sat.values[idx]
        time2[xi[idx], yi[idx], days[idx]]=self.data.time.values[idx]
        # specify xarray arguments
        if coord_grid:
            data_on_grid = xr.Dataset(\
                        data_vars={'longitude': (('latitude','longitude'),mesh_longitude),\
                                   'latitude' : (('latitude','longitude'),mesh_latitude),\
                                   'Time'     : (('time'),time_u),\
                                   'mask'     : (('latitude','longitude'),mask),\
                                   'lag'      : (('time','latitude','longitude'),lag.transpose(2,1,0)),\
                                   'flag'      : (('time','latitude','longitude'),flag.transpose(2,1,0)),\
                                   'ssh'  : (('time','latitude','longitude'),ssh.transpose(2,1,0))},\
                        coords={'longitude': longitude,\
                                'latitude': latitude,\
                                'time': range(0,len(time_u))})
        else:
            data_on_grid = xr.Dataset(\
                        data_vars={'mask'   : (('latitude','longitude'),mask),\
                                   'lag'    : (('time','latitude','longitude'),lag.transpose(2,1,0)),\
                                   'flag'   : (('time','latitude','longitude'),flag.transpose(2,1,0)),\
                                   'Time'   : (('time','latitude','longitude'),time2.transpose(2,1,0)),\
                                   'sat'    : (('time','latitude','longitude'),sat.transpose(2,1,0)),\
                                   'ssh'  : (('time','latitude','longitude'),ssh.transpose(2,1,0))},\
                        coords={'longitude': longitude,\
                                'latitude': latitude,\
                                'time': time_u})
        data_on_grid.time.attrs['units']='days since 2017-01-01 00:00:00'
        return data_on_grid 
        

