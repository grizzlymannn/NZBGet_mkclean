#!/usr/bin/env python
#
##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Runs mkclean on mkv files to make them more stream-able
#
# NOTE: This script requires Python to be installed on your system.

##############################################################################
### OPTIONS                                                                ###

# mkclean Path
#
# Path to the mkclean executable
#mkcleanpath=/usr/local/bin/mkclean

### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

import os
import sys
import subprocess


# NZBGet Exit Codes
NZBGET_POSTPROCESS_PARCHECK = 92
NZBGET_POSTPROCESS_SUCCESS = 93
NZBGET_POSTPROCESS_ERROR = 94
NZBGET_POSTPROCESS_NONE = 95

if not os.environ.has_key('NZBOP_SCRIPTDIR'):
    print("This script can only be called from NZBGet (11.0 or later).")
    sys.exit(0)

if os.environ['NZBOP_VERSION'][0:5] < '11.0':
    print("NZBGet Version %s is not supported. Please update NZBGet." % (str(os.environ['NZBOP_VERSION'])))
    sys.exit(0)

print("Script triggered from NZBGet Version %s." % (str(os.environ['NZBOP_VERSION'])))
status = 0
if os.environ.has_key('NZBPP_TOTALSTATUS'):
    if not os.environ['NZBPP_TOTALSTATUS'] == 'SUCCESS':
        print("Download failed with status %s." % (os.environ['NZBPP_STATUS']))
        status = 1

else:
    # Check par status
    if os.environ['NZBPP_PARSTATUS'] == '1' or os.environ['NZBPP_PARSTATUS'] == '4':
        print("Par-repair failed, setting status \"failed\".")
        status = 1

    # Check unpack status
    if os.environ['NZBPP_UNPACKSTATUS'] == '1':
        print("Unpack failed, setting status \"failed\".")
        status = 1

    if os.environ['NZBPP_UNPACKSTATUS'] == '0' and os.environ['NZBPP_PARSTATUS'] == '0':
        # Unpack was skipped due to nzb-file properties or due to errors during par-check

        if os.environ['NZBPP_HEALTH'] < 1000:
            print("Download health is compromised and Par-check/repair disabled or no .par2 files found. Setting status \"failed\".")
            print("Please check your Par-check/repair settings for future downloads.")
            status = 1

        else:
            print("Par-check/repair disabled or no .par2 files found, and Unpack not required. Health is ok so handle as though download successful.")
            print("Please check your Par-check/repair settings for future downloads.")

# Check if destination directory exists (important for reprocessing of history items)
if not os.path.isdir(os.environ['NZBPP_DIRECTORY']):
    print("Nothing to post-process: destination directory", os.environ['NZBPP_DIRECTORY'], "doesn't exist. Setting status \"failed\".")
    status = 1

# All checks done, now launching the script.
if status == 1:
    sys.exit(NZBGET_POSTPROCESS_NONE)

for dirpath, dirnames, filenames in os.walk(os.environ['NZBPP_DIRECTORY']):
    for file in filenames:
        if file.endswith('.mkv'):
         filepath = os.path.join(dirpath, file)
         print("cleaning file " + filepath)
         try:
             subprocess.call([os.environ.get('NZBPO_MKCLEANPATH'), "--optimize", "--quiet", "--doctype", "3", filepath])
         except:
            print("Error: unable to clean file " + filepath)
            sys.exit(NZBGET_POSTPROCESS_ERROR)
         print("renaming cleaned file " + filepath)
         try:
            newfile = "clean." + file
            newfilepath = os.path.join(dirpath, newfile)
            if os.path.exists(filepath):
               if os.path.exists(newfilepath):
                  os.remove(filepath)
                  os.rename(newfilepath, filepath)
               else:
                  print("Error: file not present " + newfilepath)
                  sys.exit(NZBGET_POSTPROCESS_ERROR)
            else:
               print("Error: file not present" + filepath)
               sys.exit(NZBGET_POSTPROCESS_ERROR)
         except:
            print("Error: unable to rename file " + newfilepath)
            sys.exit(NZBGET_POSTPROCESS_ERROR)

sys.exit(NZBGET_POSTPROCESS_SUCCESS)
