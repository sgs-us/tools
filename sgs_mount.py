#!/usr/bin/env python3

""" Mounts the SSH locations to the given mount points. Create ~/mnt and all mount points before. Use -u to umount. """

import subprocess, sys, os

whoami = os.getlogin()

mounts = [
    ["helium:/import/sgs.local", "~/mnt/sgs"],
    ["helium:", "~/mnt/home"],
    ["helium:/data2/scratch/{}".format(whoami), "~/mnt/scratch"],
    ["neon:/data/scratch/{}".format(whoami), "~/mnt/neon_scratch"],
    ["ipvslogin:/import/www.ipvs", "~/mnt/www.ipvs"],
    # ["supermuc:", "~/mnt/supermuc"] 
]

uflag = len(sys.argv) > 1 and sys.argv[1] == "-u"

for dev, diry in mounts:
    if uflag:
        cmd = "fusermount -u {}".format(diry)
    else:
        cmd = "sshfs {} {}".format(dev, diry)
    print("{:70s}".format(cmd), end="")
    if not subprocess.call(cmd, shell=True):
        print("OK.")
    else:
        print("FAILED.")
