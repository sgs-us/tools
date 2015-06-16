#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Little hack for writing the same files to a large number of USB Sticks.
'''

import glib
from pyudev import Context, Monitor
import dbus
import time
import shutil
import os
import stat
import subprocess

# number of files to copy
counter = 80

'''
find where usb stick was mounted from /proc/mounts
@param dev something like /def/sdxa
'''
def find_mountpoint(dev):
    for l in open("/proc/mounts", "r"):
        cont = l.split(" ")
        device = cont[0]
        mp = cont[1]
        if device == dev:
            return mp
    return None


'''
copy specified files from current working directory to dest.
@param dest location to copy to
'''
def start_copy(dest):
    src = os.getcwd()
    shutil.copy(os.path.join(src, "boa.pdf"), dest)
    shutil.copy(os.path.join(src, "program.pdf"), dest)
    # for dirpath, dirnames, filenames in os.walk(dest):
    #     for f in filenames:
    #         os.chmod(os.path.join(dest, f), 0o777)
    #     break


'''
if a new usb device was plugged in, if this device is a filesystem and the
filesystem is not /sda.
If such a device is found copy files to it, decrease the counter and unmount the device
'''
def get_devices():
    global counter
    global mainLoop
    bus = dbus.SystemBus()
    ud_manager_obj = bus.get_object('org.freedesktop.UDisks2', '/org/freedesktop/UDisks2')
    om = dbus.Interface(ud_manager_obj, 'org.freedesktop.DBus.ObjectManager')

    for k,v in om.GetManagedObjects().iteritems():
        drive_info = v.get('org.freedesktop.UDisks2.Block', {})
        # get drive_info, we dont want to have our local harddrive.
        if drive_info.get('IdUsage') == "filesystem" and not k[-5:-1] == '/sda':
            dest = find_mountpoint("/dev" + k[-5:])
            print "/dev" + k[-5:], "mounted on", dest
            print "copying files"
            start_copy(dest)
            print "copying done"
            counter = counter - 1
            print "unmounting device"
            subprocess.call(["umount", dest])
            print "unmounting done. ", counter, "devices remaining"
            if counter == 0:
                mainLoop.quit()
                exit()

'''
main loop.
Listen on dbus for a new usb device being plugged in.
Wait some time until the automount procedure is done and do all the fancy stuff from above
'''
# try importing different Monitors
try:
    from pyudev.glib import MonitorObserver

    def device_event(observer, device):
        print 'event {0} on device {1}'.format(device.action, device)
        if device.device_type == 'usb_interface' and action == 'add':
            print "waiting for automount"
            time.sleep(3)
            print "starting proc"
            get_devices()
        else:
            print device.device_type, action

except:
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver

    def device_event(observer, action, device):
        print 'event {0} on device {1}'.format(action, device)
        if device.device_type == 'usb_interface' and action == 'add' and counter > 0:
            print "waiting for automount"
            time.sleep(5)
            print "starting proc"
            get_devices()
        else:
            print device.device_type, action


context = Context()
monitor = Monitor.from_netlink(context)

monitor.filter_by(subsystem='usb')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)
monitor.start()

mainLoop = glib.MainLoop()
mainLoop.run()

