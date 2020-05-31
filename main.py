import pandas as pd
import numpy as np
import os
import pandas as pd 
import numpy as np
import re
import math
import warnings 
import codecs
import os
import csv
import sys
from os import listdir
from os.path import isfile, join
from datetime import datetime

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs




from convert_files import reboot_convert
from convert_files import auth_convert
from convert_files import kern_convert
from convert_files import syslog_convert
from convert_files import login_convert



logfile_path='Logging/LogFiles'
# print(logfile_path)

# print((os.path. exists(logfile_path)))
if(os.path. exists(logfile_path)==False):
    # os.system('sudo chmod 777 GetDir.sh')
    # os.system('./GetDir.sh')
    os.system('cd')
    os.system('mkdir LogFiles')
    # os.system('mkdir Logfile/kern')
#  print((os.path. exists(logfile_path)))
# o
files = open("Logging/file_names.txt", "r")
commands = (files.read().splitlines()) 
for cmd in commands:
    os.system(cmd)

kern_path=logfile_path+'/kern'
sys_path=logfile_path+'/syslog'
auth_path=logfile_path+'/auth'
# print(kern_path)


file='reboot.txt'
text_file=logfile_path+'/'+file
csv_file=logfile_path+'/CSV/'+file[:-4]+'.csv'
reboot_convert(text_file,csv_file)

file='lastlog.txt'
text_file=logfile_path+'/'+file
csv_file=logfile_path+'/CSV/'+file[:-4]+'.csv'
login_convert(text_file,csv_file)

kernfiles = [file for file in listdir(kern_path) if isfile(join(kern_path, file))]
for file in kernfiles:
    text_file=kern_path+'/'+file
    csv_file=kern_path+'/'+file[:-4]+'.csv'
    auth_convert(text_file,csv_file)


authfiles = [file for file in listdir(auth_path) if isfile(join(auth_path, file))]
for file in authfiles:
    text_file=auth_path+'/'+file
    csv_file=auth_path+'/'+file[:-4]+'.csv'
    auth_convert(text_file,csv_file)

sysfiles = [file for file in listdir(sys_path) if isfile(join(sys_path, file))]# print(kernfiles)
for file in sysfiles:
    text_file=sys_path+'/'+file
    csv_file=sys_path+'/'+file[:-4]+'.csv'
    auth_convert(text_file,csv_file)



# Each tab is drawn by a different script
from scripts.login import make_login_tab
from scripts.kernel import make_kernel_tab
from scripts.reboot import make_reboot_tab
from scripts.auth import make_auth_tab
from scripts.syslog import make_syslog_tab
tab1 = make_login_tab()
tab2 = make_kernel_tab()
tab3 = make_reboot_tab()
tab4 = make_auth_tab()
tab5 = make_syslog_tab()

tabs = Tabs(tabs = [tab1,tab2,tab3,tab4,tab5])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
curdoc().title = "Log Monitor"