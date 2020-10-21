from nadir_tools import *

domain=sys.argv[1]
phase=sys.argv[2]
# convert nadir files to daily NetCDF files
if phase=="training":
    list_path = [rawdatapath+"/alongtracks/"+str for str in ["alg","h2g","j2g","j2n","j3","s3a"] ]
else:
    list_path = [rawdatapath+"/alongtracks/"+str for str in ["c2"] ]
list_files = list([ [ path+'/'+file for file in os.listdir(path) ] for path in list_path ])
list_files = list(itertools.chain(*list_files))
data=NADIR_nadir(list_files,domain) 
data.convert2dailyNetCDF(domain=domain,id_phase=phase)
