from nadir_tools import *

# function to create recursive paths
def mk_dir_recursive(dir_path):
    if os.path.isdir(dir_path):
        return
    h, t = os.path.split(dir_path)  # head/tail
    if not os.path.isdir(h):
        mk_dir_recursive(h)

    new_path = join_paths(h, t)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)

# function to convert lon from 0:360 to -180:180
def convert_lon_360_180(lon):
    return np.asarray([ ((x+180)%360)-180 for x in lon ])

# generic function for cartopy-based mapping
def make_map(extent):
   fig, ax = plt.subplots(figsize=(8, 7),
                          subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=0.0)))
   ax.set_extent(list(extent))
   gl = ax.gridlines(alpha=0.5,draw_labels=True)
   gl.xformatter = LONGITUDE_FORMATTER
   gl.yformatter = LATITUDE_FORMATTER
   ax.coastlines(resolution='50m')
   return fig, ax

