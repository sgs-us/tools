#!/usr/bin/env python3

""" Mounts the SSH locations to the given mount points. Create ~/mnt and all mount points before. Use -u to umount. """

import subprocess, sys, os, threading

whoami = os.getlogin()

mounts = [
    ["helium:/import/sgs.local", "~/mnt/sgs"],
    ["helium:", "~/mnt/home"],
    ["helium:/data/scratch/{}".format(whoami), "~/mnt/scratch"],
    ["neon:/data/scratch/{}".format(whoami), "~/mnt/neon_scratch"],
    ["ipvslogin:/import/www.ipvs", "~/mnt/www.ipvs"],
    # ["supermuc:", "~/mnt/supermuc"] 
]

mstatus = ["OK", "FAILED", "TIMEOUT"]

def mount_cmd(dev, diry, unmount):
    if unmount:
        return "fusermount -u {}".format(diry)
    else:
        return "sshfs {} {}".format(dev, diry)

def thrd_mount(cmd):
    try:
        subprocess.check_call(cmd, shell=True, timeout=10)
    except subprocess.CalledProcessError:
        ret = 1
    except subprocess.TimeoutExpired:
        ret = 2
    else:
        ret = 0

    print("{:70s} {}".format(cmd, mstatus[ret]))

if __name__ == "__main__":
    uflag = len(sys.argv) > 1 and sys.argv[1] == "-u"

    for dev, diry in mounts:
        cmd = mount_cmd(dev, diry, uflag)
        threading.Thread(target=thrd_mount, args=(cmd,)).start()

