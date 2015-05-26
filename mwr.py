#!env python2

""" Make world readable: Scripts that sets the permission of all directories up to path and all files and directories down from path to to o+xr. """

import os, stat, sys

def norm_path(*parts):
    """ Returns the normalized, absolute, expanded and joint path, assembled of all parts. """
    return os.path.abspath(os.path.expanduser(os.path.join(*parts)))

def concat_iter(iterable, join = ""):
    """ An iterator which returns more and more of an iterable. range(4) would return: "0", "01", "012" and "0123". """
    result = ""
    yield join
    for i in iterable[1:]:
        result = join.join([result, i])
        yield result


try:
    path = norm_path(sys.argv[1])
except:
    print "Please suppy a path."
    sys.exit(-1)
    
print "Working on ", path

# Walking from / to current working dir
for i in concat_iter(path.split(os.path.sep), join=os.path.sep):
    st = os.stat(i).st_mode
    if stat.S_ISDIR(st):
        if (st & stat.S_IROTH) and (st & stat.S_IXOTH):
            print "Not setting permissions on %s" % i
        else:
            print "Setting permissions on %s" % i
            os.chmod(i, st | stat.S_IROTH | stat.S_IXOTH)

# Walking from current working dir into all subdirs
for root, dirs, files in os.walk(path):
    for d in dirs:
        d = os.path.join(root, d)
        st = os.stat(d).st_mode
        if (st & stat.S_IROTH) and (st & stat.S_IXOTH):
            print "Not setting permissions on %s" % d
        else:
            print "Setting permissions on %s" % d
            os.chmod(f, st | stat.S_IROTH | stat._SIXOTH)

            
    for f in files:
        f = os.path.join(root, f)
        st = os.stat(f).st_mode
        if (st & stat.S_IROTH):
            print "Not setting permissions on %s" % f
        else:
            print "Setting permissions on %s" % f
            os.chmod(f, st | stat.S_IROTH)
           
