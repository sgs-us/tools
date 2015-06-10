#!env python

""" Mounts the SSH locations to the given mount points. Create ~/mnt before. Use -u to umount. """

import subprocess, sys

mounts = [
    ["helium:/import/sgs.local", "~/mnt/sgs"],
    ["helium:", "~/mnt/home"],
    ["helium:/data2/scratch", "~/mnt/scratch"],
    ["ipvslogin:/import/www.ipvs", "~/mnt/www.ipvs"],
    # ["supermuc:", "~/mnt/supermuc"] 
]

try:
    arg = sys.argv[1]
except IndexError:
    arg = ""

print(arg)
for m in mounts:
    if arg == "-u":
        cmd = "fusermount -u " + m[1]
    else:
        cmd = "sshfs " + m[0] + " " + m[1]
    print(cmd)
    subprocess.call( cmd, shell=True )
