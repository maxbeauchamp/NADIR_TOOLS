"""
NADIR_TOOLS is a set of libraries to deal with NADIR-based maps
"""

__version__ = "0.0.1"

##################################
# Standard lib
##################################
import sys
import os
import time as timer
from os.path import join as join_paths
from datetime import date, datetime, timedelta
import itertools
import warnings
import traceback
import re
import functools
import configparser
import builtins
from time import sleep
from collections import OrderedDict

assert sys.version_info >= (3,6), "Need Python>=3.6"

##################################
# Config
##################################
dirs = {}
dirs['nadir_tools']    = os.path.dirname(os.path.abspath(__file__))
dirs['NADIR_TOOLS']    = os.path.dirname(dirs['nadir_tools'])

_rc = configparser.ConfigParser()
# Load rc files from dapper, user-home, and cwd
_rc.read(join_paths(x,'dpr_config.ini') for x in
    [dirs['nadir_tools'], os.path.expanduser("~"), os.curdir])
# Convert to dict
rc = {s:dict(_rc.items(s)) for s in _rc.sections() if s not in ['int','bool']}
# Parse
#for x in _rc['bool']: rc[x] = _rc['bool'].getboolean(x)

# Define paths
dirs['datapath']  = dirs['NADIR_TOOLS']
datapath="/gpfswork/rech/yrf/uba22to/NADIR"
rawdatapath="/gpfswork/rech/yrf/uba22to/NADIR_raw"
basepath="/gpfswork/rech/yrf/uba22to/NADIR"

'''if rc['welcome_message']:
  print("Initializing NADIR_TOOLS libraries...",flush=True)'''

##################################
# Scientific and mapping
##################################
import matplotlib.pyplot as plt
import pandas as pd
import shapely
from shapely import wkt
import geopandas as gpd
from cartopy import crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import xarray as xr
import xesmf as xe

##################################
# Tools
##################################
from .mods.tools import *
from .mods.class_NADIR import *
from .mods.class_NADIR_maps import *
from .mods.class_NADIR_nadir import *

'''if rc['welcome_message']:
  print("...Done") # ... initializing Libraries
  print("PS: Turn off this message in your configuration: dpr_config.ini")'''

