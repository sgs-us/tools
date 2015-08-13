from math import cos, sin

'''
note: to use this file within tikz you have to add the following definition to your tex file:
\makeatletter
\tikzoption{canvas is xy plane at z}[]{%
  \def\tikz@plane@origin{\pgfpointxyz{0}{0}{#1}}%
  \def\tikz@plane@x{\pgfpointxyz{1}{0}{#1}}%
  \def\tikz@plane@y{\pgfpointxyz{0}{1}{#1}}%
  \tikz@canvas@is@plane
}
\makeatother

\tikzset{xyp/.style={canvas is xy plane at z=#1}}
\tikzset{xzp/.style={canvas is xz plane at y=#1}}
\tikzset{yzp/.style={canvas is yz plane at x=#1}}
'''

def quad2D(lowerLeft, upperRight, angle=0):
    print (r"\begin{scope}")
    # print (r"\pgftransformcm{%f}{%f}{%f}{%f}{\pgfpoint{0 cm}{0 cm}}" % (cos(angle), sin(angle), cos(angle), -sin(angle)))
    print (r"\draw (%f, %f) rectangle (%f, %f);" % (lowerLeft[0], lowerLeft[1],
                                                    upperRight[0], upperRight[1]))
    print (r"\end{scope}")

def quad3D(backLowerLeft, frontUpperRight):
    print (r"\begin{scope}")
    print (r"\draw[xyp=%f] (%f, %f) rectangle (%f, %f);" %
           (backLowerLeft[2],
            backLowerLeft[0]  , backLowerLeft[1]  ,
            frontUpperRight[0], frontUpperRight[1]))
    print (r"\draw[xyp=%f] (%f, %f) rectangle (%f, %f);" %
           (frontUpperRight[2],
            backLowerLeft[0]  , backLowerLeft[1]  ,
            frontUpperRight[0], frontUpperRight[1]))

    print (r"\draw[xzp=%f] (0, 0) (%f, %f) rectangle (%f, %f);" %
           (backLowerLeft[1],
            backLowerLeft[0]  , backLowerLeft[2],
            frontUpperRight[0], frontUpperRight[2]))
    print (r"\draw[xzp=%f] (%f, %f) rectangle (%f, %f);" %
           (frontUpperRight[1],
            backLowerLeft[0]  , backLowerLeft[2],
            frontUpperRight[0], frontUpperRight[2]))

    print (r"\draw[yzp=%f] (%f, %f) rectangle (%f, %f);" %
           (backLowerLeft[0],
            backLowerLeft[1]  , backLowerLeft[2]  ,
            backLowerLeft[1]  , frontUpperRight[2]))
    print (r"\draw[yzp=%f] (%f, %f) rectangle (%f, %f);" %
           (frontUpperRight[0],
            backLowerLeft[1]  , backLowerLeft[2],
            frontUpperRight[1], frontUpperRight[2]))
    print (r"\end{scope}")

def gridFromEnc2D(enc):
    level = 0
    lctr = [0]
    quads = []

    # function to increment the level counter; includes completion of blocks
    def incrLCtr(l):
        nonlocal level
        if lctr[l] < 3:
            lctr[l] += 1
        else:
            lctr[l] = 0
            incrLCtr(l-1)
            level -= 1

    # process encoding and draw child cells (i.e. all unrefined cells)
    for c in enc:
        if c == '1':
            level += 1
            if len(lctr) < level + 1:
                lctr.append(0)
        else:
            pos = [[0, 0], [1, 1]]
            if len(lctr) < level:
                lctr.append(0)
            for i in range(level + 1):
                if lctr[i] % 2 == 1:
                    pos[0][0] += 1./float(1 << i)
                if lctr[i] > 1:
                    pos[0][1] += 1./float(1 << i)
            pos[1][0] = pos[0][0] + 1./float(1 << level)
            pos[1][1] = pos[0][1] + 1./float(1 << level)
            quads.append(pos)
            incrLCtr(level)

    for q in quads:
        quad2D(q[0], q[1])

def gridFromEnc3D(enc):
    level = 0
    lctr = [0]
    quads = []

    # process encoding and draw child cells (i.e. all unrefined cells)
    # import ipdb; ipdb.set_trace()

    def incrLCtr(l):
        nonlocal level
        if lctr[l] < 7:
            lctr[l] += 1
        else:
            lctr[l] = 0
            incrLCtr(l-1)
            level -= 1


    for c in enc:
        if c == '1':
            level += 1
            if len(lctr) < level + 1:
                lctr.append(0)
        else:
            pos = [[0, 0, 0], [1, 1, 1]]
            if len(lctr) < level:
                lctr.append(0)
            for i in range(level + 1):
                # x direction
                if lctr[i] % 2 == 1:
                    pos[0][0] += 1./float(1 << i)
                # y direction
                if lctr[i] in [2, 3, 6, 7]:
                    pos[0][1] += 1./float(1 << i)
                # z direction
                if lctr[i] > 3:
                    pos[0][2] += 1./float(1 << i)
            pos[1][0] = pos[0][0] + 1./float(1 << level)
            pos[1][1] = pos[0][1] + 1./float(1 << level)
            pos[1][2] = pos[0][2] + 1./float(1 << level)
            quads.append(pos)
            incrLCtr(level)

    for q in quads:
        quad3D(q[0], q[1])
