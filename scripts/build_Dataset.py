from nadir_tools import *

nadir_lag=int(sys.argv[1])
domain=sys.argv[2]
id_phase=sys.argv[3]
if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
    mask_file=None
elif domain=='GULFSTREAM':
    extent=[-65.,-55.,33.,43.]
    mask_file=None

if __name__ == '__main__':

    daterange = [datetime.strftime(datetime.strptime("2017-01-01","%Y-%m-%d") + timedelta(days=x),"%Y-%m-%d")\
                 for x in range (0,365)]
    for i in range(0,len(daterange)):
        date=daterange[i]
        print(date)
        # read nadir
        date1_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") \
                    + timedelta(days=-1*nadir_lag),"%Y-%m-%d")
        date2_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d")\
                    + timedelta(days=nadir_lag),"%Y-%m-%d")
        nadir=NADIR_nadir.init2(domain,date,date1_nadir,date2_nadir,id_phase)
        nadir.sel_spatial(extent)   
        if len(nadir.data.longitude)==0:
            # create empty swot dataset 
            time_u = (np.datetime64(datetime.strptime(date,'%Y-%m-%d'))-\
                     np.datetime64('2017-01-01T00:00:00Z')) / np.timedelta64(1, 's')
            nadir.data=xr.Dataset(\
                        data_vars={'longitude': (('time'),np.empty((1))),\
                                   'latitude' : (('time'),np.empty((1))),\
                                   'lag'      : (('time'),np.empty((1))),\
                                   'flag'     : (('time'),np.empty((1))),\
                                   'sat'      : (('time'),np.empty((1))),\
                                   'Time'     : (('time'),np.empty((1))),\
                                   'ssh'      : (('time'),np.empty((1)))},\
                        coords={'time': [time_u]})
        # conversion on grid
        # modifications of time values to force unique time values after regridding
        new_time = [(np.datetime64(datetime.strptime(date,'%Y-%m-%d') + timedelta(seconds=dt))-\
                     np.datetime64('2017-01-01T00:00:00Z')) / np.timedelta64(1, 's') \
                     for dt in np.linspace(0,0.99,len(nadir.data.time)) ]
        nadir.data = nadir.data.assign(time=new_time)
        nadir=nadir.convert_on_grid(mask_file,\
                                    longitude_bnds=(extent[0],extent[1]+0.05,0.05),\
                                    latitude_bnds=(extent[2],extent[3]+0.05,0.05))
        # concatenation along time
        if i != 0:
            Gnadir=xr.concat([Gnadir,nadir],dim='time',data_vars='minimal')    
        else:
            Gnadir=nadir
    # write in file
    mk_dir_recursive(datapath+"/"+domain+'/training')
    mk_dir_recursive(datapath+"/"+domain+'/validation')
    if id_phase=="training":
        Gnadir.to_netcdf(path=datapath+"/"+domain+'/training/dataset_nadir_'+str(nadir_lag)+'d.nc',mode="w",unlimited_dims=["time"])
    else:
        Gnadir.to_netcdf(path=datapath+"/"+domain+'/validation/dataset_nadir_'+str(nadir_lag)+'d.nc',mode="w",unlimited_dims=["time"])
