#!/usr/bin/env python
import os
import re
import sys

def get_size(start_path = '.'):
    print(" Files => Dir sizes in MB")
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        dir_size = 0
        dir_files = 0
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                dir_size += os.path.getsize(fp)
                dir_files += 1
        dir_size = dir_size / 1024 / 1024
        dir_sizeS = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%10d" % dir_size)
        print("{df:6d} => {ds:>15s} <= {dir:s} ".format(df=dir_files, ds=dir_sizeS, dir=dirpath))
    total_size = total_size / 1024 / 1024 / 1024
    print("===================================")
    print("{ts:>15d} <= Total Size (GB)".format(ts=total_size))
if len(sys.argv)>1:
    get_size(sys.argv[1])
else:
    get_size()