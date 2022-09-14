# NZBGet_mkclean

This is a post processing script for NZBGet.  It will run [mkclean](https://www.matroska.org/downloads/mkclean.html) on downloaded MKV files.

Originally found [here](https://forum.nzbget.net/viewtopic.php?t=2253#p16307).  Fixed errors so it runs with modern NZBGet.

To use:  
1. Compile mkclean from source.
2. Copy `Mkclean.py` to the NZBGet `scripts` folder.
3. Enable `Mkclean.py` in the Extensions section of the NZBGet Settings.
