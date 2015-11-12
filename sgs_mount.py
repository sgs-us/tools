#!/usr/bin/env python3

""" Mounts the SSH locations to the given mount points. Create ~/mnt and all mount points before. Use -u to umount. """

import subprocess, sys

mounts = [
    ["helium:/import/sgs.local", "~/mnt/sgs"],
    ["helium:", "~/mnt/home"],
    ["helium:/data2/scratch", "~/mnt/scratch"],
    ["ipvslogin:/import/www.ipvs", "~/mnt/www.ipvs"],
    # ["supermuc:", "~/mnt/supermuc"] 
]

uflag = len(sys.argv) > 1 and sys.argv[1] == "-u"

for dev, diry in mounts:
    if uflag:
        cmd = "fusermount -u {}".format(diry)
    else:
        cmd = "sshfs {} {}".format(dev, diry)
    print(cmd, end=": ")
    if not subprocess.call(cmd, shell=True):
        print("OK.")
    else:
        print("FAILED.")
