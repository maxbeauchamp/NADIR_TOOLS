from .class_NADIR_data import *
import re
import cftime
from datetime import datetime, timezone

class NADIR_nadir(NADIR_data):
    ''' NADIR_nadir class definition'''

    @staticmethod
    def preprocess1(ds):
        extent=[-19.5,-11.5,45.,55.]
        ds.time.attrs['units'] = 'days since 1950-01-01'
        ds.time.attrs['calendar'] = 'standard'
        index = np.where( (convert_lon_360_180(ds.longitude.values) >= extent[0]) &\
                          (convert_lon_360_180(ds.longitude.values) <= extent[1]) &\
                          (ds.latitude.values >= extent[2]) &\
                          (ds.latitude.values <= extent[3]) )[0]
        ds = ds.isel(time=index)
        # add id satellites
        path=ds.encoding['source']
        nm_sat = ['alg','h2g','j2g','j2n','j3','s3a','c2']
        id_sat=[nm_sat[i] for i in range(0,len(nm_sat)) \
               if re.search(nm_sat[i],path)][0]
        ds = ds.update({'sat':('time',np.repeat(id_sat,len(ds.time.values)))})
        #ds = xr.decode_cf(ds)
        return ds

    @staticmethod
    def preprocess2(ds):
        extent=[-65.,-55.,33.,43.]
        ds.time.attrs['units'] = 'days since 1950-01-01'
        ds.time.attrs['calendar'] = 'standard'
        index = np.where( (convert_lon_360_180(ds.longitude.values) >= extent[0]) &\
                          (convert_lon_360_180(ds.longitude.values) <= extent[1]) &\
                          (ds.latitude.values >= extent[2]) &\
                          (ds.latitude.values <= extent[3]) )[0]
        ds = ds.isel(time=index)
        path=ds.encoding['source']
        nm_sat = ['alg','h2g','j2g','j2n','j3','s3a','c2']
        id_sat=[nm_sat[i] for i in range(0,len(nm_sat)) \
               if re.search(nm_sat[i],path)][0]
        ds = ds.update({'sat':('time',np.repeat(id_sat,len(ds.time.values)))})
        #ds = xr.decode_cf(ds)
        return ds

    @staticmethod
    def preprocess3(ds):
        extent=[-19.5,-11.5,45.,55.]
        ds.time.attrs['units'] = 'days since 1950-01-01'
        ds.time.attrs['calendar'] = 'standard'
        index = np.where( (convert_lon_360_180(ds.longitude.values) >= extent[0]) &\
                          (convert_lon_360_180(ds.longitude.values) <= extent[1]) &\
                          (ds.latitude.values >= extent[2]) &\
                          (ds.latitude.values <= extent[3]) )[0]
        ds = ds.isel(time=index)
        return ds

    @staticmethod
    def preprocess4(ds):
        extent=[-65.,-55.,33.,43.]
        ds.time.attrs['units'] = 'days since 1950-01-01'
        ds.time.attrs['calendar'] = 'standard'
        index = np.where( (convert_lon_360_180(ds.longitude.values) >= extent[0]) &\
                          (convert_lon_360_180(ds.longitude.values) <= extent[1]) &\
                          (ds.latitude.values >= extent[2]) &\
                          (ds.latitude.values <= extent[3]) )[0]
        ds = ds.isel(time=index)
        return ds


    def __init__(self,list_files,domain,dateref=None,extent=[-65,-55,30,40],preproc="v1"):
        ''' '''
        # preproc: 1 or 2
        NADIR_data.__init__(self)
        if domain=="OSMOSIS":
            extent=[-19.5,-11.5,45.,55.]
        elif domain=='GULFSTREAM':
            extent=[-65.,-55.,33.,43.]
        else: 
            extent=[-65.,-55.,30.,40.]
        if len(list_files)>0:
            if preproc=="v1":
                if domain=="OSMOSIS":
                    self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess1)
                if domain=="GULFSTREAM":
                    self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess2)
            else:
                if domain=="OSMOSIS":
                    self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess3)
                if domain=="GULFSTREAM":
                    self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess4)
            self.data = self.data.sortby('time')
            lvar=['longitude','latitude','sla_filtered','mdt']
            order = np.argsort(self.data.time.values)
            new_time = self.data.time.values[order]
            self.data['time'] = new_time
            for i in range(0,len(lvar)):
                self.data = self.data.update({lvar[i]:('time',self.data[lvar[i]].values[order])})
            if dateref is not None:
                # add lag variable
                lag = np.asarray([ np.round( ( (np.datetime64((datetime(1950, 1, 1, tzinfo=timezone.utc) + timedelta(days=x))) -np.datetime64(datetime.strptime(dateref,'%Y-%m-%d'))) / np.timedelta64(1, 's'))/(3600*24),1) for x in self.data.time.values])
                self.data = self.data.update({'lag':('time',lag)})
                # add flag variable (nadir=0, swot=1)
                flag = np.repeat(0,len(self.data.time.values))
                self.data = self.data.update({'flag':('time',flag)})
            # add ssh variable
            self.data = self.data.update({'ssh':('time',self.data.sla_filtered.values+self.data.mdt.values)})
            # finalize
            self.data = self.data.dropna('time', how='any')
            self.extent=extent
            self.shape = tuple(self.data.dims[d] for d in ['time'])
        else:
            self.data=None
            self.shape = (0)
        self.gridded=False

    @classmethod
    def init2(cls,domain,dateref,t1,t2,id_phase,preproc="v1"):
        ''' '''
        t1_fmt=datetime.strptime(t1,'%Y-%m-%d')
        t2_fmt=datetime.strptime(t2,'%Y-%m-%d')    
        daterange = [datetime.strftime(t1_fmt + timedelta(days=x),"%Y-%m-%d") for x in range(0, (t2_fmt-t1_fmt).days+1)]
        if id_phase=="training":
            list_files=[rawdatapath+"/alongtracks/"+domain+"/training/NADIR_"+t+"_1d.nc" for t in daterange if os.path.exists(rawdatapath+"/alongtracks/"+domain+"/training/NADIR_"+t+"_1d.nc")]
        else:
            list_files=[rawdatapath+"/alongtracks/"+domain+"/validation/NADIR_"+t+"_1d.nc" for t in daterange if os.path.exists(rawdatapath+"/alongtracks/"+domain+"/validation/NADIR_"+t+"_1d.nc")]
        return cls(list_files,domain,dateref,preproc=preproc)

    def sel_time(self,t1,t2):
        ''' '''
        self.data = self.data.sel(time=slice(t1,t2))
        self.shape = tuple(self.data.dims[d] for d in ['time'])

    def convert2dailyNetCDF(self,domain,id_phase):
        ''' '''
        daterange = [datetime.strftime(datetime.strptime("2017-01-01","%Y-%m-%d") + timedelta(days=x),"%Y-%m-%d") for x in range (0,365)]
        for t in daterange:
            print(t)
            data_tmp = self.data.sel(time=slice(t,t))
            data_tmp = data_tmp.rename({'longitude': 'longitude',\
                                        'latitude': 'latitude',\
                                        'ssh': 'ssh',\
                                        'sat': 'sat'})
            new_time = [(x-np.datetime64('1950-01-01T00:00:00Z')) / np.timedelta64(1,'D') for x in data_tmp.time.values]
            data_tmp = data_tmp.assign(time=new_time)
            if id_phase=="training":
                new_file = rawdatapath+"/alongtracks/"+domain+"/training/NADIR_"+t+"_1d.nc"
            else:
                new_file = rawdatapath+"/alongtracks/"+domain+"/validation/NADIR_"+t+"_1d.nc"
            if os.path.exists(new_file):
                mode_="a"
            else:
                mode_="w"
            mode_="w"
            data_tmp.to_netcdf(path=new_file,mode=mode_)

